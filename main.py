import random
import time
from helper import purchasing_stock, sr, selling_stock, continue_option

stock_price = 100.00
new_price = float(100)
initial_balance = 1000
balance = initial_balance
total_stock = 0
previous_portfolio = initial_balance
market_statuses = ["Recession", "Depression", "Bear Market", "Stagnation", "Bull Market", "Euphoria"]
fluctuation_ranges = {
    "Recession": (-5, 1),
    "Depression": (-10, -2),
    "Bear Market": (-6, 3),
    "Stagnation": (-2, 2),
    "Bull Market": (-3, 6),
    "Euphoria": (2, 12)}
market_duration = {
    "Recession": (5, 15),
    "Depression": (10, 30),
    "Bear Market": (15, 25),
    "Stagnation": (30, 50),
    "Bull Market": (30, 70),
    "Euphoria": (10, 15)
}
market_weights = [5, 2, 25, 25, 41, 2]
changes_over_time = []
market_cycle = 1
portfolio = balance + total_stock * new_price
game_running = str(input("Do you want to play using normal stock?"))
if continue_option(game_running):
    game_running = True
else:
    game_running = False
while game_running:
    purchase_offers = int(input("How often do you want purchase offers to be spaced out?"))
    if purchase_offers <= 0:
        purchase_offers = 1
    market_condition = random.choices(market_statuses, weights=market_weights, k=1)[0]
    timeframe = random.randint(*market_duration[market_condition])
    print(f"The duration of the market is {timeframe}.")
    print(f"The current market condition is {market_condition}.")
    print(f"You have a balance of ${sr(balance)}")
    previous_portfolio = balance + total_stock * new_price
    for times in range(timeframe):
        if times % purchase_offers == 0:
            balance, total_stock = purchasing_stock(balance, total_stock, new_price)
            balance, total_stock = selling_stock(balance, total_stock, new_price)
        fluctuations = random.randint(*fluctuation_ranges[market_condition])
        percentage = fluctuations / 100
        new_price = new_price * (1 + percentage)
        time.sleep(0)
        print(f"Current Price: ${sr(new_price)}")
    print(f"Your final price was ${sr(new_price)}.")
    portfolio_change = ((portfolio - previous_portfolio)/previous_portfolio) * 100
    changes_over_time.append(sr(portfolio_change))
    if portfolio > previous_portfolio:
        win = sr(portfolio - previous_portfolio)
        print(f"Your portfolio has gained ${win}! ({sr(portfolio_change)}%)")
    elif previous_portfolio > portfolio:
        lose = sr(previous_portfolio - portfolio)
        print(f"Your portfolio has lost ${lose}! ({sr(portfolio_change)}%)")
    elif previous_portfolio == (balance + total_stock * new_price):
        print("You broke even.")
    game_running = input("Do you want to play again?")
    if continue_option(game_running.lower()):
        game_running = True
    else:
        game_running = False

print("Thank you for playing this wacky simulation.")
print("------------STATS DURING GAME------------")
print(f"Your final portfolio value was ${sr(portfolio)}.")
for change in changes_over_time:
    print(f"Your portfolio changed by {change}% in run {market_cycle}.")
    market_cycle += 1