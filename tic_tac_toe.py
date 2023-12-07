from ArrGen import win_arr, winning_outcomes_base
import time
import random


class Board:
    def __init__(self, player_1, player_2):
        self.positions = list(x for x in range(10))     # generate a list 1-9 for board positions
        self.pos_dict = {}
        self.player_choice = "-"
        self.win_state = False
        self.move_tracker = []      # Tracks every move made, in order, during the game. TODO: Use in analysis
        self.pos_remaining = []     # Track the positions available for play
        self.players = [player_1, player_2]
        self.current_player = self.players[random.randint(0, 1)]    # Set starting player randomly upon initialization
        self.winner = "-"
        self.tie_state = False

    def init_pos_dict(self, d: dict):
        """
        Upon initialization of the game board, populate the given dictionary with
            key:value pairs -> (k (int 1-9) : v (str(1-9)).
        These values will be used as tile indicators in print_board
        :param d: the dictionary to populate (self.pos_dict)
        """
        for num in self.positions:
            d[num] = f"{num}"

    def print_board(self):
        """
        print a game board
        Available tiles will be shown as integers, occupied tiles will have the occupying player's symbol
        position depictions are stored and retrieved from self.pos_dict
        """
        print(
            f"\n {self.pos_dict[1]} | {self.pos_dict[2]} | {self.pos_dict[3]} "
            f"\n {self.pos_dict[4]} | {self.pos_dict[5]} | {self.pos_dict[6]} "
            f"\n {self.pos_dict[7]} | {self.pos_dict[8]} | {self.pos_dict[9]} "
            )

    def start_game(self):
        """
        Initialize the game.
        """
        for pos in range(9):                            # Fill the list of available positions
            self.pos_remaining.append(str(pos + 1))
        self.init_pos_dict(self.pos_dict)               # Initialize the game board
        # Introduce the players and their symbols
        print(f"{self.players[0].name} is '{self.players[0].pos_symbol}'s, "
              f"{self.players[1].name} is '{self.players[1].pos_symbol}'s")
        self.print_board()                              # Show the starting board
        # Determine if the user or the AI is the starting player and allow for user input or have the AI choose
        if self.current_player == self.players[0]:
            print(f"\n{self.current_player.name}, please make the first move by entering a number on the board")
            self.player_choice = input("> ")
            self.update_player_position()
        else:
            print("CPU is thinking...")
            time.sleep(1)
            self.current_player.take_turn(self)

    def update_player_position(self):
        """
        Using the current player's choice, determine whether to quit the game or to place the player's move on the board
        """
        if self.player_choice == 'quit':
            self.update_board()
        else:
            self.current_player.update_positions(self.player_choice, self)      # Log the move in the player's tracker
            self.pos_dict[int(self.player_choice)] = self.current_player.pos_symbol     # change the symbol on the board
            self.move_tracker.append(self.player_choice)        # Log the move in the overall game tracker
        self.check_win_condition(self.current_player)       # Check to see if the move resulted in a win
        self.change_cur_player()        # Change the current player
        self.update_board()     # Update the board

    def update_board(self, msg=None):
        """
        If the prior move resulted in a win, tie, or neither, take the appropriate action
        :param msg: message to print when requested
        """
        while self.player_choice != "quit":
            if self.winner != "-":          # If there is a winner, then print the final board and request another game
                print(f"{self.winner.name} is the winner!")
                self.print_board()
                self.run_it_back()
            elif self.tie_state:            # If there is a tie, then print the final board and request another game
                print("Game ended in a tie")
                self.print_board()
                self.run_it_back()
            elif self.current_player.name == self.players[0].name:
                if msg:
                    print(msg)
                print(f"{self.current_player.name},Please make your next move")
                self.print_board()
                self.player_choice = input("> ")
                if self.player_choice in self.move_tracker:
                    self.update_board('Your previous choice is unavailable')
                elif int(self.player_choice) not in self.positions:
                    self.update_board('Your previous choice was invalid')
                else:
                    self.update_player_position()
            else:
                print("CPU is thinking...")
                time.sleep(1)
                self.current_player.take_turn(self)

    def change_cur_player(self):
        """
        Change the current choosing player.
        """
        if self.current_player.name == self.players[0].name:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def check_win_condition(self, player):
        """
        Check if the given player has won. If there are no positions left and no winner, declare tie.
        :param player: player whose played positions will be checked
        """
        win = 0
        for comb in winning_outcomes_base:   # Iterate over the possible winning combinations
            for num in player.played_pos:       # Check player's positions against each winning combo
                if int(num) in comb:
                    win += 1
                    if win == 3:
                        self.winner = player
            win = 0
        if self.winner == "-":
            if len(self.pos_remaining) == 0:
                self.tie_state = True

    def run_it_back(self):
        """
        Check if the user would like another game and either reset conditions or quit the program
        """
        self.player_choice = input("Would you like to play again? Y/N > ")
        if self.player_choice == "Y" or "y":
            self.reset_game()
            self.start_game()
        else:
            self.player_choice = "quit"

    def reset_game(self):
        """
        Reset the game attributes to those required by the starting conditions to run the game
        """
        self.positions = list(x for x in range(10))
        self.pos_dict = {}
        self.player_choice = "-"
        self.win_state = False
        self.move_tracker = []
        self.pos_remaining = []
        self.winner = "-"
        self.tie_state = False
        for p in self.players:
            p.reset_pos()


class Player:
    def __init__(self, symbol, name):
        self.played_pos = []
        self.pos_symbol = symbol
        self.name = name

    def update_positions(self, pos, board):
        """
        Log the player's last choice in their tracker and remove it from the available positions board list
        :param pos: the choice that the current player made
        :param board: the game board
        """
        self.played_pos.append(int(pos))
        board.pos_remaining.remove(board.player_choice)

    def reset_pos(self):
        """
        Clear the player's position tracker
        """
        self.played_pos.clear()


class AI(Player):
    def __init__(self, symbol, name):
        super().__init__(symbol, name)
        self.options = {}
        self.fill_options()
        self.choice = 0

    def fill_options(self):
        """
        Set the values in the options dictionary to 0
        """
        for r in range(0, 10):
            self.options[str(r)] = 0

    def analyze_options(self, board):
        """
        Using the available positions that may be played and the AIs positions already played, decide which option
            affords the highest number of possible remaining win combinations.
        :param board: The game board
        """
        tot_opts = self.played_pos + board.pos_remaining
        for r_ind in tot_opts:
            r = int(r_ind) - 1
            for c_ind in tot_opts:
                c = int(c_ind) - 1
                # Using the winning combos array, lookup the value which would result in a win condition and
                # increment the corresponding value in the options' dictionary.
                # Refer to ArrGen.py to view the lookup table
                if not win_arr[r][c] == "na":
                    if win_arr[r][c] in board.pos_remaining:
                        self.options[win_arr[r][c]] += 1

    def analyze_win(self, board, player):
        """
        If either the AI or the user have a possible winning combination on the next move, choose that position
        :param board: the game board
        :param player: the player to be checked for a win condition
        """
        if len(player.played_pos) > 1:
            for r_ind in player.played_pos:
                r = int(r_ind) - 1
                for c_ind in player.played_pos:
                    c = int(c_ind) - 1
                    if not win_arr[r][c] == "na":
                        if win_arr[r][c] in board.pos_remaining:
                            self.choice = int(win_arr[r][c])

    def choose_pos(self, board):
        """
        AI choosing the best option.
        Preferential order(lowest to highest): option with most win combos remaining, option that prevents user from winning,
            option that results in the AI winning.
        :param board: the game board
        """
        # choose option with the highest possible number of win combinations.
        for k in self.options:
            if self.options[k] > self.options[str(self.choice)]:
                self.choice = int(k)
        # If there are no more winning combinations available, choose from remaining positions at random
        if self.choice == 0:
            self.choice = board.pos_remaining[random.randint(0, len(board.pos_remaining) - 1)]
        # Choose option that would prevent user from winning
        self.analyze_win(board, board.players[0])
        # choose option that would result in AI winning
        self.analyze_win(board, board.players[1])
        print(f"CPU choice: {self.choice}")
        board.player_choice = str(self.choice)
        # Reset choice and options dictionary
        self.choice = 0
        self.fill_options()
        board.update_player_position()

    def take_turn(self, board):
        """
        Analyze the best possible options and choose the best option available
        :param board: the game board
        """
        self.analyze_options(board)
        self.choose_pos(board)


CPU = AI("C", "CPU")
player1 = Player("X", "Player1")

GameBoard = Board(player1, CPU)
GameBoard.start_game()
