The Stock Market Game:
The premise of the whole game and my development of it was to create something similar to real life stock market's in Python, for example, market condition's, which I have implemented by having the game choose out of a random selection of market conditions, which are weighted for their probabilities to occur, which produce the market conditions during your run.
For each market condition, I gave it 2 values, which are set to the minimum and maximum timeframe a market condition can have. This mimics real life stock markets as in general, Bull Markets last much longer than Recessions, Depressions, and Bear Markets, although even in this simulation, it is somewhat limited by the range I have implemented.
You can set when you want a purchase offer (basically, a buy and sell option) will appear after a certain amount of time. If you want to play more granularly, you can set the purchase offers to be closer together by spacing them out less. 
I see this as a good representation of the actual market, since people will simply have different preferences as to when they want to trade, some might trade on a daily timeframe, while other may trade on weekly, monthly, or minutes, and this simply gives the player customizability.

After finishing the base model of the game, I attempted to make short-selling a reality by integrating it into my original selling mechanics, but it was so convoluted that I ultimately scrapped the idea of integrating it into my sell function.
Instead, I decided to rebuild the game from scratch, and start working on it on another file.
Onec I got the base functions of short-selling to work, I refactored the code into functions, which made it much more readable, and I tried to remove redundancies, though I am sure there is definitely more than can be done to simplify game functions or make it more realistic.
I plan to continue working on this to fix current, buggy, or inconsistent logic in this game, and add new features, like options trading and fully integrating the short-selling mechanics with the base game, since due to the complex nature of short-selling, I really don't want to integrate it just yet as there are still kinks I have to work out and to improve the realism.

I haven't had a chance to create comments on my code yet, but I hope to do so in the future when I have the time to. 

For the message about forced liquidation, if the unrealized profit-loss is greater than your portfolio value, forced liquidation will occur, and otherwise, forced liquidation message typically tells you your portfolio value if the unrealized profit-loss is positive or not greater than your margin, which means you are safe, but if the forced liquidation message is less tha your portfolio value, it implies that your unrealized profit-loss is greater than your margin and is currently eating into your portfolio.

(Now that I think about it, it wouldn't be so hard to integrate into the base, but I'm unsure of how the logic would work, since the way I built it up, it uses similar variable names, and I might have to address some issues there, but it shouldn't be impossible. 
And, another thing, I would really like to correct is the floating point errors, because they happen all the time while playing, so it would be a lot less annoying if that didn't keep happening.)
