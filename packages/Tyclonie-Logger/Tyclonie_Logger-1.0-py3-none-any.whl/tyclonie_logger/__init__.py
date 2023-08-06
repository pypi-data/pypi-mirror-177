import datetime
from colorama import Fore, Back, Style, init

if __name__ != "__main__":
    init()

class TyclonieLogger:
    def __init__(self, datetime_format="%Y/%m/%d @ %H:%M:%S"):
        self.datetime_format = datetime_format

    def get_datetime_formatted(self) -> str:
        return f"{Back.YELLOW}{Fore.BLACK}{datetime.datetime.now().strftime(self.datetime_format)}{Style.RESET_ALL} | "

    def log(self, message) -> None:
        print(f"{self.get_datetime_formatted()}{Fore.GREEN}{Style.DIM}Log{Style.RESET_ALL}: {message}")

    def warn(self, message) -> None:
        print(f"{self.get_datetime_formatted()}{Fore.RED}{Style.BRIGHT}Warning{Style.RESET_ALL}: {message}")

    def error(self, message) -> None:
        print(f"{self.get_datetime_formatted()}{Back.RED}{Fore.BLACK}{Style.BRIGHT}Error{Style.RESET_ALL}: "
              f"{Fore.RED}{message}{Fore.RESET}")
