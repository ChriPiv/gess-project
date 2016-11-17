# MATLAB Fall 2016 – Research Plan

> * Group Name: Council of Rivendell 
> * Group participants names: Daniel Keyes, Isabella Marquez, Christophe Piveteau
> * Project Title: Analyzing Investment Strategies in a Agent-Based Financial Market Simulation

## General Introduction

The importance of understanding the dynamics in a financial market and the parameters that determine investor behaviour is manifested in the various policy efforts that seek to maintain integrity in the financial system. 

For instance, in order to secure market confidence, regulate foreign participation and prevent collusion, policy makers have become increasingly interested in identifying dominant trading strategies and the social effects that level the playing field. The market composition plays a significant role in the predictive analysis as it is likely to exacerbate inherent financial dynamics. Examples are the speculative bubbles experienced in 2000 and 2007 as observed by Kaizoji et al [2].

One of the earliest works similar to this project is [4], which uses an agent-based economic model. Further related works that use the same model have mostly investigated emerging market characteristics (formation of demand/supply or characteristic price formation). Since the agent-based model has proven its usefulness in modelling market characteristics we feel comfortable to adopt and expand the proposed model in order to study how market characteristics propagate back to the agent as in how they adapt their strategies.


## The Model

We use an agent-based model losely based on [1] to simulate a financial market. Every timestep each agent makes a buy/sell order which consists of an amount of assets to be traded and a limit price at which those assets are to be traded.

This amount is computed in the following way: The agent considers how much assets it wants to own next timestep. This value is drawn from a normal distribution with mean <i>mu<sub>S</sub></i> and standard deviation <i>sigma<sub>S</sub></i>:
<i>mu<sub>S</sub></i> = currentAmountOfAssets * (1 + (marketPrice - meanMarketPriceOverNTimesteps) * agentConservativness + priceMomentum * agentInfluencability)
<i>mu<sub>S</sub></i> = agentNoisiness
We see the <i>mu<sub>S</sub></i> starts out to be around the current amount of assets of the agnet. There are two force influencing <i><sub>mu</sub>A</i>: If the market price is higher(lower) than the average in recent history, then the agent is more likely to sell(buy). If a lot of people are buying(selling) and thus the market price momentum is high(low) the agent is more likely to buy(sell). These two forces are weighted by two agent parameters: its conservativeness and its influencability.
A third parameter governs the behaviour of our agent: its noisiness.

Finally the order price is also taken from a normal distribution with mean <i>mu<sub>P</sub></i> and standard deviation <i>sigma<sub>P</sub></i>:
<i>mu<sub>P</sub></i> = 0.99 * currentAssetPrice if the agent is buying
<i>mu<sub>P</sub></i> = 1.01 * currentAssetPrice if the agent is selling
<i>sigma<sub>P</sub></i> = const. * marketVolatility

Agents also undergo a learning process. The model is run for a specific number of time steps, then a ranking of the agents is done considering their final owned wealth. Depending on how successfull each agent was in that ranking, it will adapt its parameters: A successfull agent will only slightly change its parameters, while less successfull agents will vary them more strongly.

As this convergence process could be extremely complex, we will first start out by reducing our agent paramaters to 1. We will fix the agent noisiness and tie conservativeness and influencability together
noisiness = C - influencability with C being a constant
basically reducing both parameters to one.


## Fundamental Questions

How does the evolution and distribution of strategies depend on market parameters?
Which strategy/strategies prevail/s depending on the market parameters?
What subspaces of our market parameter spaces produce mostly one strategy? What subspaces allow for a wider range of successful strategies?
Can our model predict interesting properties of real markets in the term of optimal strategies?


## Expected Results

We expect high risk traders to be at the same time be the most and least successful traders in our ranking.

We expect chartist/influencable agents to be more successfull in markets with higher clustering probabilities, as they will be able to make buy decisions which take into account the greater social movements inside our market. But when market fluctuations are too big, the entirety of the chartist agents starts encountering higher risks of losing money together at one time, as market fluctuations start to have higher effects than social movements.


## References 

* [1] Marco Raberto, Silvano Cincotti, Sergio M Focardi, Michele Marchesi, Agent-based simulation of a financial market
* [2] Taisei Kaizoji, Matthias Leiss, Alexander Saichev, Didier Sornette, Super-exponential endogenous bubbles in an equilibrium model of fundamentalist and chartist traders
* [3] Matthias Leiss, Financial Market Ris of Speculative Bubbles
* [4] Positive Feedback Investment Strategies and Destabilizing Rational Speculation, De Long et al.

## Research Methods

We will run our agent-based simulations for many different market parameters and analyze the strategy distribution after a long period of time. This will allow us to map phases where different populations are successful.
