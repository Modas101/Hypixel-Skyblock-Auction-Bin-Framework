import requests


class RPI:

    def ParseAllValues(self, ValueTable):
        Values = requests.get("https://www.rolimons.com/itemapi/itemdetails").json()['items']


        for key, value in Values.items():
            if str(value[3]) != "-1":
                ValueTable[key] = [value[3], value[2]]
            else:
                ValueTable[key] = [value[2], value[2]]

    def ParseOnlyValues(self, ValueTable):
        Values = requests.get("https://www.rolimons.com/itemapi/itemdetails").json()['items']


        for key, value in Values.items():
            if str(value[3]) != "-1":
                ValueTable[key] = value[3]

    def getValue(self, item):
        itemdetails = requests.get("https://www.rolimons.com/itemapi/itemdetails")
        itemcheck = itemdetails.json()['items'][str(item)][3]

        if str(itemcheck) != "-1":

            return itemdetails.json()['items'][str(item)][3]
        else:

            return itemdetails.json()['items'][str(item)][2]