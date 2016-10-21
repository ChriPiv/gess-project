# MATLAB Fall 2016 – Research Plan

> * Group Name: DCI
> * Group participants names: Daniel Keyes, Isabella Marquez, Christophe Piveteau
> * Project Title: Analyzing Optimal Investment Strategies in a Agent-Based Financial Market Simulation

## General Introduction

TODO


## The Model

We use an agent-based model adapted from [1] to simulate a financial market. As the model includes social interactions in the form of clustering, it has been shown to be able to reproduce some key characteristics of real financial markets, such as fat tails and volatility clustering.

Agents have variable parameters (riskiness and influenceability) which model their strategy. We can therefore differentiate between chartists and fundamentalists (this distinction was absent in [1], however has been used in other models, such as [2]). The transition however is continuous, not discrete. Agents also engage a learning process: Depending on their performance compared to the other agents, they vary their parameters more or less strongly.

There are some global market parameters that can be adjusted: The variations of the market growth fluctiations and asset price fluctuations can be separately set. Additionally the amount of agents participating can be varied aswell. The probability of the cluster activation process, which represents the facility of cooperation/social interactions, is also variable.

The model is run for a specific number of time steps, aiming at reaching a stable distribution of agent parameters.


## Fundamental Questions

How does the evolution and distribution of strategies depend on market parameters?
Which strategy/strategies prevail/s depending on the market parameters?
What subspaces of our market parameter spaces produce mostly one strategy? What subspaces allow for a wider range of successful strategies?
Can our model predict interesting properties of real markets in the term of optimal strategies?


## Expected Results

We expect fundamentalist agents to me more successfull in markets with large asset price fluctuations.
We also expect chartists agents to be more successfull in markets with high clustering probabilities. 


## References 

* [1] Marco Raberto, Silvano Cincotti, Sergio M Focardi, Michele Marchesi, Agent-based simulation of a financial market
* [2] Taisei Kaizoji, Matthias Leiss, Alexander Saichev, Didier Sornette, Super-exponential endogenous bubbles in an equilibrium model of fundamentalist and chartist traders
* [3] Matthias Leiss, Financial Market Ris of Speculative Bubbles

## Research Methods

We will run our agent-based simulations for many different market parameters and analyze the strategy distribution after a long period of time. This will allow us to make a map.
