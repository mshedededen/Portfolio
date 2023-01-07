# Data Science Portfolio | Matthew Shedden
This GitHub repository contains data science portfolio projects I have conducted. These range in scope and are often centred around other interests of mine, such as football, investing.

Some work-in-progress notebooks can be found on [Kaggle](https://www.kaggle.com/mattshedden).

**Code base**: Python, R, SQL, Bash, Powershell.

**Software**: PostgreSQL, Git, Microsoft Excel (yes, it's a basic but it's how 95% of white-collar workers interact with data).

## Data analytics
### English Premier League results, analysis
*(Python)*

Exploratory data analysis is performed on EPL results, forked from [Stoijkovic, et al.](https://github.com/datasets/football-datasets). The **first** objective is to transform the data into a readable format, before trends in results and determinant factors of match results are identified. **Second**, a Shallow Regressor is created to predict the correct number of goals scored based upon other match-related statistics. **Third**, a Shallow Classifier is created to predict the correct outcome of the game for each team, based upon match statistics and previous results.
- The Python notebook is available on [**here on Kaggle**](https://www.kaggle.com/mattshedden/english-premier-league-results-analysis).

## Machine Learning
### Tender classification, Natural Language Processing
*(Python)*

An Deep Learning project using Natural Language Processing ("NLP") on Tender Searches for an anonymised government contract tendering organisation in German. The project makes use of DL libraries including Keras / Tensorflow as well as SciKit-Learn for text tokenization.
- The Python notebook is provided [**here**](https://github.com/mshedededen/Portfolio/blob/main/Python-ML/Tender%20classification%20notebook%2C%20NLP.ipynb).
### Portfolio Optimisation (Markowitz Portfolio Theory), Genetic Algorithms
*(R)*

Genetic Algorithms are an optimization and Machine Learning method that applies Neo-Darwinism evolutionary theory to perform an exhaustive search of all possible combinations. Genetic Algorithms have a variety of use-cases, from the [Knapsack Problem](https://en.wikipedia.org/wiki/Knapsack_problem) to Portfolio Optimisation, which shall be explored here. The aim of this project is to use R and Genetic Algorithms to find the best possible weighting of a basket of stocks, given a specific level of risk tolerance.
- The R notebook is provided [**here**](https://github.com/mshedededen/Portfolio/blob/main/R-GeneticProgramming/Portfolio%20Optimization%20(Markowitz)%20using%20Genetic%20Algorithms%20in%20R.ipynb).

## Data engineering
### Web scraping jobs on Indeed
*(Python)*

This project is inspired by job hunting in anticipation for finishing my postgraduate studies. Finding the right job is time-consuming. Therefore, this project has dual benefit of increasing the efficiency by which I find jobs as well as improving my abilities in web scraping. The aim of this project is to build an ETL pipeline that scrapes jobs from Indeed.com which match keyword findings across various roles.
- The Python notebook is provided [**here**](https://github.com/mshedededen/Portfolio/blob/main/Python-WebScraping/Job%20scraper.ipynb).

## End-to-end projects
- **Friendly reminder**: Python script to help users keep track of friends who they have contacted recently and those who they should maybe reach out to.
- **Investment Management Workflow**: Related to my day job (Investment Management), the underlying software that is used to track transactions, performance, costs & charges, etc. is - underneath - just a collection of databases. Therefore, this projects is my curiosity if I can build a similar piece of software - albeit without the UI.