maxMoney = 0
maxFarms = 20
wave = 0
money = 600

farms = []

farmProductionArr = [
    80,
    120,
    160,
    320,
    1500,
    6000
]

farmCostArr = [
    1000,
    500,
    600,
    3000,
    19000,
    100000
]

tier5Taken = 6

while wave <= 100:

    for farmNum in range(0, len(farms)):
        while farms[farmNum]["level"] + 1 < tier5Taken:
            cost = farmCostArr[farms[farmNum]["level"] + 1]
            if not farms[farmNum]["lvl2Banana"]:
                if cost + 1100 <= money:
                    money -= cost
                    money -= 1100
                    farms[farmNum]["level"] += 1
                    farms[farmNum]["lvl2Banana"] = True
                    if farms[farmNum] == 5:
                        tier5Taken = 5
                    print(f"Upgrade farm number {farmNum + 1} to level {farms[farmNum]}")
                    print(f"Upgrade farm number {farmNum + 1}'s to valuable bananas")
                elif cost <= money or 1100 <= money:
                    if farmProductionArr[farms[farmNum]["level"] + 1] < farmProductionArr[farms[farmNum]["level"]] * 1.25:
                        farms[farmNum]["lvl2Banana"] = True
                        money -= 1100
                        print(f"Upgrade farm number {farmNum + 1}'s to valuable bananas")
                    else:
                        money -= cost
                        farms[farmNum]["level"] += 1
                        if farms[farmNum] == 5:
                            tier5Taken = 5
                        print(f"Upgrade farm number {farmNum + 1} to level {farms[farmNum]}")
                else:
                    break
            elif cost <= money:
                money -= cost
                farms[farmNum]["level"] += 1
                if farms[farmNum] == 5:
                    tier5Taken = 5
                print(f"Upgrade farm number {farmNum + 1} to level {farms[farmNum]}")
            else:
                break

    while len(farms) < maxFarms and money >= farmCostArr[0]:
        farms.append({"level": 0, "lvl2Banana": False})
        money -= farmCostArr[0]
        print(f"Purchase farm number {len(farms)}")

        for farmNum in range(0, len(farms)):
            while farms[farmNum]["level"] + 1 < tier5Taken:
                cost = farmCostArr[farms[farmNum]["level"] + 1]
                if not farms[farmNum]["lvl2Banana"]:
                    if cost + 1100 <= money:
                        money -= cost
                        money -= 1100
                        farms[farmNum]["level"] += 1
                        if farms[farmNum] == 5:
                            tier5Taken = 5
                        farms[farmNum]["lvl2Banana"] = True
                        print(f"Upgrade farm number {farmNum + 1} to level {farms[farmNum]}")
                        print(f"Upgrade farm number {farmNum + 1}'s to valuable bananas")
                    elif cost <= money or 1100 <= money:
                        if farmProductionArr[farms[farmNum]["level"] + 1] < farmProductionArr[
                            farms[farmNum]["level"]] * 1.25:
                            farms[farmNum]["lvl2Banana"] = True
                            money -= 1100
                            print(f"Upgrade farm number {farmNum + 1}'s to valuable bananas")
                        else:
                            money -= cost
                            farms[farmNum]["level"] += 1
                            if farms[farmNum] == 5:
                                tier5Taken = 5
                            print(f"Upgrade farm number {farmNum + 1} to level {farms[farmNum]}")
                    else:
                        break
                elif cost <= money:
                    money -= cost
                    farms[farmNum]["level"] += 1
                    if farms[farmNum] == 5:
                        tier5Taken = 5
                    print(f"Upgrade farm number {farmNum + 1} to level {farms[farmNum]}")
                else:
                    break

    for produce in farms:
        if produce["level"] >= 0:
            multiplier = 1
            multiplier += produce["lvl2Banana"] and 0.25
            multiplier += tier5Taken == 5 and produce["level"] == 4 and 0.25
            money += farmProductionArr[produce["level"]] * multiplier

    print(f"Wave: {wave}, Money: {money}")

    wave += 1
    money += 200

waveProduce = 0

for produce in farms:
    if produce["level"] >= 0:
        multiplier = 1
        multiplier += produce["lvl2Banana"] and 0.25
        multiplier += tier5Taken == 5 and produce["level"] == 4 and 0.25
        waveProduce += farmProductionArr[produce["level"]] * multiplier

print(f"\nFinished with ${money}\nWaveProduce: {waveProduce}")
