# MATLAB Fall 2016 – Research Plan

> * Group Name: DCI
> * Group participants names: Daniel Keyes, Isabella Marquez, Christophe Piveteau
> * Project Title: Analyzing Investment Strategies in a Agent-Based Financial Market Simulation

## General Introduction

The importance of understanding the dynamics in a financial market and the parameters that determine investor behaviour is manifested in the various policy efforts that seek to maintain integrity in the financial system. 

For instance, in order to secure market confidence, regulate foreign participation and prevent collusion, policy makers have become increasingly interested in identifying dominant trading strategies and the social effects that level the playing field. The market composition plays a significant role in the predictive analysis as it is likely to exacerbate inherent financial dynamics. Examples are the speculative bubbles experienced in 2000 and 2007 as observed by Kaizoji et al [2].

One of the earliest works similar to this project is [4], which uses an agent-based economic model. Further related works that use the same model have mostly investigated emerging market characteristics (formation of demand/supply or characteristic price formation). Since the agent-based model has proven its usefulness in modelling market characteristics we feel comfortable to adopt and expand the proposed model in order to study how market characteristics propagate back to the agent as in how they adapt their strategies.


## The Model

We use an agent-based model adapted from [1] to simulate a financial market. As the model includes social interactions in the form of clustering, it has been shown to be able to reproduce some key characteristics of real financial markets, such as fat tails and volatility clustering. The model is built upon by adding random price fluctuations and adding smarter agents which undergo a learning process.

Agents have variable parameters (riskiness and influenceability) which model their strategy. We can therefore differentiate between chartists and fundamentalists (this distinction was absent in [1], however has been used in other models, such as [2]). The transition however is continuous, not discrete. Agents also engage a learning process: Depending on their performance compared to the other agents, they vary their parameters more or less strongly.

There are some global market parameters that can be adjusted: The variations of the market growth fluctiations and asset price fluctuations can be separately set. Additionally the amount of agents participating can be varied aswell. The probability of the cluster activation process, which represents the facility of cooperation/social interactions, is also variable.

The model is run for a specific number of time steps, aiming at reaching a stable distribution of agent parameters.


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

We will run our agent-based simulations for many different market parameters and analyze the strategy distribution after a long period of time. This will allow us to make a map.
