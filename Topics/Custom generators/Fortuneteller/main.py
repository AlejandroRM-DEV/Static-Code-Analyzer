# put your code here
number = input()
generator = (int(n) for n in number)
sum = 0
for n in generator:
    sum += n
print(sum)
