import random

ans = {}
questions = []

with open("input.txt", "r") as inp:
    lines = inp.readlines()
    res = ""

    for i, line in enumerate(lines):
        splitline = line.split("|")
        ans[splitline[0]] = splitline[1]
        questions.append(splitline[0])

while len(questions) > 0:
    randind = random.randrange(len(questions))
    print(ans[questions[randind]])
    res = input("Answer: ")
    if res == questions[randind]:
        print("Right!")
        questions.pop(randind)
        print(len(questions))
    else:
        print("Wrong!")
        print(questions[randind])