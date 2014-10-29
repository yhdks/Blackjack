# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome2 = ""
outcome3 = ""
outcome4 = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.ha = []
        pass	# create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.ha)):
            ans += str(self.ha[i]) + " "
        return "Hand contains " + ans
        pass	# return a string representation of a hand

    def add_card(self, card):
        self.ha.append(card)
        pass	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        count = 0
        value_of_hand = 0
        for j in range(len(self.ha)):
            if VALUES.get(self.ha[j].get_rank()) == 1:
                count += 1
            value_of_hand += VALUES.get(self.ha[j].get_rank())

        if count > 0:
            for k in range(count):
                if value_of_hand + 10 <= 21:
                    value_of_hand += 10
        
        return value_of_hand
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for j in range(len(self.ha)):
            self.ha[j].draw(canvas, [pos[0] + j*CARD_SIZE[0], pos[1]])

        pass	# draw a hand on the canvas, use the draw method for cards

 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        pass	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)
        pass    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop(0)
        pass	# deal a card object from the deck
    
    def __str__(self):
        anss = ""
        for i in range(len(self.deck)):
            anss += str(self.deck[i]) + " "
        return anss
        pass	# return a string representing the deck


    #define event handlers for buttons
def deal():
    global outcome, outcome2, in_play, dec, player_hand, dealer_hand, score, outcome3, outcome4
    outcome2 = ""
    outcome3 = ""
    outcome4 = ""
    # your code goes here
    if in_play:
        score -= 1
        outcome2 = "You just lost the previous round due to a new deal request."
    
    dec = Deck()
    dec.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(dec.deal_card())
    dealer_hand.add_card(dec.deal_card())
    player_hand.add_card(dec.deal_card())
    dealer_hand.add_card(dec.deal_card())
    
    outcome = "Hit or stand?"
    in_play = True

def hit():
    global in_play, outcome, score, outcome2, outcome3, outcome4
    outcome2 = ""
    pass	# replace with your code below
 
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(dec.deal_card())
        if in_play and player_hand.get_value() > 21:
            outcome = "Dealer wins! New deal?"
            outcome2 = "You have busted."
            outcome3 = str(dealer_hand.get_value())
            outcome4 = str(player_hand.get_value())
            in_play = False
            score -= 1
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, in_play, score, outcome2, outcome3, outcome4
    pass	# replace with your code below
    outcome2 = ""
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if player_hand.get_value() > 21:
            outcome2 = "You have busted."
        elif player_hand.get_value() <= 21:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(dec.deal_card())
                
        if dealer_hand.get_value() > 21:
            outcome = "You win! New deal?"
            outcome2 = "Dealer has busted."
            score += 1
        elif player_hand.get_value() - dealer_hand.get_value() > 0:
            outcome = "You win! New deal?"
            score += 1
        elif player_hand.get_value() - dealer_hand.get_value() <= 0:
            outcome = "Dealer wins! New deal?"
            score -= 1
    # assign a message to outcome, update in_play and score
    outcome3 = str(dealer_hand.get_value())
    outcome4 = str(player_hand.get_value())
    in_play = False
    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, outcome2
    
    player_hand.draw(canvas, [130, 400])
    dealer_hand.draw(canvas, [130, 200])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [130 + CARD_BACK_SIZE[0]/2, 200 + CARD_BACK_SIZE[1]/2], CARD_BACK_SIZE)

    canvas.draw_text(outcome, (150, 590), 32, 'White')
    canvas.draw_text(outcome2, (20, 540), 16, 'White')
    canvas.draw_text(outcome3, (220, 180), 24, 'Orange')
    canvas.draw_text(outcome4, (220, 380), 24, 'Orange')
    canvas.draw_text("Blackjack", (170, 50), 60, 'Pink')
    canvas.draw_text("Your score:", (260, 120), 40, 'Cyan')
    canvas.draw_text(str(score), (500, 120), 40, 'Cyan')
    canvas.draw_text("Dealer", (130, 180), 24, 'Yellow')
    canvas.draw_text("Player", (130, 380), 24, 'Yellow')

    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Black")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric