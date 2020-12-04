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
# 1. The server creates a socket and binds to ‘localhost’ and port xxxx
# 2. The server then listens for a connection
# 3. When connected, the server calls recv to receive data
# 4. The server prints the data, then prompts for a reply
# 5. If the reply is /q, the server quits
# 6. Otherwise, the server sends the reply
# 7. Back to step 3
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

# constants to hold host, port and data
HOST = '127.0.0.1'
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


def chat_server():
    """
        This function runs when the user has selected to run the chat client/server version
        of the code. The function created makes connections and displays them once connected
        The function then waits for the client to send a message. If the message was that the
        client is quitting then the server closes its sockets and quits as well. Otherwise it
        displays the client's message and then gets input for its own message. If the user decides
        to quit the server, the the server sends the quit message to the client and then closes its
        own sockets and exits. Otherwise the message is sent over to the client.
        :return:
        """
    # variable to control initial message output to match PDF sample
    first_message = True

    try:
        # learned how to create socket from: https://docs.python.org/3/howto/sockets.html
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow socket re-use - obtained from assignment PDF
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # socket object creation. catch any failure and exit if failed
    except socket.error:
        print("Error creating socket! EXITING PROGRAM!!")
        sys.exit(1)

    else:

        # bind the socket
        s.bind((HOST, PORT))

        # listen for connections to server. only allowing one
        s.listen(1)

        # display server host and port
        print(f"Server listening on: {HOST} on port: {PORT}")

        while True:
            # create the connection to the client
            client_connection, client_address = s.accept()

            # verify connection details between server and client
            print(f"Connected by {client_address}")
            print("Waiting for message...")

            # partially inspired from https://www.geeksforgeeks.org/socket-programming-python/
            # continue accepting connections while server code is running
            while True:
                try:
                    client_message = receive_data(client_connection)

                except socket.error:
                    print("Unable to receive data on this socket!")
                    sys.exit(1)

                else:

                    # if the client had chosen to quit then close the sockets and end program
                    if client_message == '/q':
                        client_connection.close()
                        s.close()
                        sys.exit(0)

                    # otherwise show what the client sent over
                    print(client_message)

                    # formatting to match PDF output
                    if first_message:
                        print("Type /q to quit")
                        print("Enter a message to send...")
                        first_message = False

                    # get input from user for server message
                    print(">", end='')
                    server_msg = input()

                    try:
                        # send the message over to the client
                        send_data(client_connection, server_msg)

                    except socket.error:
                        print("Unable to send data on this socket!")
                        sys.exit(1)

                    # if user chose to quit server, then close sockets and end program
                    if server_msg == '/q':
                        client_connection.close()
                        s.close()
                        sys.exit(0)


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
        print("\nPlease enter '1 - 9' to place O marker")
        print("Type /q to quit")
        print(">", end='')
        server_msg = input()

        # do not allow non-integer responses
        if not server_msg.isnumeric():

            # if the message was quit, allow this only
            if server_msg == '/q':
                break

            # otherwise reject the input, display error message and loop again
            print("INPUT ERROR: You must enter a valid integer from '1 - 9'!")
            continue

        # if the value was actually a number check that it is in acceptable range
        elif int(server_msg) < 1 or int(server_msg) > 9:
            print("INPUT ERROR: Your integer selection can only be from 1 - 9!")
            continue

        # now check that cell is not already taken
        elif player.board_game[int(server_msg)] != '     ':
            print("That game position is already occupied. Choose again")

        # input assumed good and ok to continue
        else:
            break

    return server_msg


def run_game():
    """
        This function handles the game of the client/server program. The function first
        creates an object of Game which it will use to access the Game board and the
        class data members. Next the function creates sockets and makes connections and
        displays them. It then displays the current round number and then obtains the client's
        message. If the client had wanted to quit, then close sockets and end program. Otherwise,
        update client's move and check if game is over via win or draw and display the board. If
        the game is over, then send quit message to client and display output and close server.
        Otherwise get/validate input for the server's move and check if user wanted to quit.
        If the user wanted to quit server, let the client know and then close sockets and end
        program. Otherwise update the server's move on the board, send move to client and then
        check for game being over.
        :return:
        """
    player = Game()

    try:
        # learned how to create socket from: https://docs.python.org/3/howto/sockets.html
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allow socket re-use - obtained from assignment PDF
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    except socket.error:
        print("Error creating socket! EXITING PROGRAM!!")
        sys.exit(1)

    else:
        # bind the socket
        s.bind((HOST, PORT))

        # listen for connections to server. only allowing one
        s.listen(1)

        # display server host and port
        print(f"Server listening on: {HOST} on port: {PORT}")

        while True:
            # create the connection to the client
            client_connection, client_address = s.accept()

            # verify connection details between server and client
            print(f"Connected by {client_address}")
            player.game_rules()

            # partially inspired from https://www.geeksforgeeks.org/socket-programming-python/
            # continue accepting connections while server code is running
            while True:
                # show current round number
                global ROUND
                print("\n")
                print("#" * 15 + f" ROUND: {ROUND} " + "#" * 15)

                # increment variable for next round number
                ROUND += 1

                print("\nWaiting for opponent's move...")

                try:
                    # call function to receive data from client
                    client_message = receive_data(client_connection)

                except socket.error:
                    print("Unable to receive data on this socket!")
                    sys.exit(1)

                else:

                    # if the client had chosen to quit then close sockets and end program
                    if client_message == '/q':
                        client_connection.close()
                        s.close()
                        sys.exit(0)

                    # otherwise update board to reflect opponents move and print it out
                    player.make_move(int(client_message), 'X')
                    player.show_board()

                    # check if game is over
                    player.check_game("  X  ")

                    # if the game is over then quit and close server
                    if player.game_over:
                        client_connection.close()
                        s.close()
                        sys.exit(0)

                    # otherwise prompt for and perform input validation
                    server_msg = validate_input(player)

                    # if server user had chosen to quit let client know & close sockets and end program
                    if server_msg == '/q':
                        send_data(client_connection, server_msg)
                        client_connection.close()
                        s.close()
                        sys.exit(0)

                    # update board to reflect player's move and print it out
                    player.make_move(int(server_msg), 'O')
                    player.show_board()

                    # check for a win
                    player.check_game("  O  ")

                    try:
                        # send the move over to the opponent
                        send_data(client_connection, server_msg)

                    except socket.error:
                        print("Unable to send data on this socket!")
                        sys.exit(1)

                    # if the game is over then quit and close server
                    if player.game_over:
                        client_connection.close()
                        s.close()
                        sys.exit(0)


# main program to handle input validation and check to run chat or game version
if __name__ == "__main__":
    while True:
        print("Would you like to chat or play Tic Tac Toe?")
        response = input('Enter "chat" or "game" and press enter: ')

        if response == "chat":
            chat_server()
            break

        elif response == "game":
            run_game()
            break

        else:
            print('INVALID INPUT: You must enter either "chat or "game')
            continue
