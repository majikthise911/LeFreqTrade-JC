# Getting Started

1.  first create dev folder for this.
2.  activate dev env
3.  go to https://www.freqtrade.io/en/stable/docker_quickstart/
4.  cd to directory you want to work from and mkdir ft_userdata
5.  cd to ft_userdata
6.  paste the following into the terminal to download the docker-compose file from the repository:

- curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

### Pull the freqtrade image:

- docker-compose pull

### Create user directory structure

- docker-compose run --rm freqtrade create-userdir --userdir user_data

### Create configuration - Requires answering several questions

Paste the following into the terminal and then you will be prompted to answer several questions for the .json config file.

- docker-compose run --rm freqtrade new-config --config user_data/config.json
    interactive questions

### We will then have to answer some questions.

1.  ? Do you want to enable Dry-run (simulated trades)? Yes
2.  ? Please insert your stake currency: USD
3.  ? Please insert your stake amount (Number or 'unlimited'): unlimited
4.  ? Please insert max\_open\_trades (Integer or -1 for unlimited open trades): 10
5.  ? Time Have the strategy define timeframe.
6.  ? Please insert your display Currency (for reporting): USD
7.  ? Select exchange ftx
8.  ? Do you want to enable Telegram? Yes
    1.  To create a telegram bot:
        1.  add BotFather in telegram desktop app
        2.  in the chat with BotFather type the following
            - /start
            - /newbot
            - name the bot
            - create a username
        3.  to get chat ID
            - go to https://api.telegram.org/botXXX:YYYYY/getUpdates
            - (replace the XXX: YYYYY with your BOT HTTP API Token you just got from the Telegram BotFather)
            - In order to see the chat ID you must chat the bot in telegram.
            - you will see the chat ID in the window
            - Alternatively you can use the tool in the following linke: https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659
9.  ? Insert Telegram token **********************************************
10. ? Insert Telegram chat id **********
11. ? Do you want to enable the Rest API (includes FreqUI)? Yes
12. ? Insert Api server Listen Address (0.0.0.0 for docker, otherwise best left untouched) 0.0.0.0
13. ? Insert api-server username freqtrader
14. ? Insert api-server password pizza


### Spin up docker which will then communicate with telegram app

- docker-compose up -d

### Now that this is working lets add a dry run wallet amount

- Click on the config.json file in the user\_data folder and under "dry\_run": true, line type:
    - "dry\_run\_wallet": 20000,
- Now we must reload the config file in telegram by going to Telegram and typing in
    - /reload_config

# Changing the strategy

1.  copy and paste a pair list whitelist in the config.json file
    
2.  This will go in the "exchange" block under "pair_whitelist"
    
    },
    
    "exchange": {
    
    "name": "ftx",
    
    "key": "",
    
    "secret": "",
    
    "ccxt_config": {},
    
    "ccxt\_async\_config": {},
    
    "pair_whitelist": \[
    
    "ALGO/USD",
    
    "ATOM/USD",
    
    "BAT/USD",
    
    "BTC/USD",
    
    "BCH/USD",
    
    "ETH/USD",
    
    "LINK/USD",
    
    "LTC/USD",
    
    "XRP/USD",
    
    "SOL/USD"
    
    \],
    
3.  When ever you make changes to the .json file need to go back into telegram and type
    
    - /reload_config
4.  Next to change the strategy, go to the <ins>strategy.py</ins> file and copy the <ins>class name</ins> into the <ins>docker_compose.yml</ins> file next to strategy
    
5.  Whenever change the docker-compose file need to bring bot down and back up again with
    
    - docker-compose down
    - docker-compose up -d
6.  next navigate to freq ui to log in
    
7.  find the credentials in config.json file
    
    1.  type http://localhost:8080/

# Hyperopt Video Steps:

When you see “freqtrade” in the http://freqtrade.io docs, then it assumes docker-compose run

- Pip install hvPlot if you don’t have it already installed on your Python interpreter which you are running your freqtrad

### BACKTESTING (DOWNLOAD PAIRS)

2.  Create a pairs.json file in the *data* subdirectory of the *user_data* folder and paste the whitelist. Use the same format as the config.json whitelist but without setting it to a variable
    
    - \[
        
        "ALGO/USD",
        
        "ATOM/USD",
        
        "BAT/USD",
        
        "BTC/USD",
        
        "BCH/USD",
        
        "ETH/USD",
        
        "LINK/USD",
        
        "LTC/USD",
        
        "XRP/USD",
        
        "SOL/USD"
        
        \]
        
3.  Type in the terminal while in the main directory for freqtrade
    
    - *$ docker-compose run --rm freqtrade download-data --exchange ftx -t 15m*
        - The above will default to download data for 29 days. To backtest for different periods you must use --timeframe command as follows:
    - *$ docker-compose run --rm freqtrade download-data --exchange ftx -t 15m --timerange=20210726-*
    - This command will download data starting from 7/26/2021 up to present day then your backtesting command will default backtest all the data from 7/26/2021 to present day
4.  Back test your strategy for the number of days that you downloaded data for using the command:
    
    - *$ docker-compose run --rm freqtrade backtesting --datadir user_data/data/ftx --export trades --stake-amount 10000 -s bbrsiNaiveStrategy -i 15m*
        *Note:* Must have StaticPairList instead of volumepairlist in the config.json file and the number of assets needs to be set to the same number of pairs in the pair list or you will get ERROR: 2

# PLOTTING

5.  Plot this by going to the docker-compose.yml file and
    a) uncomment the image:develop_Plot and comment out the first two images.
6.  Enter the command:
    - *$ docker-compose run --rm freqtrade plot-dataframe --strategy bbrsiNaiveStrategy -p BEST PAIR -i 15m*
        a). make sure that there are no market order types in the strategy .py
7.  Open the file in Finder and then open the file in a browser of your choice (just copy  and past to desktop, right click, and open with.
8.  Highlight a portion of the plot to expand, then hover over trades to identify the reason and to make sure hvplot is installed in your base Python interpreter
9.  Revert the image changes in the docker-compose.yml file after plotting!

### HYPEROPTING - notes - likely will delete 

10. We want to hyper opt with protections (cooldown period etc). In this example, doing 500 epochs. 5000 recommended but it takes a lot longer
    
    - docker-compose run --rm freqtrade hyperopt --enable-protections --strategy bbrsiNaiveStrategy --hyperopt-loss SharpeHyperOptLoss -i 15m -e 500
11. once hyperopt is complete, go to the telegram bot and type in /reload_config
    

- To check that your bot is running the hyperopted version of the strategy, look at the roi value in the strategy.json file and type /show_config in telegram to compare the roi numbers, the format will look like {'0': 0.226, '115': 0.097, '293': 0.026, '645': 0} the 0.226 is the roi. if they are the same then you are good to go