# Project overview
- **Purpose**: Trial version of a side project for my full-time job within a Scotland-based Investment Fund. 
- **Outline**: An all-in-one dashboard that allows *everyone* in the Investment Team to view, analyse, and make decisions based on quantitative data as well as internal and external research.
- **Problem**: A plethora of quantitative and qualitative research produced by Investment Analysts gets quickly dusty and forgotten about. Retreiving research is cumbersome (in disparate Word and Excel files) which is acted upon at monthly meetings.

---

# Project outline
***Note**: Internal and external processes are not reliant on one-another. External processes may fail, but there will always be a location where information is aggregated.*
1. Set up custom spreadsheets where investment analysts can input **internal** data related to:
  - Portfolio positions log ([link]()): Monitor current and past positions, qualiatively. 
  - Portfolio primer research log ([link]()): Explore past and present theses connecting investments together.
  - Company news log ([link]()): Log news coverage internally generated on portfolio companies.
  - Ongoing company meeting log ([link]()): Log meetings held with portfolio companies, non-portfolio companies, and industries.
  - ESG engagement log ([link]()): Log ESG engagements with portfolio companies, non-portfolio companies, and industries.

  *For general, durable use: must be easy to update (information), difficult to ruin (format)*

2. Build a database for **external** data collected based off internal data, which contains pricing information, among others, based on portfolio positions.

  *This must scale by be kept simple (storage may gradually become a concern)*

3. Build a series of dashboards, using Power BI, which connects all datasets together:
  - Current portfolio positions.
  - Positions review document.
  - Financial analysis (optional).

**Tools used**: 
- SQL ([code](https://github.com/mshedededen/Portfolio/blob/main/Mini-projects/Equity%20research%20dashboard/invested_companies%20code.sql)): PostgreSQL database is constructed (experience gained in pgAdmin and psql command line).
- Python ([code](https://github.com/mshedededen/Portfolio/blob/main/Mini-projects/Equity%20research%20dashboard/prices_companies_fetch.py)): Streamlined script for inserting share prices on a weekly basis.
- Microsoft Excel and VBA: Spreadsheets where analysts insert qualitative information and financial forecasts.
- Power BI ([file](https://github.com/mshedededen/Portfolio/blob/main/Mini-projects/Equity%20research%20dashboard/Equity%20research%20dashboard.pbix)): For VBA dashboard.
- uiPath: For automatic scripting.

Disclaimer: All data presented in this project is **unrelated** to my current employer, McInroy & Wood Ltd. Therefore, no breaches of confidentiality are observed.

**PowerBI dashboard shown below**

![image](https://user-images.githubusercontent.com/70542502/169715852-20deb713-2d90-46ae-befc-d034018bbc70.png)
