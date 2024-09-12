import socket
import sys
import threading
import logging
from utils import validate_ip, validate_port, receive_messages, send_messages
from colorama import Back, Fore, Style

logging.basicConfig(
    filename='chat_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def start_server():
    """A function that starts a server host."""
    ip = input(
        "\tEnter the preferred IP address (preferably your public IP): "
    )
    if not validate_ip(ip):
        print(
            "\n" + Back.RED + Fore.WHITE +
            " Invalid IP address. Exiting." + Style.RESET_ALL
        )
        sys.exit()
    port = int(input("\tEnter the port number (1024-65535): "))
    if not validate_port(port):
        print(
            "\n" + Back.RED + Fore.WHITE +
            " Invalid port number. Exiting." + Style.RESET_ALL
        )
        sys.exit()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((ip, port))
        server.listen()
        print(f"\n\tWaiting for a new connection with IP: {ip}:{port} ....")
        client, address = server.accept()
        print(
            f"\n\t{Back.YELLOW}{Fore.WHITE} Connection from "
            f"{address[0]}:{address[1]} established{Style.RESET_ALL}"
        )
        client.send(str.encode("Welcome!"))

        receive_thread = threading.Thread(
            target=receive_messages, args=(client, [])
        )
        send_thread = threading.Thread(
            target=send_messages, args=(client,)
        )
        receive_thread.start()
        send_thread.start()
        receive_thread.join()
        send_thread.join()

        logging.info(f"Connection with {address[0]}:{address[1]} closed.")
        server.close()

    except socket.error as e:
        print(
            f"\n{Back.RED}{Fore.WHITE}Socket error: {e}{Style.RESET_ALL}"
        )
        logging.error(f"Socket error: {e}")
    except Exception as e:
        print(
            f"\n{Back.RED}{Fore.WHITE}Unexpected error: {e}{Style.RESET_ALL}"
        )
        logging.error(f"Unexpected error: {e}")


def start_client():
    """A function that connects to a server as a client."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input("\nEnter the IP address of the host: ")
    if not validate_ip(ip):
        print(
            "\n" + Back.RED + Fore.WHITE +
            " Invalid IP address. Exiting." + Style.RESET_ALL
        )
        sys.exit()
    port = int(
        input("\nEnter the port number for the connection (1024-65535): ")
        )
    if not validate_port(port):
        print(
            "\n" + Back.RED + Fore.WHITE +
            " Invalid port number. Exiting." + Style.RESET_ALL
        )
        sys.exit()

    try:
        client.connect((ip, port))
        message = client.recv(4096).decode('utf-8')
        print(f"\n\t{Back.GREEN}{Fore.WHITE}Host:{Style.RESET_ALL} {message}")

        receive_thread = threading.Thread(
            target=receive_messages, args=(client, [])
        )
        send_thread = threading.Thread(
            target=send_messages, args=(client,)
        )
        receive_thread.start()
        send_thread.start()
        receive_thread.join()
        send_thread.join()

    except ConnectionRefusedError:
        print(
            "\n" + Back.RED + Fore.WHITE +
            "Connection refused. Please check the IP address and port."
            + Style.RESET_ALL
        )
        logging.error("Connection refused.")
    except socket.error as e:
        print(
            f"\n{Back.RED}{Fore.WHITE}Socket error: {e}{Style.RESET_ALL}"
        )
        logging.error(f"Socket error: {e}")
    except Exception as e:
        print(
            f"\n{Back.RED}{Fore.WHITE}Unexpected error: {e}{Style.RESET_ALL}"
        )
        logging.error(f"Unexpected error: {e}")
    finally:
        client.close()
