import subprocess
import atexit


class Olympian:
    def __init__(self):
        olympian = subprocess.Popen(
            ["olympian.exe"],
            bufsize=1,
            universal_newlines=True
        )

        self.olympian = olympian
        print("Olympian process started!")
        atexit.register(self.termination)

    def termination(self):
        print("Olympian process terminated!")
        self.olympian.terminate()

    def __del__(self):
        atexit.unregister(self.termination)