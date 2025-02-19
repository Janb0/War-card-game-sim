
def loadConfig() -> tuple[dict, int, int, bool]:
    from json import load as loadJSON
    config = loadJSON(open('config.json', 'r'))
    cards = config['cards']
    shuffle_times = config['shuffle times']
    turns = config['turns']
    printResults = config["print results"]
    return cards, shuffle_times, turns, printResults

class Hand(list):
    def shuffle(self, times) -> None:
        from random import randint
        for _ in range(times):
            for i in range(len(self) - 1):
                rolled = randint(0, len(self) - i - 1)
                self.append(self.pop(rolled))
    def addCards(self, new_contents) -> None:
        for key in list(new_contents.keys()):
            for _ in range(new_contents[key]):
                self.append(key)

class Deck(Hand):
    def give(self) -> tuple[Hand]:
        hands = (Hand(), Hand())
        for i in range(len(self)):
            hands[i % 2].addCards({self[i] : 1})
        return hands

class Game:
    def __init__(self, hands, values) -> None:
        if len(hands) != 2: raise Exception("Wrong amount of hands. Only valid amount of hands is 2.")
        self.hands = hands
        self.wager = []
        self.comparing = ['', '']
        self.card_values = values
        self.turn = 0

    def place(self) -> None:
        try:
            self.comparing[0] = self.hands[0].pop(0)
            self.comparing[1] = self.hands[1].pop(0)
        except: pass

    def addWager(self) -> None:
        self.wager += self.comparing

    def nextTurn(self) -> None:
        self.turn += 1
        self.place()
        self.addWager()

        if self.card_values[self.comparing[0]] == self.card_values[self.comparing[1]]:
            self.place()
            self.addWager()
            self.comparing = ['', '']
        elif self.card_values[self.comparing[0]] > self.card_values[self.comparing[1]]:
            for card in self.wager:
                self.hands[0].addCards({card : 1})
            self.wager = []
        elif self.card_values[self.comparing[0]] < self.card_values[self.comparing[1]]:
            for card in self.wager:
                self.hands[1].addCards({card : 1})
            self.wager = []

    def write(self) -> None:
        print((f'-------------------- - turn {self.turn} - -----------------------------------------\n'
               f'player 0:\n'
               f'{self.hands[0]}\n'
               f'-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -\n'
               f'player 1:\n'
               f'{self.hands[1]}\n'
               f'-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -\n'
               f'wager = {self.wager}\n'
               f'comparing = {self.comparing}'))

    def play(self, turns, printResults) -> None:
        if printResults:
            self.write()
            for _ in range(turns):
                self.nextTurn()
                self.write()
                if len(self.hands[0]) == 0 or len(self.hands[1]) == 0: break
        else:
            self.write()
            for _ in range(turns):
                self.nextTurn()
                if len(self.hands[0]) == 0 or len(self.hands[1]) == 0: break
            self.write()



card_set, shuffle_times, turns, printResults = loadConfig()

mainDeck = Deck()

mainDeck.addCards(card_set["count"])

mainDeck.shuffle(shuffle_times)

game = Game(mainDeck.give(), card_set['value'])

game.play(turns, printResults)