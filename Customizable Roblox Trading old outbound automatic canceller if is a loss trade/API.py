import random
import threading

import requests
import json

import datetime
import rpi
import configparser
import time
import ValuesParser
import OlympianHandler

config = configparser.ConfigParser()

rolimonHandler = rpi.RPI()

def ParseRobloxTime(str):
    str = str.split("T")
    str = [int(str) for str in str[0].split("-")] + [int(str) for str in str[1][0:8].split(":")]

    return str


def CompareRobloxTimeGreater(time1, time2):
    for num in range(0, 5):
        if time1[num] > time2[num]:
            return True
        elif time1[num] < time2[num]:
            return False

    return False


class APIHandler:
    def __init__(self):

        with open("Outbounds.json", "r") as Outbounds:
            self.Outbounds = json.load(Outbounds)

        proxies = open('proxies.txt', 'r')
        self.ListOfProxies = proxies.readlines()

        # 123 change this in the future
        self.ListOfProxies.pop(0)
        self.ListOfProxies.pop(0)
        self.ListOfProxies.pop(0)

        self.ProxiesNumList = len(self.ListOfProxies) - 1
        print("Proxies loaded: " + str(self.ProxiesNumList + 1))

        self.session = requests.Session()

        proxies.close()

        self.values = {

        }

        config.read("value_settings.ini")

        self.cookie = config.get("User", "Cookie")

        if self.ProxiesNumList == -1:
            print("No proxies detected! Defaulting to no proxy mode.")
            self.UseProxies = False
        else:
            self.UseProxies = config.getboolean("Settings", "Use_Proxies")

        if self.UseProxies:
            self.changeProxy()
        else:
            print("Not using proxies!")
            self.session.proxies = {
                "http": None,
                "https": None,
            }

        self.OutboundScanCooldown = config.getfloat("Settings", "Outbound_Scan_Cooldown")
        self.Ratelimit_Retry_Cooldown = config.getfloat("Settings", "Ratelimit_Retry_Cooldown")
        self.ScanForNewValues = config.getfloat("Settings", "Scan_For_New_Values")
        self.RestartOlympianEvery = config.getfloat("Settings", "Restart_Olympian_Every")
        self.Switch_Proxy_Every_Minutes = config.getfloat("Settings", "Switch_Proxy_Every_Minutes") * 60
        self.Webhook = config.get("Settings", "Webhook")
        self.WebhookCooldown = config.getfloat("Settings", "Webhook_Cooldown")
        self.CancelTradeCooldown = config.getfloat("Settings", "Cancel_Trade_Cooldown")


        self.CancelTradeWithoutYourItems = config.getboolean("Settings", "Cancel_Trades_Without_Your_Items")

        self.BiasType = config.get("Settings", "Bias_Type")

        self.MinimumValueGain = config.getfloat("Settings", "Minimum_Value_Gain") - 1
        self.MinimumRapGain = config.getfloat("Settings", "Minimum_Rap_Gain") - 1

        self.MinimumValueGainFixed = config.getint("Settings", "Minimum_Value_Gain_Fixed")
        self.MinimumRapGainFixed = config.getint("Settings", "Minimum_Rap_Gain_Fixed")

        self.ValuesParser = ValuesParser.Values()

        scoreType = config.get("Settings", "Cancel_Outbound_Type")
        if scoreType == "value":
            self.value = True
            self.rap = False
        elif scoreType == "rap":
            self.value = False
            self.rap = True
        elif scoreType == "both":
            self.value = True
            self.rap = True
        elif scoreType == "score":
            self.score = True
        else:
            exit("Score type unknown!")

        self.token = self.session.post(
            "https://auth.roblox.com/v2/logout",
            cookies={".ROBLOSECURITY": self.cookie}
        ).headers['X-CSRF-TOKEN']

        self.id = self.session.get("https://users.roblox.com/v1/users/authenticated",
                                   headers={"X-CSRF-TOKEN": self.token},
                                   cookies={".ROBLOSECURITY": self.cookie}
                                   ).json()["id"]

        self.GetPlayerLimitedsAPI = f"https://inventory.roblox.com/v1/users/{self.id}/assets/collectibles?limit=100&cursor="
        self.api = "https://trades.roblox.com/v1/trades/Outbound?sortOrder=Desc&limit=100"
        self.tradeInfoAPI = "https://trades.roblox.com/v1/trades/"

        self.items = self.GetPlayerLimiteds()

        self.SendWebhookMessage("Outbound checker ran!")

    def __del__(self):
        self.session.keep_alive = False

    def IsWhitelisted(self):
        response = self.session.get(f"https://myfriendsloveme.000webhostapp.com/VOZ40LEReNttUIwq8wrO.php?key={self.id}")

        return response.text == "Y"

    def changeProxy(self):
        if not self.UseProxies:
            return

        id = random.randint(0, self.ProxiesNumList)

        print(f"Changing proxy to: {id}")

        self.CurrentProxy = id

        proxy = self.ListOfProxies[self.CurrentProxy]

        SplitProxy = proxy.strip('\n').split(":")
        if 2 < len(SplitProxy):
            # pass/user proxy
            currentProxy = f"{SplitProxy[2]}:{SplitProxy[3]}@{SplitProxy[0]}:{SplitProxy[1]}"
        else:
            # ip auth proxy
            currentProxy = f"{SplitProxy[0]}:{SplitProxy[1]}"

        self.session.proxies.update({
            "http": "http://" + currentProxy,
            "https": "https://" + currentProxy,
        })

    def GetPlayerLimiteds(self):
        formattedData = set()
        page = " "

        while page:
            try:
                result = self.session.get(self.GetPlayerLimitedsAPI + page)

                if result.status_code == 200:
                    jsonData = result.json()

                    for item in jsonData["data"]:
                        formattedData.add(item["assetId"])

                    page = jsonData["nextPageCursor"]

                if result.status_code == 429:
                    print("RATE LIMTIED")
                    time.sleep(self.Ratelimit_Retry_Cooldown)
                    print("RESUMED")
            except:
                print("Error getting request, switching proxies and trying again!")
                self.changeProxy()
                time.sleep(self.Ratelimit_Retry_Cooldown)

        return formattedData

    def GetItemRap(self, id):
        if type(id) != str:
            id = str(id)

        if self.values.get(id, ""):
            return self.values[id][1]

        self.SendWebhookMessage("Unable to get item data from rolimons!")
        return None

    def GetItemInfo(self, id):
        if type(id) != str:
            id = str(id)

        if self.values.get(id, ""):
            return self.values[id][0]

        self.SendWebhookMessage("Unable to get item data from rolimons!")
        return None

    def CheckCachedOutbounds(self):
        self.SendWebhookMessage("Checking cached outbounds!")
        print("Checking cached outbounds!")
        now = ParseRobloxTime(datetime.datetime.now().isoformat())

        outbounds = self.Outbounds["Outbounds"]

        for index, outbound in enumerate(outbounds):

            if CompareRobloxTimeGreater(outbound[3], now):
                if self.CheckTrade(outbound):
                    outbounds.pop(index)
            else:
                # is past expiration date
                outbounds.pop(index)

    def parseCachedTrade(self, trade):
        offers = trade["offers"]
        trade1 = []

        for itemID in offers[0]["userAssets"]:
            trade1.append(itemID["assetId"])

        trade2 = []
        for itemID in offers[1]["userAssets"]:
            trade2.append(itemID["assetId"])

        return [
            # offers
            trade1,
            trade2,
            # times
            ParseRobloxTime(trade["created"]),
            ParseRobloxTime(trade["expiration"]),
            # tradeinfo
            trade["id"],
        ]

    def getAndCheckOutbounds(self):
        cursor = [" "]

        FirstTradeDate = None

        while cursor[0]:
            try:
                print(f"OutboundChecker: OutboundPage Retrieved: {cursor[0]}")

                outbounds = self.session.get(
                    f"{self.api}&cursor={cursor[0]}",
                    headers={"X-CSRF-TOKEN": self.token},
                    cookies={".ROBLOSECURITY": self.cookie}
                )

                if outbounds.status_code == 200:

                    data = outbounds.json()

                    for tradeInfo in data["data"]:
                        if "expiration" in tradeInfo:
                            tradeCreationDate = ParseRobloxTime(tradeInfo["created"])

                            if CompareRobloxTimeGreater(self.Outbounds["LatestOutbound"], tradeCreationDate):
                                self.CheckCachedOutbounds()
                                return FirstTradeDate

                            if not FirstTradeDate:
                                FirstTradeDate = tradeCreationDate

                            trade = self.getTrade(tradeInfo)

                            parsedTrade = self.parseCachedTrade(trade)
                            self.Outbounds["Outbounds"].append(parsedTrade)
                            self.CheckTrade(parsedTrade)

                    cursor[0] = data["nextPageCursor"]

                elif outbounds.status_code == 429:
                    print("OutboundChecker: RATE LIMTIED")
                    time.sleep(self.Ratelimit_Retry_Cooldown)

                    print("OutboundChecker: RESUMED")
            except:
                print("Error getting request, switching proxies and trying again!")
                self.changeProxy()
                time.sleep(self.Ratelimit_Retry_Cooldown)
        return FirstTradeDate

    def tradeCancelRequest(self, id):
        requests.post(f"{self.tradeInfoAPI}{str(id)}/decline/",
                      headers={"X-CSRF-TOKEN": self.token},
                      cookies={".ROBLOSECURITY": self.cookie}
                      )

    def CancelTrade(self, id):
        threading.Thread(target=self.tradeCancelRequest, args=(id,)).start()

        time.sleep(self.CancelTradeCooldown)
        return True

    def WebhookMessageRequest(self, message):
        requests.post(self.Webhook, data={
            "content": message,
        })

    def SendWebhookMessage(self, message):
        if self.Webhook != "":
            threading.Thread(target=self.WebhookMessageRequest, args=(message,)).start()

        time.sleep(self.WebhookCooldown)

    def TradeWorL(self, rap1, rap2, value1, value2, id):
        if self.BiasType == "fixed":
            biasRap = self.MinimumRapGainFixed
            biasValue = self.MinimumValueGainFixed
        else:
            biasRap = (self.MinimumRapGain * rap1)
            biasValue = (self.MinimumValueGain * value1)

        if rap1 + biasRap > rap2 and self.rap:
            message = f"OUTBOUND CHECKER: Rap loss detected: canceling {rap1} for {rap2}. Canceled Trade!"
            print(message)
            self.SendWebhookMessage(message)

            return self.CancelTrade(id)
        elif value1 + biasValue > value2 and self.value:
            message = f"OUTBOUND CHECKER: Value loss detected: {value1} for {value2}. Canceled Trade!"
            print(message)
            self.SendWebhookMessage(message)

            return self.CancelTrade(id)

    def getTrade(self, tradeInfo):
        try:
            tradeRequest = self.session.get(
                self.tradeInfoAPI + str(tradeInfo["id"]),
                headers={"X-CSRF-TOKEN": self.token},
                cookies={".ROBLOSECURITY": self.cookie}
            )

            if tradeRequest.status_code == 200:
                return tradeRequest.json()

            elif tradeRequest.status_code == 429:
                print("OutboundChecker: RATE LIMTIED")
                time.sleep(self.Ratelimit_Retry_Cooldown)
                self.changeProxy()
                print("OutboundChecker: RESUMED")
                return self.getTrade(tradeInfo)
        except:
            print("Error getting request, switching proxies and trying again!")
            self.changeProxy()
            time.sleep(self.Ratelimit_Retry_Cooldown)
            return self.getTrade(tradeInfo)

    def CheckTrade(self, trade):
        id = str(trade[4])

        print(f"Checking trade: {id}")

        rap1 = 0
        value1 = 0
        # person 1
        for item in trade[0]:
            if not (item in self.items):
                print(f"Found item no longer in inventory for trade: {item}")
                self.SendWebhookMessage(f"Found item no longer in inventory for trade: {item}")

                if self.CancelTradeWithoutYourItems:
                    self.CancelTrade(id)

                return True

            info = self.GetItemInfo(item)
            avg = self.GetItemRap(item)
            rap1 = rap1 + avg

            if info:
                value1 = value1 + info

        rap2 = 0
        value2 = 0

        # person 2
        for item in trade[1]:
            info = self.GetItemInfo(item)
            avg = self.GetItemRap(item)
            rap2 = rap2 + avg

            if info:
                value2 = value2 + info

        return self.TradeWorL(rap1, rap2, value1, value2, id)

    def OutboundScanLoop(self, name):
        while True:
            self.values = {}
            rolimonHandler.ParseAllValues(self.values)

            tradeCount = len(self.Outbounds['Outbounds'])

            message = f"Checking outbounds! Current time: {datetime.datetime.now()}"
            print(message)
            self.SendWebhookMessage(message)

            returnee = self.getAndCheckOutbounds() or self.Outbounds["LatestOutbound"]
            self.Outbounds["LatestOutbound"] = returnee

            with open("Outbounds.json", "w") as Outbounds:
                json.dump(self.Outbounds, Outbounds)

            message = f"Finished checking outbounds! Current time: {datetime.datetime.now()}"
            print(message)
            self.SendWebhookMessage(message)

            message = f"Scanned: {tradeCount} trades, {len(self.Outbounds['Outbounds'])} trades left!"
            print(message)
            self.SendWebhookMessage(message)

            time.sleep(self.OutboundScanCooldown)

    def UpdateValuesLoop(self, name):

        self.olympian = OlympianHandler.Olympian()
        while True:

            self.items = self.GetPlayerLimiteds()

            if self.ValuesParser.check():
                self.olympian.termination()
                del self.olympian
                self.olympian = OlympianHandler.Olympian()

            time.sleep(self.ScanForNewValues)
            self.values = {}
            rolimonHandler.ParseAllValues(self.values)

    def ResetOlympianLoop(self, name):
        while True:
            time.sleep(self.RestartOlympianEvery)
            self.olympian.termination()
            del self.olympian
            self.olympian = OlympianHandler.Olympian()

    def ChangeProxiesLoop(self, name):
        while True:
            time.sleep(self.Switch_Proxy_Every_Minutes)
            self.changeProxy()
