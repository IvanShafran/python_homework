def next_fibonacci(sequence, modulo):
    return (sequence[len(sequence) - 2] +
            sequence[len(sequence) - 1]) % modulo


def fibonacci(number, modulo):
    sequence = [0, 1]
    for x in range(number):
        sequence.append(next_fibonacci(sequence, modulo))

    return sequence

if __name__ == '__main__':
    period = 58
    sequence = fibonacci(period, 10)

    number = int(input())
    print(sequence[number % period])
