import random
from helper import continue_option, sr, check_bankruptcy, short_selling, insolvency, close_position
from main import market_statuses, market_duration, market_weights, fluctuation_ranges

balance = 1000
original_stock_price = 100
current_stock_price = original_stock_price
portfolio_value = balance
short_amount = 0
unrealized_pl = 0
total_original_short_interest = 0
total_stock_held = 0

game_run = str(input("Do you want to play using short-selling?"))
if continue_option(game_run):
    game_run = True
else:
    game_run = False
while game_run:
    short_selling_offers = int(input("How often do you want short-selling offers to be spaced out?"))
    market_condition = random.choices(market_statuses, weights=market_weights, k=1)[0]
    timeframe = random.randint(*market_duration[market_condition])
    print(f"The duration of the market is {timeframe}.")
    print(f"The current market condition is {market_condition}.")
    print(f"You have a balance of ${sr(portfolio_value)}")
    for times in range(timeframe):
        fluctuations = random.randint(*fluctuation_ranges[market_condition])
        current_stock_price = sr(current_stock_price * (1 + (fluctuations / 100)))
        print(f"Current Stock Price: ${sr(current_stock_price)}")
        if times % short_selling_offers == 0:
            if insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
                print("You have gone bankrupt, your liabilities are greater than your deposit.")
                solvency = False
                break
            if not insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
                total_stock_held, total_original_short_interest = short_selling(total_stock_held, total_original_short_interest, portfolio_value, current_stock_price)
                if insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
                    break
                total_stock_held, total_original_short_interest, portfolio_value = close_position(total_stock_held, total_original_short_interest, current_stock_price, portfolio_value)
    if insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
        game_run = False
    if not insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
        game_run = str(input("Do you want to keep playing?"))
        if continue_option(game_run):
            game_run = True
            print("The game will continue.")
        elif not continue_option(game_run):
            print("The game has ended.")
            game_run = False

if insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
    print("Thank you for playing, you lost your entire original portfolio.")
    print(f"Fun Fact: Your total short interest was ${sr(total_stock_held * current_stock_price)}.")
    print(f"Your went into debt by ${sr(abs(portfolio_value + (total_original_short_interest - total_stock_held * current_stock_price)))}.")

if not insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
    print("Thank you for playing, you have not lost your entire original portfolio!")
    print(f"Your final balance at the end of the game was ${portfolio_value}.")
    print(f"The change in account from the start is {sr((portfolio_value - balance)/balance * 100)}%.")