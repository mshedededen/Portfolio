# Project overview

**Purpose**: Trial version of a project I am doing as part of my full-time job within a Scotland-based Investment Fund. The aim is to build a database comprising of tables which ingest **1)** stock data; **2)** ad-hoc investment thesis data; and **3)** ongoing company news data. Thereafter, data will be fed into a dashboard to provide an interface which allows members of the investment team to easily track performance and (if desired) updated investment theses.

**Tools used**: SQL (Postgres database), Python (incl. Quandl package), Microsoft Excel (for qualitative data), Power BI (for dashboard), "UNKNOWN" (for automating scripting).

**Contents**:
...


**Initial Plan**:
1.  Build a table (qualitative) of companies that we invest in. The column headings will be *ticker* **(primary key)**, *company_name*, *country_listed*, *date_first_investment*, *date_sold_investment*.
2.  Build a table (quantitative) including prices (daily close) of invested companies. The column headings will be *ticker*, *date*, *price_close*.
    N.B. I want this table to be updated automatically on a weekly basis. Therefore I need code which fetches prices and appends to current table.
3.  Build a table (qualitative) including Investment thesis. The column headings will be *ticker*, *date_update*, *thesis*, *risks*, *about_company*.
4.  Build a table (qualitative) including Company News. The column headings will be *ticker*, *date*, *company_news*.

Disclaimer: All data presented in this project is **unrelated** to my current employer, McInroy & Wood Ltd. Therefore, no breaches of confidentiality are met.
