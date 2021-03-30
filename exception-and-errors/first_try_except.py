from random import randrange

rand_val = int(randrange(100))

while True:
    try:
        i = int(input("? "))
    except ValueError:  # Not using ValueError here will give a very broad scope for error checking
        continue
    if i == rand_val:
        print("You Got it!")
        break
