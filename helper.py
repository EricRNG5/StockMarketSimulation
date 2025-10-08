def purchasing_stock(balance, total_stock, current_stock_price):
    purchasing = str(input(f"Do you want to purchase at this price? ({sr(current_stock_price)})"))
    if continue_option(purchasing.lower()):
        number_of_stock_purchased = int(input(f"How much to purchase at this price? ({sr(current_stock_price)})"))
        total_purchase_price = (number_of_stock_purchased * round(current_stock_price, 2))
        purchase_infeasible = total_purchase_price > balance
        if purchase_infeasible:
            print(f"Unable to purchase {number_of_stock_purchased}. ({total_purchase_price - balance})")
        else:
            current_balance = round((balance - total_purchase_price), 2)
            print(f"Purchased {number_of_stock_purchased}.")
            total_stock += number_of_stock_purchased
            new_total_stock = total_stock
            print(f"Total stock: {new_total_stock}")
            print(f"New Balance: {current_balance}")
        return current_balance, new_total_stock
    elif not continue_option(purchasing.lower()):
        print("No stock purchased at this price.")
        return balance, total_stock
    else:
        return balance, total_stock


def selling_stock(balance, total_stock, current_stock_price):
    selling = str(input(f"Do you want to sell at this price? ({sr(current_stock_price)})"))
    if continue_option(selling.lower()):
        selling_amount = int(input(f"How much do you want to sell at this price? ({sr(current_stock_price)})"))
        if selling_amount <= 0 and total_stock == 0:
            print("Unable to sell stock that you don't own.")
            return balance, total_stock
        elif selling_amount > total_stock:
            print(f"Unable to sell more than you own. ({total_stock})")
            return balance, total_stock
        else:
            print(f"You sold {selling_amount} stock. You have {total_stock - selling_amount} stock left.")
            balance += sr(selling_amount * current_stock_price)
            print(f"New balance: ${balance}")
            total_stock -= selling_amount
            return balance, total_stock
    elif not continue_option(selling.lower()):
        print("No stock sold at this price.")
        return balance, total_stock
    else:
        return balance, total_stock

# sr is shorthand for simplified rounding, due to the high usage case of rounding to the 2nd float
# as money is denominated to 2 decimals, and there are a lot of rounding errors, and I don't know
# where exactly they all come from.


def sr(rounded):
    rounded = round(rounded, 2)
    return rounded

def continue_option(user_input):
    confirmation = ["yes", "y", "true"]
    denied = ["no", "n", "false"]
    if user_input in confirmation:
        return True
    elif user_input in denied:
        return False
    else:
        return False

def unrealized_pl(total_original_short_interest, current_stock_price, total_stock_held, portfolio_value):
    current_short_value = current_stock_price * total_stock_held
    realized_profit_loss = portfolio_value + (total_original_short_interest - current_short_value)
    return realized_profit_loss

def check_bankruptcy(loss_from_position, bankruptcy_threshold):
    real_equity = loss_from_position + bankruptcy_threshold
    if real_equity <= 0:
        return True
    elif real_equity > 0:
        return False


def short_selling(total_stock_held, total_original_short_interest, portfolio_value, current_stock_price):
    short = str(input(f"Do you want to short at this price? ({sr(current_stock_price)})"))
    if continue_option(short):
        short_amount = int(input(f"How many stock do you want to short-sell?"))
        if short_amount <= 0:
            print("Unable to short negative stock.")
            return total_stock_held, total_original_short_interest
        elif short_amount > 0:
            short_interest = short_amount * current_stock_price
            if insolvency(total_stock_held + short_amount, current_stock_price, total_original_short_interest, portfolio_value):
                print(f"You cannot short greater than your entire margin account value.")
                return total_stock_held, total_original_short_interest
            elif not insolvency(total_stock_held + short_amount, current_stock_price, total_original_short_interest, portfolio_value):
                total_original_short_interest += short_interest
                total_stock_held += short_amount
                print(f"New Total Stock Shorted: {total_stock_held} stock.")
                print(f"New Total Short Interest: ${total_stock_held * current_stock_price}")
                return total_stock_held, total_original_short_interest
        return total_stock_held, total_original_short_interest
    elif not continue_option(short):
        print("No stock shorted at this price.")
        return total_stock_held, total_original_short_interest
    else:
        return total_stock_held, total_original_short_interest

def insolvency(total_stock_held, current_stock_price, total_original_short_interest, portfolio_value):
    pl_from_position = unrealized_pl(total_original_short_interest, current_stock_price, total_stock_held, portfolio_value)
    return check_bankruptcy(pl_from_position, portfolio_value)


def close_position(total_stock_held, total_original_short_interest, current_stock_price, portfolio_value):
    close_position = input("Close position? (y/n)")
    if continue_option(close_position):
        print(f"To close the position you will have to buyback shares at {current_stock_price}.")
        print(f"Your total shares number of shares is ${total_stock_held}.")
        input("Enter anything to close the position.")
        portfolio_value =  unrealized_pl(total_original_short_interest, current_stock_price, total_stock_held, portfolio_value)
        total_original_short_interest = 0
        total_stock_held = 0
        print(f"Your new balance is ${sr(portfolio_value)}.")
        return total_stock_held, total_original_short_interest, portfolio_value
    elif not continue_option(close_position):
        print(f"Your short position has not been closed.")
        print(f"Reminder: Your total current short interest is {sr(total_stock_held * current_stock_price)}.")
        print(f"You are ${sr(unrealized_pl(total_original_short_interest, current_stock_price, total_stock_held, portfolio_value))} away from forced liquidation. (Bankruptcy)")
        print(f"Your balance is ${sr(portfolio_value)}. Make sure to keep it above short interest.")
        return total_stock_held, total_original_short_interest, portfolio_value
    else:
        return total_stock_held, total_original_short_interest, portfolio_value

def portfolio(balance, current_stock_price, total_stock):
    portfolio_value = balance + current_stock_price * total_stock
    return portfolio_value