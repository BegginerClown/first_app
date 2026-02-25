from math import sqrt

n = 8261200

# Найдём все делители
divisors = set()
for i in range(1, int(sqrt(n)) + 1):
    if n % i == 0:
        divisors.add(i)
        divisors.add(n // i)

# Отфильтруем делители >= 100000
large_divisors = sorted([d for d in divisors if d >= 100000])
large_divisors[:20], len(large_divisors)
print(large_divisors[0])