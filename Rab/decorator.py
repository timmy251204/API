user = {
    'name': 'masha',
    'access_level': 'admin'
}
Password = 'Brawl_stars'
def benchmark(func):
    import time

    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end - start))

    return wrapper


def secure_function(func):
    def wrapper(*args, **kwargs):
        if user['access_level'] == 'admin':
            return func(*args, **kwargs)
        return 'Access denied'

    return wrapper


def check_password(func):
    checked = 0
    def wrapper(*args, **kwargs):
        nonlocal checked
        if checked <= 0:
            print('ВВЕДИТЕ ПАРОЛЬ')
            check = input()
            if check == Password:
                checked += 1
                return func(*args, **kwargs)
            else:
                print('В доступе отказано')
        else:
            return func(*args, **kwargs)


    return wrapper







def get_secure_information():
    return 'My super password is qwerty123'
# print_ = print
# print = lambda *args: print_(' '.join(map(str.upper, args))) Print Capsom



@check_password
def fibonacci(n):
    if n in (1, 2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def fib_with_cache(n):
    if n in fib_with_cache.cache:
        return fib_with_cache.cache[n]
    if n in (1, 2):
        fib_with_cache.cache[n] = 1
        return 1
    fib_with_cache.cache[n] = fib_with_cache.cache(n - 1) + fib_with_cache.cache(n - 2)
    return fib_with_cache.cache[n]
fib_with_cache.cache = {}






print(fibonacci(8))