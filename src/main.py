import pandas as pd
import numpy as np

import os
import os.path

import format_date as formatter
import set_balance as bal

# Navigate to the parent directory
PARENT_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Construct the path to input.csv & output.csv
INPUT_PATH = os.path.join(PARENT_DIRECTORY, 'data', 'transactions.csv')
OUTPUT_PATH = os.path.join(PARENT_DIRECTORY, 'data', 'accounts.csv')

transactions = pd.read_csv(INPUT_PATH, delimiter=',')
accounts = pd.DataFrame(
    columns=['customerID', 'MM/YYYY', 'minBalance', 'maxBalance', 'endingBalance'])

minBalance = 0
maxBalance = 0
endingBalance = 0

for index, row in transactions.iterrows():
    customer_id = row['customerID']
    date = formatter.convert_date(row['date'])
    amount = row['amount']

    transaction_data = {
        "customerID": customer_id,
        "MM/YYYY": date,
        "minBalance": minBalance,
        "maxBalance": maxBalance,
        "endingBalance": endingBalance
    }

    # Case 1: CustomerID already exists
    if (customer_id in accounts['customerID'].values):
        # print("Case 1")
        selected_row = accounts[accounts['customerID'] == customer_id]
        # Case 1a: CustomerID and MM/YYYY already exists, only need to update balances
        if date in selected_row['MM/YYYY'].values:
            queried_row = accounts.query('customerID == @customer_id & `MM/YYYY` == @date')
            print(queried_row)

            bal.set_end(accounts, queried_row, amount)

            # print("Case 1a", '\n')
        else: # Case 1b: CustomerID exists but the MM/YYYY doesn't, need to write new entry for it
            accounts.loc[index] = transaction_data
            accounts.to_csv(OUTPUT_PATH, index=False)
            # print("Case 1b", '\n')
    else: # Case 2: CustomerID does not exist, therefore need to write new entry for it
        bal.set_all(transaction_data, amount)
        accounts.loc[index] = transaction_data
        accounts.to_csv(OUTPUT_PATH, index=False)
        print("Case 2", '\n')