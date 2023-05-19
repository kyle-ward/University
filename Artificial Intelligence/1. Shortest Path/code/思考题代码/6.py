import random

ans = random.randint(0, 10)
print(ans)
count = 1
guess = int(input())
while guess != ans:
    if guess > ans:
        print("猜大了")
    else:
        print("猜小了")
    guess = int(input())
    count += 1
print("一共猜了" + str(count) + "次")