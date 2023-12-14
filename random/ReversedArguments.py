def reversed_args(f):
    return f

int_func_map = {
    'pow': lambda x, y: reversed_args(pow(y, x)),
    'cmp': lambda x, y: reversed_args(y - x),
}

string_func_map = {
    'join_with': lambda strings: reversed_args(str(strings[-1:][0]).join(reversed(strings[:-1]))),
    'capitalize_first_and_join': lambda strings: reversed_args(str(strings[-1:][0]).upper() + ''.join(reversed(strings[:-1]))),
}

# Read the number of queries
queries = int(input())

# Read and process each query
for _ in range(queries):
    line = input().split()
    func_name, args = line[0], line[1:]
    if func_name in int_func_map:
        args = list(map(int, args))
        print(int_func_map[func_name](*args))
    else:
        print(string_func_map[func_name](args))

