import API
import threading
import time
import atexit

def ExitFunc():
    del api

if __name__ == "__main__":
    print("Checking whitelist!")

    api = API.APIHandler()

    tries = 1

    while not api.IsWhitelisted():
        print(f"Whitelist not found! Trying again in 5 seconds! Attempt: {tries}")
        tries = tries + 1
        time.sleep(5)

    print("Whitelist found!")

    threading.Thread(target=api.UpdateValuesLoop, args=(0,)).start()
    threading.Thread(target=api.OutboundScanLoop, args=(0,)).start()
    threading.Thread(target=api.ResetOlympianLoop, args=(0,)).start()
    threading.Thread(target=api.ChangeProxiesLoop, args=(0,)).start()

    atexit.register(ExitFunc)

