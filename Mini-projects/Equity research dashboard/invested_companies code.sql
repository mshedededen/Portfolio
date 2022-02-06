/* CREATE invested_companies TABLE*/
CREATE TABLE invested_companies (
    ticker TEXT NOT NULL,
    company_name TEXT NOT NULL,
    country_listed TEXT NOT NULL,
    date_first_investment DATE NOT NULL,
    date_sold_investment DATE
);

/* IMPORT .csv FILE INTO invested_companies*/
/*USING psql*/
\c equity_research_dashboard
\copy invested_companies
FROM 'C:\Users\shedd\Documents\MyLearning\Data Science\DS Projects\Equity research dashboard\Invested_companies.csv'
DELIMITER ','
CSV HEADER;


/* testing data upload with a simple query*/
SELECT * FROM invested_companies WHERE date_sold_investment IS NULL;