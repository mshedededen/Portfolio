# Transaction recorder
def transactions_launcher():
    print("Launching transactions prompt...")
    print("Welcome. The keywords RESET, HELP, and CANCEL can be used at any point.")
    while True:
        launch_input = input("What would you like to do?\n- View transactions: Press V.\n- Record a transaction: Press R\n- Delete a transaction: Press D")
        if launch_input == "V" or launch_input == "D":
            print("Launching a view of all transactions...")
            break
            # launch transactions viewer function
        elif launch_input == "R":
            print("Launching transaction recorder...")
            # launch transactions recorder function
            transactions_recorder()
            break
        else:
            print('Invalid response. Please re-enter.')
            continue

def transactions_recorder():
    print("Launching transactions recorder...")
    transactions = dict()
    print("When prompted, please enter details")
    # Function to cycle through transactions recorder prompt
    def transactions_recorder_details(variable, question):
        while True:
            recorder_input = input(question)
            confirmation = input("Got it. For {}, adding {}. Are you sure (Y/N)?".format(variable, recorder_input))
            if confirmation == "Y":
                transactions.update({variable: recorder_input})
                break
            elif confirmation == "N":
                print("Please try again.")
                continue
            elif recorder_input == "":
                break
            else:
                print("Invalid response, please try again.")
                continue
    prompts_dict = {"Stock name": "What is the name of the stock?",
        "Date": "What date was recorded?",
        "Value": "What is the value transacted?",
        "Currency_ISO": "What is the currency ISO code? (e.g. GBP, USD, DKK)"
        }
    for key, question in prompts_dict.items():
        transactions_recorder_details(variable=key, question=question)


#transactions_launcher()
print("Success.")
transactions_recorder()
print(transactions.items())