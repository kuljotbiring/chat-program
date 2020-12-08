# *******************************************************************************************
# Kuljot Biring
# Project 4
# May 31, 2020
# CS 372 Spring 2020
#
# EXTRA CREDIT
# Turn your client-server into a multi-player ascii game. Tic-tac-toe? Hangman? The choice
# is up to you. Points awarded subjectively based on effort. Max points possible tbd.
#
# I have chosen to create a tic tac toe board game
# *******************************************************************************************


class Game:
    """Class to make Tic Tac Toe Game"""

    def __init__(self):
        """
        Class constructor which sets up initial board game as a dictionary with empty board slots as values
        and using numbers as keys. Constructor sets up a boolean to false which holds finish state of game
        """
        self.board_game = {1: '     ', 2: '     ', 3: '     ', 4: '     ', 5: '     ', 6: '     ', 7: '     ',
                           8: '     ', 9: '     '}

        self.game_over = False

    def game_rules(self):
        """ This function show the game rules and how to select position on the board to play.
        This function is called once in the beginning if the user chooses to play game"""

        # create a dictionary with values to represent indices. The keys themselves will be used to
        # access the values and board game positions desired by the plaer
        index_board = {1: '  1  ', 2: '  2  ', 3: '  3  ', 4: '  4  ', 5: '  5  ', 6: '  6  ', 7: '  7  ',
                      8: '  8  ', 9: '  9  '}

        # display rules
        print("\n")
        print("*" * 15 + " TIC TAC TOE " + "*" * 15)
        print("Each player chooses an index '1 through 9' to place their symbol 'X' or 'O'\n"
              "on the game board. You may not choose a game board position already taken\n"
              "The first player to get their symbol connected in a row wins!")

        # iterate through dictionary and print out items and line separators
        print("______________________")
        for index, value in index_board.items():
            if index == 1 or index == 4 or index == 7:
                print("|", end="")

            print(value, end="")
            print(" |", end="")

            # check if line separator should be placed for every 3 dictionary value outputs
            if index % 3 == 0:
                print("\n|______|______|______|")

    def show_board(self):
        """
        This function prints out the dictionary in the format of a tic tac toe board and
        places ascii chars to represent borders creating scaffolding for the board game
        """
        print("\n")
        print("     TIC TAC TOE     ")
        print("______________________")

        # iterate through dictionary and print out items and line separators
        for index, value in self.board_game.items():
            if index == 1 or index == 4 or index == 7:
                print("|", end="")

            print(value, end="")
            print(" |", end="")

            # check if line separator should be placed for every 3 dictionary value outputs
            if index % 3 == 0:
                print("\n|______|______|______|")

    def make_move(self, key, player):
        """
        Function take in parameters for the key and a string. The key is used to access the dictionary
        and place the string player into the value mapped by the key selected. Function ensures position
        on board is empty first. The main program also has a validator function to ensure overwritting
        taken board positions does not occur
        """
        if self.board_game[key] == '     ':
            self.board_game[key] = f"  {player}  "

    def check_game(self, symbol):
        """
        This function checks if the game is finished by getting the symbol to check and looking at all the
        possible win combinations to see if the same symbol shows up in them. If any of these conditions is
        true, the boolean of the class which indicates game is finished is set to true. If none of these
        conditions exist, then the function loops through the dictionary and counts the number of spots which
        are taken. If all of the spots are taken and no win condition was triggered, the function identifies
        this as a draw game
        :param symbol:
        :return:
        """
        # array to hold outcomes of possible win scenarios
        win_condition = []

        # check the possible combination of wins if the same symbol is in each position

        # check top row and add True/Falso result to array
        top_win = self.board_game[1] == self.board_game[2] == self.board_game[3] == symbol
        win_condition.append(top_win)

        # check middle row and add True/False result to array
        mid_win = self.board_game[4] == self.board_game[5] == self.board_game[6] == symbol
        win_condition.append(mid_win)

        # check bottom row and add True/False result to array
        bottom_win = self.board_game[7] == self.board_game[8] == self.board_game[9] == symbol
        win_condition.append(bottom_win)

        # check left column and add True/False result to array
        left_win = self.board_game[1] == self.board_game[4] == self.board_game[7] == symbol
        win_condition.append(left_win)

        # check center column and add True/False result to array
        center_win = self.board_game[2] == self.board_game[5] == self.board_game[8] == symbol
        win_condition.append(center_win)

        # check right column and add True/False result to array
        right_win = self.board_game[3] == self.board_game[6] == self.board_game[9] == symbol
        win_condition.append(right_win)

        # check left diagonal and add True/False result to array
        lr_win = self.board_game[1] == self.board_game[5] == self.board_game[9] == symbol
        win_condition.append(lr_win)

        # check right diagonal and add True/False result to array
        rl_win = self.board_game[3] == self.board_game[5] == self.board_game[7] == symbol
        win_condition.append(rl_win)

        # verify if any of these conditions occurred and set variable true if they did
        for condition in win_condition:
            if condition:
                # display output message showing who won
                print("\n")
                print("*" * 15 + f" PLAYER {symbol} WINS!!: " + "*" * 15)
                print("\n")
                self.game_over = True
                break

        # check for draw games
        else:
            tiles_taken = 0

            # count up all the tiles with a player symbol in them
            for space in self.board_game.values():
                if space != '     ':
                    tiles_taken += 1

            # if all tiles are filled up then game is over - set variable to true
            if tiles_taken == 9:
                print("\n")
                print("*" * 15 + " DRAW! TIE GAME!!: " + "*" * 15)
                print("\n")
                self.game_over = True
