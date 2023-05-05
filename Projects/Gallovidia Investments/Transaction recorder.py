import datetime as dt

class Gallovidia:
    class TransactionsRecord:
        """Class to handle the transactions record of Gallovidia Investments.
        """
        def __init__(self):
            self.path = 'C:/Users/PC/OneDrive/GALLOVIDIA INVESTMENTS/Miscellaneous/Transactions/'
        def recordTransaction(self):
            """Records a transaction.
            """

            # 1. Check if transaction is a flow (cash transaction) or a security transaction.
            while True:
                transaction_type = (input("Is this a cash (flow) transaction or a security transaction? \
                                          (cash/security): ")
                                    .lower())
            # 2. Check further details of transaction
                if transaction_type == "cash":
                    print("Processing as cash transaction.")
                    transaction_subtype = input("Is this a deposit, withdrawal, or investment income (e.g. dividends) ? \
                                                (deposit/withdrawal/income): ")
                    break
                elif transaction_type == "security":
                    print("Processing as security transaction.")
                    transaction_subtype = input("Is this a buy or sell? (buy/sell): ")
                    break
                else:
                    print("Invalid input. Please enter 'cash' or 'security'.")
                    continue
            

            # 3. Record transaction.
            # 3.1 Define question sets, in dictionary format
            # 3.1.1 Cash transaction question set
            question_set_cash = {
                "date": "Enter transaction date (YYYY-MM-DD): ",
                "date_of_entry": dt.datetime.now().strftime("%Y-%m-%d"),
                "account": "Enter account name: ",
                "value": "Enter value of transaction: ",
                "currency_ISO": "Enter the currency ISO: ",
                "fx_rate": "Enter FX rate (if applicable): ",
                "fees": "Enter fees (if applicable): "
                }
            # 3.1.2 Security transaction question set
            question_set_security = {
                "date": "Enter transaction date (YYYY-MM-DD): ",
                "date_of_entry": dt.datetime.now().strftime("%Y-%m-%d"),
                "account": "Enter account name: ",
                "security": "Enter security name: ",
                "ticker": "Enter ticker symbol (e.g. MSFT for Microsoft): ",
                "exchange country": "Enter country of exchange: ",
                "value": "Enter value of transaction: ",
                "quantity": "Enter quantity: ",
                "price": "Enter price: (optional)",
                "currency_ISO": "Enter the currency ISO: ",
                "fx_rate": "Enter FX rate (if applicable): ",
                "fees": "Enter fees (if applicable): "
                }
            # 3.1.3 Security transaction question set (dividend)
            question_set_security_dividend = question_set_cash.update(question_set_security)




            # 1.1 Different sets of questions will be available depending on the type of transaction.
            question_set_cash = ["date", "account", "value", "currency_ISO", "fx_rate", "fees"]
            question_set_security = ["date", "account", "security", "ticker", "exchange country", "value", "quantity",
                                     "price", "type", "currency_ISO", "fx_rate", "fees"]
            

            # 2. Begin recording transaction.



            # Enter transaction details as a json object.
            transaction = {
                "date": input("Enter transaction date (YYYY-MM-DD): "),
                "account": input("Enter account name: "),
                "security": input("Enter security name: "),
                "ticker": input("Enter ticker symbol (e.g. MSFT for Microsoft)"),
                "exchange country": input("Enter country of exchange"),
                "value": input("Enter value of transaction: "),
                "quantity": input("Enter quantity: "),
                "price": input("Enter price: "),
                "type": input("Enter transaction type (buy/sell/dividend): "),
                "currency_ISO": input("Enter the currency ISO"),
                "fx_rate": input("Enter FX rate (if applicable): "),
                "fees": input("Enter fees (if applicable): ")
                }