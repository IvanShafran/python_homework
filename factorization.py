def stupid_factorization(number):
    factorization_list = dict()
    i = 2
    while i*i <= number:
        if number % i == 0:
            factorization_list[i] = 0
        while number % i == 0:
            factorization_list[i] += 1
            number //= i
        i += 1

    if number != 1:
        factorization_list[number] = 1

    return tuple((x, factorization_list[x])
                 for x in factorization_list)


if __name__ == '__main__':
    number = int(input())
    print(stupid_factorization(number))
