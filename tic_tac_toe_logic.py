import tic_tac_toe_arrays as analysis
import random as r
import tic_tac_toe_board as b
import records as rec

P1, P2, game = None, None, None


class Game:
    def __init__(self, p1, p2):
        self.players = [p1, p2]
        self.current_player = ''
        self.avail_pos = []
        self.game_record = []
        self.choice, self.winner, self.win_state = None, None, False

    def reset_pos(self):
        self.avail_pos = []
        for i in range(9):
            self.avail_pos.append(i + 1)

    def start_game(self):
        """
        Initialize the game.
        """
        for p in self.players:
            p.reset()
            if p.name == self.players[0].name:
                p.opponent = self.players[1].name
            else:
                p.opponent = self.players[0].name
        self.reset_pos()
        self.choice, self.winner, self.win_state = None, None, False
        self.game_record = []
        self.current_player = r.choice(self.players)
        if self.current_player.name == 'CPU':
            self.current_player.take_turn(self)
            b.replace_button(b.btnDict[f'btn{self.choice}'])
            self.update(self.choice)

    def change_player(self):
        """
        Change the current choosing player.
        """
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
            if self.current_player.name == 'CPU':
                if len(self.avail_pos) > 0:
                    self.current_player.take_turn(self)
                    b.replace_button(b.btnDict[f'btn{self.choice}'])
                    self.update(self.choice)
        else:
            self.current_player = self.players[0]

    def update(self, pos):
        self.current_player.update(pos)
        self.game_record.append(pos)
        self.avail_pos.remove(pos)
        self.win_cond(self.current_player)
        if self.winner is None:
            self.change_player()

    def win_cond(self, pl):
        for o in analysis.win_oc:
            count = 0
            for p in pl.positions:
                if p in o:
                    count += 1
            if count == 3:
                self.winner = pl
                self.win_state = True
        if (self.win_state is True) or (len(self.avail_pos) == 0):
            self.end_game()

    def end_game(self):
        for p in self.players:
            if self.winner is None:
                p.result = 3
            elif p.name == self.winner.name:
                p.result = 1
            else:
                p.result = 2
        if self.win_state is True:
            for a in self.avail_pos:
                b.replace_button(b.btnDict[f'btn{str(a)}'])
        rec.playerStats.update_records()


class Player:
    def __init__(self, name, sym):
        self.positions = []
        self.sym = sym
        self.name = name
        self.result = 0
        self.opponent = None
        self.stats = {'Overall': [0, 0, 0]}

    def update(self, pos):
        """
        Log the player's last choice in their tracker and remove it from the available positions board list
        :param pos: the choice that the current player made
        """
        self.positions.append(pos)

    def reset(self):
        """
        Clear the player's position tracker
        """
        self.positions.clear()
        self.opponent = None

    def reset_stats(self):
        self.stats = {'Overall': [0, 0, 0]}


class AI(Player):
    def __init__(self, name, sym):
        super().__init__(name, sym)
        self.w_dict = {}
        self.win_arr = analysis.win_arr
        self.choice = 0
        self.reset_w_dict()
        self.difficulty = b.vBar.get()

    def reset_w_dict(self):
        for p in range(10):
            self.w_dict[p] = 0

    def take_turn(self, g):
        self.choice = 0
        self.analyze_board(g)
        if self.choice == 0:
            self.choice = r.choice(g.avail_pos)
        g.choice = self.choice

    def best_opt(self, g):
        opts = self.positions + g.avail_pos
        for opt in opts:
            for op in opts:
                if self.win_arr[opt - 1][op - 1] != 0:
                    self.w_dict[int(self.win_arr[opt - 1][op - 1])] += 1

        for p in self.w_dict:
            if p in g.avail_pos:
                if self.w_dict[p] > self.w_dict[self.choice]:
                    self.choice = p
        self.reset_w_dict()

    def analyze_board(self, g):
        if (((self.difficulty == 1) and (r.randint(0, 100) > 70))
                or ((self.difficulty == 2) and (r.randint(0, 100) > 40))
                or ((self.difficulty == 3) and (r.randint(0, 100) > 10))):
            self.best_opt(g)
            self.check_win(P1, g)
            self.check_win(self, g)

    def check_win(self, pl, g):
        for p1 in pl.positions:
            for p2 in pl.positions:
                if p1 != p2:
                    if int(self.win_arr[p1 - 1][p2 - 1]) in g.avail_pos:
                        self.choice = int(self.win_arr[p1 - 1][p2 - 1])


def set_user():
    global P1
    P1 = Player(b.userName, "X")


def start_game(btn):
    global P1, P2, game
    if btn == 0:
        P2 = AI('CPU', 'O')
    elif btn == 1:
        P1 = Player(b.oppoName, 'O')
    game = Game(P1, P2)
    game.start_game()
