import random
import argparse
import time
from threading import Timer
import sys

random.seed(0)


class ExceptionforOne(Exception):
    pass


class Die:

    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        self.value = random.randint(1, 6)
        if self.value == 1:
            raise ExceptionforOne

        return self.value

    def __str__(self):
        return "Rolled " + str(self.value) + "."


class Box:

    def __init__(self):
        self.value = 0

    def setToZero(self):
        self.value = 0

    def addValue(self, value_of_dice):
        self.value += value_of_dice


class Player(object):

    def __init__(self, name=None):
        self.name = name
        self.score = 0

    def add_score(self, player_score):

        self.score += player_score

    def __str__(self):

        return str(self.name) + ": " + str(self.score)


class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    def keep_rolling(self, box):

        human_decision = self.choices("  r - Roll again, h - Hold? ")
        if human_decision == "r":
            return True
        else:
            return False

    def choices(self, prompt='Please enter a Choice: '):

        while True:
            choice = (input(prompt))
            if (choice != "r" and choice != "h"):
                print("Enter a valid choice")
            else:
                break
        return choice


class ComputerPlayer(Player):

    def __init__(self, number):

        name = 'Computer Player {}'.format(number + 1)

        super(ComputerPlayer, self).__init__(name)

    def keep_rolling(self, box):

        if 100 - self.score < 25:
            print("Computer Player will hold.")
            return False
        else:
            print("Computer Player will roll again.")
            return True


class Play:
    def __init__(self, humanPlayers, computerPlayers):

        self.players = []

        for i in range(humanPlayers):
            player_name = input('Player {}, enter your name: '.format(i + 1))
            self.players.append(HumanPlayer(player_name))
        for i in range(computerPlayers):
            self.players.append(ComputerPlayer(i))

        print(self.players)

        self.no_of_players = len(self.players)

        self.die = Die()
        self.box = Box()

    def firstPlayer(self):
        self.current_player = 0 % self.no_of_players

    def nextPlayer(self):
        self.current_player = (self.current_player + 1) % self.no_of_players

    def previousPlayer(self):
        self.current_player = (self.current_player - 1) % self.no_of_players

    def get_all_scores(self):

        return ', '.join(str(player) for player in self.players)

    def startGame(self):
        self.firstPlayer()
        # print(self.players.score)

        while all(player.score < 100 for player in self.players):
            print('\n Current score > {}'.format(self.get_all_scores()))
            self.box.setToZero()

            print("-------{} First Roll------  ".format(self.players[self.current_player].name))
            while self.keep_rolling():
                pass

            self.players[self.current_player].add_score(self.box.value)
            self.nextPlayer()

        self.previousPlayer()
        print(' {} Wins!! Congrats!! '.format(self.players[self.current_player].name).center(70, '*'))

    def keep_rolling(self):
        try:
            value_of_dice = self.die.roll()
            self.box.addValue(value_of_dice)
            print('Last roll: {}, New Turn Total: {}'.format(value_of_dice, self.box.value))

            # do you want to keep rolling?
            return self.players[self.current_player].keep_rolling(self.box)

        except ExceptionforOne:
            print('Oops, Rolled a one. Changing Player')
            self.box.setToZero()
            return False


class TimeGameProxy(Play):
    def __init__(self, humanPlayers, computerPlayers):
        self.timer = time.time()
        super(TimeGameProxy, self).__init__(humanPlayers, computerPlayers)
        self.timeleft = 60

    def playgame(self):
        self.firstPlayer()

        if self.timeleft == 60:
            self.countdown()

        if self.timeleft > 0:
            while all(player.score < 100 for player in self.players):
                print('\n Current score > {}'.format(self.get_all_scores()))
                self.box.setToZero()

                print("-------{} First Roll------  ".format(self.players[self.current_player].name))
                while self.keep_rolling():
                    pass

                self.players[self.current_player].add_score(self.box.value)
                self.nextPlayer()

            self.previousPlayer()
            print(' {} Wins!! Congrats!! '.format(self.players[self.current_player].name).center(70, '*'))
        else:
            print("end game")

    def countdown(self):
        if self.timeleft > 0:
            self.timeleft -= 1

            timer = Timer(1, self.countdown).start()
        else:

            print("\n ----------------- Time has ended! ----------------")

            self.endGame()

    def endGame(self):
        # sys.exit("One minute has elapsed. Exiting Game")

        winner = 0
        maximum = 0
        for player in self.players:
            if maximum <= player.score:
                winner_name = player.name
        print("The winner is {}".format(winner_name))
        quit()


def main():
    # Initialize parser
    commandParser = argparse.ArgumentParser(description="Send a ­­url parameter to the script")
    # add parameter for file
    commandParser.add_argument("--player1", type=str, help="Number of Human players")
    commandParser.add_argument("--player2", type=str, help="Number of Computer players")
    commandParser.add_argument("--timed", action='store_true', help="Timer function")
    args = commandParser.parse_args()

    human_players = int(args.player1)  # no of human players
    computer_players = int(args.player2)  # no of computer players

    if args.timed:
        start = TimeGameProxy(human_players, computer_players)
        start.playgame()
    else:
        startGame = Play(human_players, computer_players)
        startGame.startGame()


if __name__ == '__main__':
    main()
