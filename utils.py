import socket
import sys
from colorama import Back, Fore, Style

closing_statements = ['bye', 'close', 'exit']


def validate_ip(ip):
    """Validate IP address format."""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def validate_port(port):
    """Validate port number."""
    return 1024 <= port <= 65535


def receive_messages(sock, chat_log):
    """Continuously receive and display messages."""
    while True:
        try:
            message = sock.recv(4096).decode('utf-8')
            if any(statement in message.lower() for statement in closing_statements):
                print(
                    "\n" + Back.RED + Fore.WHITE + "Connection closed." + Style.RESET_ALL
                )
                break
            if message:  # Only print if the message is not empty
                print(
                    f"\n{Back.GREEN}{Fore.WHITE}Partner:{Style.RESET_ALL} {message}",
                    end=''
                )
                chat_log.append(f"Partner: {message}")

        except Exception as e:
            print(
                f"\n{Back.RED}{Fore.WHITE}Error receiving message: {e}{Style.RESET_ALL}"
            )
            break
    sock.close()


def send_messages(sock):
    """Continuously send messages based on user input."""
    while True:
        try:
            msg = input(f"\n{Back.RED}{Fore.WHITE}Me:{Style.RESET_ALL} ")
            if msg:  # Only send if the message is not empty
                sock.send(str.encode(msg))
                if any(statement in msg.lower() for statement in closing_statements):
                    print(
                        "\n" + Back.RED + Fore.WHITE + "Closing connection as requested."
                        + Style.RESET_ALL
                    )
                    break
        except Exception as e:
            print(
                f"\n{Back.RED}{Fore.WHITE}Error sending message: {e}{Style.RESET_ALL}"
            )
            break
    sock.close()


def main_menu():
    """Display the main menu to choose host, connect, or close the program."""
    while True:
        try:
            choice = int(
                input("\tDo you want to host (1), connect (2), or close the program (3): ")
            )
            if choice in (1, 2, 3):
                return choice
            else:
                raise ValueError("Invalid choice")
        except ValueError:
            print(
                "\n" + Back.RED + Fore.WHITE + " Invalid choice. Please try again. "
                + Style.RESET_ALL
            )
        except KeyboardInterrupt:
            print("\n\tExiting program...")
            sys.exit()
        except EOFError:
            print("\n\tExiting program...")
            sys.exit()
