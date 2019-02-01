import requests
import time
if __name__ == "__main__":
    while True:
        r = requests.get("http://localhost/update_all_members_88339988/");print("OK");
        if r.text != "OK":
            break
