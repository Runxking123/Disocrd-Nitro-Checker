import os
import requests
import random
import threading
import time
import json
from colorama import Fore

def center(var: str, space: int = None):  # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2

    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class Console():
    def ui(self):
        os.system(f'cls && title [H] Discord Nitro Generator' if os.name == "nt" else "clear")
        print(center(f"""\n\n

~ Discord Nitro Generator ~

github.com/xHERMIS ~ pain.lol

\n\n
              """).replace('█', Fore.CYAN + "█" + Fore.RESET).replace('~', Fore.CYAN + "~" + Fore.RESET).replace('-', Fore.CYAN + "-" + Fore.RESET))

    def printer(self, color, status, code):
        threading.Lock().acquire()
        print(f"{color} {status} > {Fore.RESET}discord.gift/{code}")

    def proxies_count(self):
        proxies_list = 0
        proxies_file_path = os.path.join('assets', 'proxies.txt')
        try:
            with open(proxies_file_path, 'r') as file:
                proxies = [line.strip() for line in file]

            for _ in proxies:
                proxies_list += 1

        except FileNotFoundError:
            pass  # Handle the case where the file is not found

        return int(proxies_list)

class Worker():
    def __init__(self, use_proxy, use_webhook):
        self.use_proxy = use_proxy
        self.use_webhook = use_webhook

    def random_proxy(self):
        proxies_file_path = os.path.join('assets', 'proxies.txt')
        with open(proxies_file_path, 'r') as f:
            proxies = [line.strip() for line in f]

        return random.choice(proxies)

    def config(self, args, args2=False):
        config_file_path = os.path.join('assets', 'config.json')
        try:
            with open(config_file_path, 'r') as conf:
                data = json.load(conf)

            if args2:
                return data[args][args2]
            else:
                return data[args]

        except FileNotFoundError:
            return None  # Handle the case where the file is not found

    def check_proxies(self):
        # Check if at least one proxy is available
        if self.use_proxy:
            proxies_file_path = os.path.join('assets', 'proxies.txt')
            with open(proxies_file_path, 'r') as f:
                proxies = [line.strip() for line in f]

            if not proxies:
                print("No proxies available. Please add working proxies to the proxies.txt file.")
                input("Press Enter to exit.")
                exit()

        # Check if using webhook and verify the necessary details
        if self.use_webhook:
            webhook_url = self.config("webhook", "url")
            if not webhook_url:
                print("Please add your webhook details to the config.json file and try again.")
                input("Press Enter to exit.")
                exit()


    def run(self):
        self.code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
        try:
            proxies = None
            if self.use_proxy:
                proxies = {'http': self.config("proxies") + '://' + self.random_proxy(),
                           'https': self.config("proxies") + '://' + self.random_proxy()}

            req = requests.get(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{self.code}?with_application=false&with_subscription_plan=true',
                proxies=proxies, timeout=5)  # Change the timeout to a longer value, e.g., 5 seconds

            if req.status_code == 200:
                Console().printer(Fore.LIGHTGREEN_EX, " Valid ", self.code)
                open('results/hit.txt', 'a+').write(self.code + "\n")
                if self.use_webhook:
                    try:
                        requests.post(self.config("webhook", "url"),
                                      json={"content": f"||@here|| **__New Valid Nitro !!__**\n\nhttps://discord.gift/{self.code}",
                                            "username": self.config("webhook", "username"),
                                            "avatar_url": self.config("webhook", "avatar")})
                    except:
                        print("Failed to send to webhook. Please check your webhook configuration.")

            elif req.status_code == 404:
                Console().printer(Fore.LIGHTRED_EX, "Invalid", self.code)
            elif req.status_code == 429:
                print(f"{Fore.LIGHTYELLOW_EX} Retry - Rate Limited - Status Code: {req.status_code} {Fore.RESET}")
                # rate = (int(req.json()['retry_after']) / 1000) + 1
                # time.sleep(rate)
            else:
                print(f"{Fore.LIGHTYELLOW_EX} Retry - Unexpected Status Code: {req.status_code} {Fore.RESET}")

        except requests.exceptions.RequestException as e:
            print(f"{Fore.LIGHTYELLOW_EX} Retry - {e} {Fore.RESET}")
        except KeyboardInterrupt:
            Console().ui()
            threading.Lock().acquire()
            print(f"{Fore.LIGHTRED_EX} Stopped > {Fore.RESET}Nitro Gen Stopped by Keyboard Interrupt.")
            os.system('pause >nul')
            exit()
        except:
            print(f"{Fore.LIGHTYELLOW_EX} Retry - Unexpected Error {Fore.RESET}")

# ...


if __name__ == "__main__":
    Console().ui()
    print(" " + Fore.CYAN + str(Console().proxies_count()) + Fore.RESET + " Total proxies loaded...\n\n")

    use_proxy = input("Do you want to use a proxy? (yes/no): ").lower() == 'yes'
    use_webhook = input("Do you want to use a webhook? (yes/no): ").lower() == 'yes'

    worker = Worker(use_proxy, use_webhook)

    # Check for working proxies and webhook details before starting worker threads
    worker.check_proxies()

    while True:
        if threading.active_count() <= int(worker.config("thread")):
            threading.Thread(target=worker.run, args=()).start()

    time.sleep(5)
    input("Press Enter to exit.")
