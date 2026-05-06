import Module

print(Module.hello_rust())
print(Module.sum_as_string(1, 2))
print(Module.hello(1, 2))


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


import time

t1 = time.time()

print(fib(40))
t2 = time.time()
print("Python fib(40) took %s seconds" % (t2 - t1))

print(Module.fib(40))
t3 = time.time()
print("Rust fib(40) took %s seconds" % (t3 - t2))

print(Module.fib_map([1,2,3,4,5]))