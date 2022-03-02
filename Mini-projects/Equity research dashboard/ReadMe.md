# Project overview
- **Purpose**: Trial version of a side project for my full-time job within a Scotland-based Investment Fund. 
- **Outline**: An all-in-one dashboard that allows *everyone* in the Investment Team to view, analyse, and make decisions based on quantitative data as well as internal and external research.
- **Problem**: A plethora of quantitative and qualitative research produced by Investment Analysts gets quickly dusty and forgotten about. Retreiving research is cumbersome (in disparate Word and Excel files) which is acted upon at monthly meetings.

---

# Project outline
1. Build a database containing: **1)** a list of 'preferred' stocks; **2)** stock data that is automatically ingested; and **3)** ad-hoc investment thesis data.
2. Set up a custom spreadsheet where analysts - who typically only know how to use Excel and nothing else - can input ongoing company news data with ease.
3. Build a dashboard (Power BI) connecting all datasets together.
4. (optional) Enable analysts' company forecasts (DCF, multiples, comps) and company financials to be viewed in the same dashboard.

**Tools used**: 
- SQL ([code](https://github.com/mshedededen/Portfolio/blob/main/Mini-projects/Equity%20research%20dashboard/invested_companies%20code.sql)): PostgreSQL database is constructed (experience gained in pgAdmin and psql command line).
- Python ([code](https://github.com/mshedededen/Portfolio/blob/main/Mini-projects/Equity%20research%20dashboard/prices_companies_fetch.py)): Streamlined script for inserting share prices on a weekly basis.
- Microsoft Excel and VBA: Spreadsheets where analysts insert qualitative information and financial forecasts.
- Power BI ([file](https://github.com/mshedededen/Portfolio/blob/main/Mini-projects/Equity%20research%20dashboard/Equity%20research%20dashboard.pbix)): For VBA dashboard.
- uiPath: For automatic scripting.

Disclaimer: All data presented in this project is **unrelated** to my current employer, McInroy & Wood Ltd. Therefore, no breaches of confidentiality are observed.
