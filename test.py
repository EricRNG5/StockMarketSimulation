import random
from helper import continue_option, sr, check_bankruptcy, short_selling, insolvency
from main import market_statuses, market_duration, market_weights, fluctuation_ranges

balance = 1000
original_stock_price = 100
new_stock_price = original_stock_price
portfolio = balance
short_amount = 0
unrealized_pl = 0
# tosh is shorthand for total_original_short_interest
tosh = 0
# total_sh is total shorted stock held, basically the total stock.
total_sh = 0

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
    print(f"You have a balance of ${sr(portfolio)}")
    for times in range(timeframe):
        fluctuations = random.randint(*fluctuation_ranges[market_condition])
        new_stock_price = sr(new_stock_price * (1 + (fluctuations / 100)))
        print(f"Current Stock Price: ${sr(new_stock_price)}")
        if times % short_selling_offers == 0:
            if insolvency(total_sh, new_stock_price, portfolio):
                print("You have gone bankrupt, your liabilities are greater than your deposit.")
                solvency = False
                break
            if not insolvency(total_sh, new_stock_price, portfolio):
                total_sh, tosh = short_selling(total_sh, tosh, portfolio, new_stock_price)
                close_position = input("Close position? (y/n)")
                if continue_option(close_position):
                    print(f"To close the position you will have to buyback shares at {new_stock_price}.")
                    print(f"Your total shares number of shares is ${total_sh}.")
                    input("Enter anything to close the position.")
                    unrealized_pl = tosh - total_sh * new_stock_price
                    portfolio += unrealized_pl
                    tosh = 0
                    total_sh = 0
                    print(f"Your new balance is ${sr(portfolio)}.")
                elif not continue_option(close_position):
                    print(f"Your short position has not been closed.")
                    print(f"Reminder: Your total short interest is {sr(tosh)}.")
                    print(f"You are ${sr(portfolio * 3 - total_sh * new_stock_price)} away from a margin call. (Bankruptcy)")
                    print(f"Your balance is ${sr(portfolio)}. Make sure to keep it above short interest.")
    if insolvency(total_sh, new_stock_price, portfolio):
        game_run = False
    if not insolvency(total_sh, new_stock_price, portfolio):
        game_run = str(input("Do you want to keep playing?"))
        if continue_option(game_run):
            game_run = True
            print("The game will continue.")
        elif not continue_option(game_run):
            print("The game has ended.")
            game_run = False

if insolvency(total_sh, new_stock_price, portfolio):
    print("Thank you for playing, you lost your entire original portfolio.")
    print(f"Fun Fact: Your total short interest was ${sr(total_sh * new_stock_price)}.")
    print(f"Your went into debt by ${sr(((total_sh * new_stock_price) - tosh)  - portfolio)}.")

if not insolvency(total_sh, new_stock_price, portfolio):
    print("Thank you for playing, you have not lost your entire original portfolio!")
    print(f"Your final balance at the end of the game was ${portfolio}.")
    print(f"The change in account from the start is {sr((portfolio - balance)/balance * 100)}%.")