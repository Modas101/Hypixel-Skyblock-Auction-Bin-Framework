import rpi
import time

RolimonAPI = rpi.RPI()


class Values():
    def __init__(self):
        self.roliValues = {}
        RolimonAPI.ParseOnlyValues(self.roliValues)

    def check(self):
        startTime = time.perf_counter()

        print("\nValue Updater: Checking for changes in values")

        RolimonAPI.ParseOnlyValues(self.roliValues)


        with open("values", "r") as values:

            lines = values.readlines()

            changed = False

            for i, line in enumerate(lines):
                list = line.split(":")

                if self.roliValues.get(list[0]):

                    if self.roliValues[list[0]] != int(list[1]):
                        newValue = self.roliValues[list[0]]
                        print(f"\nValue Updater: Item {list[0]} changed from {list[1]} to {newValue}")
                        list[1] = str(newValue)
                        lines[i] = ':'.join(list)
                        changed = True

            if changed:
                print("\nValue Updater: Replacing updated lines!")

                with open("values", "w") as valueWrite:
                    valueWrite.writelines(lines)
                    return True
            else:
                print("\nValue Updater: No changes detected!")

        print(f"\nValue Updater: Time elapsed: {time.perf_counter() - startTime}")