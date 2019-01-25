import random

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

PLAYING = True

class Card:
    
    def __init__(self, SUIT, RANK):
        
        self.SUIT = SUIT
        self.RANK = RANK
        pass
    
    def __str__(self):
        return self.RANK+ "of"+self.SUIT

class DECK:
    
    def __init__(self):
        self.DECK = []  # start with an empty list
        for SUIT in SUITS:
            for RANK in RANKS:
                self.DECK.append(Card(SUIT,RANK))
    
    def __str__(self):
        DECK_comp = ''
        for card in self.DECK:
            DECK_comp += '\n'+ card.__str__()
        return "The DECK has: "+DECK_comp

    def shuffle(self):
        random.shuffle(self.DECK)
        
    def deal(self):
        single_card = self.DECK.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the DECK class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self, card):
        #The card passed in
        #from the DECK.deal() --> Single Card(SUIT,RANK)
        self.cards.append(card)
        self.value += VALUES[card.RANK]
        
        if card.RANK == 'Ace':
            self.aces += 1
        
    
    def adjust_for_ace(self):
        
        #IF TOTAL VALUE > 21 AND I STILL HAVE AN ACE
        # THAN CHANGE MY ACE TO BE A 1 INSTEAD OF 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self, total=100):
        self.total = total  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips would like to bet"))
        except:
            print("Sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
            else:
                break

def hit(DECK, hand):
    
    single_card = DECK.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(DECK, hand):
    global PLAYING  # to control an upcoming while loop
    
    while True:
        x = input("Hit or Stand? Enter h or s.")
        
        if x[0].lower() == 'h':
            hit(DECK,hand)
        elif x[0].lower() == 's':
            print("Player Stands, Dealers turn!")
            PLAYING = False
        else:
            print("Sorry, I didn't understand that. Please enter h or s only!")
            continue
        
        break

def show_some(player, dealer):
    
    print('\n')
    print("DEALERS HAND:")
    print('\n')
    print('one card hidden!')
    print(dealer.cards[1])
    print('\n')
    print('PLAYERS HAND:')
    print('\n')
    for card in player.cards:
        print(card)
    
    
    
    
def show_all(player, dealer):
    
    print('DEALERS HAND:')
    for card in dealer.cards:
        print(card)
    print("\n")
    print('PLAYERS HAND:')
    for card in player.cards:
        print(card)

def player_busts(player, dealer, chips):
    print("BUST PLAYER!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("PLAYER WINS!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("PLAYER WINS! DEALER BUSTED")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("DEALER WINS!")
    chips.lose_bet()
    
def push(player, dealer):
    print("Delaer and player tie! PUSH")

while True:
    # Print an opening statement

    print("WELCOME TO BLACKJACK")
    # Create & shuffle the DECK, deal two cards to each player
    DECK = DECK()
    DECK.shuffle()
    
    PLAYER_HAND = Hand()
    PLAYER_HAND.add_card(DECK.deal())
    PLAYER_HAND.add_card(DECK.deal())
    
    DEALER_HAND = Hand()
    DEALER_HAND.add_card(DECK.deal())
    DEALER_HAND.add_card(DECK.deal())
    
        
    # Set up the Player's chips
    PLAYER_CHIPS = Chips()
    
    # Prompt the Player for their bet
    take_bet(PLAYER_CHIPS)
    
    # Show cards (but keep one dealer card hidden)
    show_some(PLAYER_HAND,DEALER_HAND)
    
    while PLAYING:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(DECK,PLAYER_HAND)
        
        # Show cards (but keep one dealer card hidden)
        show_some(PLAYER_HAND,DEALER_HAND)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if PLAYER_HAND.value > 21:
            player_busts(PLAYER_HAND,DEALER_HAND,PLAYER_CHIPS)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if PLAYER_HAND.value <= 21:
        
        while DEALER_HAND.value < 17:
            hit(DECK,DEALER_HAND)
    
        # Show all cards
        show_all(PLAYER_HAND,PLAYER_HAND)
        # Run different winning scenarios
        if DEALER_HAND.value > 21:
            dealer_busts(PLAYER_HAND,DEALER_HAND,PLAYER_CHIPS)
        elif DEALER_HAND.value > PLAYER_HAND.value:
            dealer_wins(PLAYER_HAND,DEALER_HAND,PLAYER_CHIPS)
        elif DEALER_HAND.value < PLAYER_HAND.value:
            player_wins(PLAYER_HAND,DEALER_HAND,PLAYER_CHIPS)
        else:
            push(PLAYER_HAND,DEALER_HAND)
    
    # Inform Player of their chips total 
    print('\n Player total chips are at: {}'.format(PLAYER_CHIPS.total))
    # Ask to play again
    NEW_GAME = input("Would you like to play another hand? y/n")
    
    if NEW_GAME[0].lower() == 'y':
        PLAYING = True
        continue
    else:
        print("Thanks for PLAYING!\n Credits: By Tacio Degrazia")    
        break