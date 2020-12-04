# ************************************************************************************
# Kuljot Biring
# Project 4
# May 31, 2020
# CS 372 Spring 2020
#
# In this coding project you will write a simple client-server program using python sockets.
# Your program will emulate a simple chat client. For extra-credit (points tbd), turn your
# chat program into a simple ascii multiplayer game (see below for spec).
#
# This chat client-server is fairly simple in design. The server doesn’t handle multiple
# clients, and there is only one socket connection made. You will reuse this socket for the
# life of the program. The one issue with reusing sockets is that there is no easy way to tell
# when you’ve received a complete communication:
#
# 1. The client creates a socket and connects to ‘localhost’ and port xxxx
# 2. When connected, the client prompts for a message to send
# 3. If the message is /q, the client quits
# 4. Otherwise, the client sends the message
# 5. The client calls recv to receive data
# 6. The client prints the data
# 7. Back to step 2
# 8. Sockets are closed (can use with in python3)
#
#
# EXTRA CREDIT
# Turn your client-server into a multiplayer ascii game. Tic-tac-toe? Hangman? The choice
# is up to you. Points awarded subjectively based on effort. Max points possible tbd.
# ************************************************************************************

import socket
import sys
from tictactoe import Game

# constants to hold host, port and round
HOST = 'localhost'
PORT = 5500
ROUND = 1


def send_data(sock, data):
    """
    This function uses sendall to send over the size of the data that the
    other side should expect. Both peices of data are sent over in bytes format
    so that they can be carried across the network
    :param sock:
    :param data:
    :return: N/A
    """
    # learned to convert int to bytes from
    # https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
    sock.sendall(len(data).to_bytes(4, byteorder='big'))
    sock.sendall(data.encode())


# partially inspired from https://docs.python.org/3/howto/sockets.html
def receive_exact(sock, msg_len):
    """
    This function handles receiving exactly the amount of data that was sent
    the function essentially continues to loop which the bytes remaining variable
    has an amount left. this amount is continually updated in the loop and chunks
    of the data sent over are grabbed and appended to an empty string which keeps
    updating and adding new data grabbed to it. I used the logic from my Project 1
    and CS344 OTP assignment to create this function
    :param sock:
    :param msg_len:
    :return: data received from other side
    """
    data_received = b''
    bytes_remaining = msg_len

    # continually grab incoming data and update amount remaining
    # while appending each new amount grabbed to current data
    while bytes_remaining > 0:
        incoming_data = sock.recv(bytes_remaining)
        data_received += incoming_data
        bytes_remaining -= len(incoming_data)

    return data_received


def receive_data(sock):
    """
    Thi function converts the size into an integer and then
    uses this size to call on the receive exact function to
    ensure all of the data sent was grabbed
    :param sock:
    :return: data from function call to receive exact
    """
    # string variable to hold data from server
    # learned to convert int to bytes from
    # https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
    msg_len = int.from_bytes(receive_exact(sock, 4), byteorder='big')
    return receive_exact(sock, msg_len).decode()


def chat_client():
    """
    This function runs when the user has selected to run the chat client/server version
    of the code. The function created makes connections and displays them once connected
    The function then sends over data to the server and then grabs a reply from the server.
    If the user requests to quit the program ends after closing its sockets. If the program
    receives a request from the server to quit it will likewise quit since the server is stopping
    :return:
    """
    try:
        # learned how to create socket from: https://docs.python.org/3/howto/sockets.html
        # socket object creation
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow socket re-use - obtained from assignment PDF
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # handle errors creating sockets
    except socket.error:
        print("Error creating socket! EXITING PROGRAM!!")
        sys.exit(1)

    # if sockets were created successfully continue
    else:

        # handle any socket error exceptions
        try:
            # connect client to the server
            s.connect((HOST, 5500))

            # display successful connection
            print(f"Connected to:  {HOST} on port: {PORT}")
            print("Type /q to quit")
            print("Enter a message to send...")

            while True:
                print(">", end='')

                # assign input string to variable
                client_message = input()

                # call function to send data
                send_data(s, client_message)

                if client_message == '/q':
                    s.close()
                    sys.exit(0)

                # call function to receive data
                server_reply = receive_data(s)

                if server_reply == '/q':
                    s.close()
                    sys.exit(0)

                # piazza post 61 hint used to use decode to format output
                # display server's reply
                print(server_reply)

        # if the socket failed for any reason display error message, close socket, exit program with 1
        # create a tuple to hold the common errors. obtained this from my own Project 1 assignment.
        except (socket.herror, socket.herror, socket.timeout, RuntimeError) as error:
            print(f"ERROR: Program has failed due to a {type(error).__name__} error!")
            s.close()
            sys.exit(1)


def validate_input(player):
    """
    This function takes as parameter a Game object and validates user entry
    The function first checks that the user has entered a number (quit command OK).
    If a number was entered then the program checks if the numbered entered is within the
    acceptable range. If the number is in range the function then checks that
    the board position requested is not already occupied by another symbol. if
    everything is good it will then return that message as a valid input
    :param player:
    :return:
    """
    while True:
        # prompt and get input from the user
        print("\nPlease enter '1 - 9' to place X marker")
        print("Type /q to quit")
        print(">", end='')
        client_message = input()

        # do not allow non-integer responses
        if not client_message.isnumeric():

            # allow quit command as only non numeric input
            if client_message == '/q':
                break

            # otherwise bad input and need to re-prompt
            print("INPUT ERROR: You must enter a valid integer from '1 - 9'!")
            continue

        # if the value was actually a number check that it is in acceptable range
        elif int(client_message) < 1 or int(client_message) > 9:
            print("INPUT ERROR: Your integer selection can only be from 1 - 9!")
            continue

        # now check that cell is not already taken
        elif player.board_game[int(client_message)] != '     ':
            print("That game position is already occupied. Choose again")

        # input assumed good and ok to continue
        else:
            break

    return client_message


def run_game():
    """
    This function handles the game of the client/server program. The function first
    creates an object of Game which it will use to access the Game board and the
    class data members. Next the function creates sockets and makes connections and
    displays them. It then displays the current round number and validates input
    entered on the client side. If the quit command was entered the program will quit
    and let the server know to quit as well. Otherwise, the position is updated with
    the client's symbol, board is shown and the game is checked if a win occurred and will
    subsequently exit and let the server know to exit as well. Otherwise data is obtained from
    the server; checked if it needs to quit - otherwise make the move on the board for the server
    and check if a win occurred.
    :return:
    """
    player = Game()

    try:
        # learned how to create socket from: https://docs.python.org/3/howto/sockets.html
        # socket object creation
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow socket re-use - obtained from assignment PDF
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # handle errors creating sockets
    except socket.error:
        print("Error creating socket! EXITING PROGRAM!!")
        sys.exit(1)

    # if sockets were created successfully continue
    else:

        # handle any socket error exceptions
        try:
            # connect client to the server
            s.connect((HOST, 5500))

            # display successful connection
            print(f"Connected to:  {HOST} on port: {PORT}")
            player.game_rules()

            while True:
                # show current round number
                global ROUND
                print("\n")
                print("#" * 15 + f" ROUND: {ROUND} " + "#" * 15)

                # increment variable for next round
                ROUND += 1

                # prompt for and perform input validation
                client_message = validate_input(player)

                # call function to send data
                send_data(s, client_message)

                # if client chose to quit, shutdown sockets and end program
                if client_message == '/q':
                    s.close()
                    sys.exit(0)

                # update board to reflect player's move and display board
                player.make_move(int(client_message), 'X')
                player.show_board()

                # check if game is over
                player.check_game("  X  ")

                # if the game is over then close sockets and exit program
                if player.game_over:
                    s.close()
                    sys.exit(0)

                print("\nWaiting for opponent's move...")

                # call function to receive data
                server_reply = receive_data(s)

                # if server chose to quit, shutdown sockets and end program
                if server_reply == '/q':
                    s.close()
                    sys.exit(0)

                # update board to reflect opponent's move and display board
                player.make_move(int(server_reply), 'O')
                player.show_board()

                # check if game is over
                player.check_game("  O  ")

                # if the game is over then close sockets and exit program
                if player.game_over:
                    s.close()
                    sys.exit(0)

        # if the socket failed for any reason display error message, close socket, exit program with 1
        # create a tuple to hold the common errors. obtained this from my own Project 1 assignment.
        except (socket.herror, socket.herror, socket.timeout, RuntimeError) as error:
            print(f"ERROR: Program has failed due to a {type(error).__name__} error!")
            s.close()
            sys.exit(1)


# main program to handle input validation and check to run chat or game version
if __name__ == "__main__":
    while True:
        print("Would you like to chat or play Tic Tac Toe?")
        response = input('Enter "chat" or "game" and press enter: ')

        if response == "chat":
            chat_client()
            break

        elif response == "game":
            run_game()
            break

        else:
            print('INVALID INPUT: You must enter either "chat or "game')
            continue
