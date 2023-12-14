# Recursive Function
# def fibonacci(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     else:
#         return fibonacci(n - 1) + fibonacci(n - 2)

# print("The first 10 Fibonacci numbers are:")
# for i in range(10):
#     print(fibonacci(i))

## Using while
# def fibonacci(n):
#     a, b, i = 0, 1, 1
#     while i <= n : 
#         i += 1
#         yield a
#         a, b = b, a + b
# for i in fibonacci(10):
#     print(i)

## Weith Dictionary
# def fibonacci(n):
#     fib_dict = {}
#     fib_dict[0] = 0
#     fib_dict[1] = 1
#     for i in range(2, n + 1):
#         fib_dict[i] = fib_dict[i - 1] + fib_dict[i - 2]
#     yield from fib_dict.values()

# for i in fibonacci(20):
#     print(i)

## Final good version with list
def fibonacci(n):
    fib_list = [0, 1]
    for i in range(2, n + 1):
        fib_list.append(fib_list[i - 1] + fib_list[i - 2])
    yield from fib_list

for i in fibonacci(20):
    print(i)
