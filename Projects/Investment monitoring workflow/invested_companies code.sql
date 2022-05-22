/* CREATE prices_companies TABLE */
CREATE TABLE prices_companies (
    ticker TEXT NOT NULL,
    price_date DATE NOT NULL,
    price_close NUMERIC             /* prices can be null, should markets be closed on a given date */
);

