import socket
import sys
import os
import time

class timeit(object):

    def __init__(self, name='unnamed', output=True):
        self.name = name
        self.output = output
        self.beg = 0
        self.end = 0
        self.elapsed = 0

    def __enter__(self):
        self.beg = time.clock()
        return self

    def __exit__(self, *_):
        self.elapsed = time.clock() - self.beg
        if self.output:
            sys.stdout.write('{} executed {}s\n'.format(
                self.name, self.elapsed))

def send(data, ip='127.0.0.1', port=6560):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(data)
    s.close()

def loc(dir='.',
        includes=lambda fname: fname.endswith('.py'),
        excludes=lambda fname: fname == 't.py'):
    n_lines = 0
    for path, dirs, fnames in os.walk(dir):
        for fname in fnames:
            if not excludes(fname) and includes(fname):
                n_lines += len(open(os.path.join(path, fname)).readlines())
    return n_lines

class each(object):
    '''
    Succinct way to write `for` loop
    For example:

    >>> each('hello').upper()
    ['H', 'E', 'L', 'L', 'O']

    is equaivalent to

    >>> [c.upper() for c in 'hello']
    ['H', 'E', 'L', 'L', 'O']

    Normally, you will use this to call methods of instances in an array:

    >>> class Foo:
    ...     def __init__(self, n): self.n = n
    ...     def show(self): print self.n
    ...     def mul(self, factor): self.n *= factor; return self.n

    >>> a = [Foo(i) for i in range(3)]
    >>> e = each(a)
    >>> e.show()
    0
    1
    2
    [None, None, None]
    >>> e.mul(3)
    [0, 3, 6]
    '''

    class ItemProxy(object):

        def __init__(self, iterable, key):
            self.iterable = iterable
            self.key = key

        def __call__(self, *args, **kwargs):
            return [getattr(t, self.key)(*args, **kwargs)
                    for t in self.iterable]

    def __init__(self, iterable):
        self.__iterable = iterable

    def __getattribute__(self, key):
        if key == '_each__iterable':
            return object.__getattribute__(self, key)
        else:
            return each.ItemProxy(self.__iterable, key)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
