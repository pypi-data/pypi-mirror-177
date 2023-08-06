import os
import signal
import sqlite3
from contextlib import contextmanager
from inspect import isgeneratorfunction
from itertools import chain, groupby
from pathlib import PurePath


@contextmanager
def _connect(db):
    conn = sqlite3.connect(db)
    conn.row_factory = _dict_factory
    try:
        yield conn
    finally:
        # Atomize the commit and close,
        # so that the keyboard interrupts do not corrupt the database
        with _delayed_keyboard_interrupts():
            conn.commit()
            conn.close()


@contextmanager
def _delayed_keyboard_interrupts():
    signal_received = []

    def handler(sig, frame):
        nonlocal signal_received
        signal_received = (sig, frame)
    # Do nothing but recording something has happened.
    old_handler = signal.signal(signal.SIGINT, handler)

    try:
        yield
    finally:
        # signal handler back to the original one.
        signal.signal(signal.SIGINT, old_handler)
        if signal_received:
            # do the delayed work
            old_handler(*signal_received)


class Inst:
    def __init__(self, iterable):
        def gen():
            yield from iterable

        self._iter_stack = [iterable if isgeneratorfunction(iterable) else gen]
        self._is_grouped = False

    def map(self, fn):
        # should be evaluated before the generator evokes

        fn = _fn2gen(fn)
        # previous generator
        pg = self._iter_stack[-1]

        def gen1():
            for r in pg():
                yield from fn(r)

        def gen2():
            for _, rs in pg():
                yield from fn(list(rs))

        self._iter_stack.append(gen2 if self._is_grouped else gen1)
        self._is_grouped = False

        return self

    def by(self, cols):
        cols = _listify(cols)

        pg = self._iter_stack[-1]

        def gen():
            rs = list(pg())
            keyfn = _keyfn(cols)
            rs.sort(key=keyfn)
            yield from groupby(rs, keyfn)

        self._iter_stack.append(gen)
        self._is_grouped = True

        return self

    def merge(self, fn, other):
        fn = _fn2gen(fn)

        empty = object()
        def _step(krs1, krs2):
            try:
                k1, rs1 = next(krs1)
                k2, rs2 = next(krs2)
                while True:
                    if k1 == k2:
                        yield from fn(list(rs1), list(rs2))
                        k1 = k2 = empty 
                        k1, rs1 = next(krs1)
                        k2, rs2 = next(krs2)
                    elif k1 < k2:
                        yield from fn(list(rs1), [])
                        k1 = empty 
                        k1, rs1 = next(krs1)
                    else:
                        yield from fn([], list(rs2))
                        k2 = empty 
                        k2, rs2 = next(krs2)
            except StopIteration:
                # unconsumed
                if k1 is not empty:
                    yield from fn(list(rs1), [])
                if k2 is not empty:
                    yield from fn([], list(rs2))

                for _, rs1 in krs1:
                    yield from fn(list(rs1), [])
                for _, rs2 in krs2:
                    yield from fn([], list(rs2))
        
        selfpg = self._iter_stack[-1]
        otherpg = other._iter_stack[-1]

        def gen():
            yield from _step(selfpg(), otherpg())

        self._iter_stack.append(gen)
        self._is_grouped = False
        return self

    def concat(self, other):

        selfpg = self._iter_stack[-1]
        otherpg = other._iter_stack[-1]

        def gen():
            for r in selfpg():
                yield r
            for r in otherpg():
                yield r

        self._iter_stack.append(gen)
        return self


class Conn:
    def __init__(self, dbfile):
        # dbfile must be a filename(str), can't be :memory:
        if PurePath(dbfile).is_absolute():
            self._db = dbfile
        else:
            self._db = os.path.join(os.getcwd(), dbfile)

        self._conn = None

    def inst(self, tname, by=None):
        def gen():
            yield from _fetch(self._conn, tname, by)

        nst = Inst(gen)
        if by:
            nst._is_grouped = True

        return nst

    def __setitem__(self, tname, nst):
        with _connect(self._db) as c:
            self._conn = c
            _delete(c, tname)
            _insert(c, tname, nst._iter_stack[-1]())

    def __getitem__(self, tname):
        try:
            return list(_fetch(self._conn, tname, None))
        # in case self._conn is either NoneType or closed connection
        except (AttributeError, sqlite3.ProgrammingError):
            with _connect(self._db) as c:
                return list(_fetch(c, tname, None))


def _insert_statement(name, d):
    """Generate an insert statememt.

    ex) insert into foo values (:a, :b, :c, ...)
        Notice the colons.
    """
    keycols = ', '.join(":" + c.strip() for c in d)
    return "insert into %s values (%s)" % (name, keycols)


def _create_statement(tname, cols):
    """Create table if not exists foo (...).

    Note:
        Every type is numeric.
    """
    schema = ', '.join([col + ' ' + 'numeric' for col in cols])
    return "create table if not exists %s (%s)" % (tname, schema)


def _listify(x):
    try:
        return [x1.strip() for x1 in x.split(',')]
    except AttributeError:
        try:
            return list(iter(x))
        except TypeError:
            # x not [x]
            return x


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _keyfn(cols):
    cols = _listify(cols)
    if len(cols) == 1:
        col = cols[0]
        return lambda r: r[col]
    return lambda r: [r[col] for col in cols]


def _delete(c, tname):
    c.cursor().execute(f'drop table if exists {tname}')


def _insert(c, tname, rs):
    try:
        r0 = next(rs)
    except StopIteration:
        raise ValueError(f"No row to insert in {tname}") from None
    else:
        cols = list(r0)

        c.cursor().execute(_create_statement(tname, cols))
        istmt = _insert_statement(tname, r0)
        c.cursor().executemany(istmt, chain([r0], rs))


def _fetch(c, tname, cols=None):
    if cols:
        cols = _listify(cols)
        query = f"select * from {tname} order by {','.join(cols)}"
        yield from groupby(c.cursor().execute(query), _keyfn(cols))
    else:
        query = f"select * from {tname}"
        yield from c.cursor().execute(query)


def _fn2gen(f):
    def gen(*r):
        x = f(*r)
        if isinstance(x, dict):
            yield x
        elif x is not None:
            yield from x

    return f if isgeneratorfunction(f) else gen
