## **You do not need seperate hyperopt files in ft_user data anymore. You can just run the command below and start optimization** 

`docker-compose run --rm freqtrade hyperopt --enable-protections --strategy bbrsiNaiveStrategy --hyperopt-loss SharpeHyperOptLoss -i 15m -e 500`

*you can also see what the protections are in hyperopt's documentation, and activate and deactivate specific protections you see the best fit to your strategy* 

## **NOTE: *SharpeHyperOptLoss* is one of the many built-in hyperopt-loss(IHyperOptLoss) functions available**.

**built-in hyperopt-loss functions:**

*ShortTradeDurHyperOptLoss, OnlyProfitHyperOptLoss,
SharpeHyperOptLoss, SharpeHyperOptLossDaily,
SortinoHyperOptLoss, SortinoHyperOptLossDaily,
CalmarHyperOptLoss, MaxDrawDownHyperOptLoss,
MaxDrawDownRelativeHyperOptLoss, ProfitDrawDownHyperOptLoss*