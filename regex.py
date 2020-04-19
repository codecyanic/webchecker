import re
from multiprocessing import Process, ProcessError


def search(pattern, text):  # pragma: no cover
    exit(bool(pattern.search(text)))


def safe_search(pattern, text, timeout):
    compiled = re.compile(pattern)

    p = Process(target=search, args=(compiled, text))
    p.start()
    p.join(timeout)

    if p.exitcode is None:
        p.terminate()
        raise TimeoutError('search process timeout')

    if p.exitcode < 0:
        raise ProcessError('search process terminated')

    return bool(p.exitcode)
