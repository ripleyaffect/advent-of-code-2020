def get_input_raw(input_file):
    return [line.strip() for line in open(input_file).readlines()]


def get_decks(input_file):
    input_raw = get_input_raw(input_file)

    break_index = input_raw.index('')

    return (
        [int(val) for val in input_raw[1:break_index]],
        [int(val) for val in input_raw[break_index+2:]]
    )


class Player():
    def __init__(self, id, deck):
        self.id = id
        self.deck = deck

    @property
    def score(self):
        score = 0
        deck_len = len(self.deck)
        for i, card in enumerate(self.deck):
            score += (deck_len - i) * card
        return score

    def draw(self):
        card = self.deck[0]
        self.deck = self.deck[1:]
        return card

    def add_to_bottom(self, cards):
        self.deck += cards
        return self.deck

    def __repr__(self):
        return f'<Player {self.id}>'


class Combat():
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None

    def play_round(self):
        card_1 = self.player_1.draw()
        card_2 = self.player_2.draw()

        if card_1 > card_2:
            self.player_1.add_to_bottom([card_1, card_2])
        else:
            self.player_2.add_to_bottom([card_2, card_1])

        return self.player_1.deck and self.player_2.deck

    def play(self):
        while not self.winner:
            self.play_round()
            if not self.player_2.deck:
                self.winner = self.player_1
            if not self.player_1.deck:
                self.winner = self.player_2
        return self.winner


class RecursiveCombat(Combat):
    def __init__(self, player_1, player_2):
        super().__init__(player_1, player_2)
        self.previous_states = set()

    @property
    def current_state(self):
        return str(self.player_1.deck) + str(self.player_2.deck)

    def save_current_state(self):
        return self.previous_states.add(self.current_state)

    def has_encountered_current_state(self):
        return self.current_state in self.previous_states

    def play_sub_game(self, card_1, card_2):
        return RecursiveCombat(
            Player(1, [card for card in self.player_1.deck][:card_1]),
            Player(2, [card for card in self.player_2.deck][:card_2])
        ).play()

    def get_winning_card(self, card_1, card_2):
        should_recurse = (
            card_1 <= len(self.player_1.deck) and
            card_2 <= len(self.player_2.deck)
        )

        if should_recurse:
            sub_game_winner = self.play_sub_game(card_1, card_2)
            if sub_game_winner.id == self.player_1.id:
                return card_1
            return card_2

        if card_1 > card_2:
            return card_1
        return card_2

    def play_round(self):
        if self.has_encountered_current_state():
            self.winner = self.player_1
            return

        self.save_current_state()

        card_1 = self.player_1.draw()
        card_2 = self.player_2.draw()

        winning_card = self.get_winning_card(card_1, card_2)
        losing_card = card_2 if winning_card == card_1 else card_1

        if winning_card == card_1:
            self.player_1.add_to_bottom([winning_card, losing_card])
        else:
            self.player_2.add_to_bottom([winning_card, losing_card])


        return self.player_1.deck and self.player_2.deck


def run(input_file):
    deck_1, deck_2 = get_decks(input_file)

    combat = Combat(Player(1, deck_1), Player(2, deck_2))
    winner = combat.play()

    print(winner)
    print(f'Part 1: {winner.score}')

    recursive_combat = RecursiveCombat(Player(1, deck_1), Player(2, deck_2))
    winner = recursive_combat.play()

    print(winner)
    print(f'Part 2: {winner.score}')


if __name__ == "__main__":
    run('input.txt')
