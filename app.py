#!/usr/bin/env python3

import sys

from server_client import start_server, start_client
from utils import main_menu

if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == 3:
            print("\n\tExiting program...")
            sys.exit()

        if choice == 1:
            start_server()
        elif choice == 2:
            start_client()
