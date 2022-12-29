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

for i, transactions_row in transactions.iterrows():
    t_customer_id = transactions_row['customerID']
    t_date = formatter.convert_date(transactions_row['date'])
    t_amount = transactions_row['amount']

    transaction_data = {
        "customerID": t_customer_id,
        "MM/YYYY": t_date,
        "minBalance": minBalance,
        "maxBalance": maxBalance,
        "endingBalance": endingBalance
    }

    # Edge case: CSV is empty, write the first entry into CSV
    if accounts.empty: 
        bal.set_all(transaction_data, t_amount)
        accounts.loc[i] = transaction_data
        accounts.to_csv(OUTPUT_PATH, index=False)
        # print("Edge case occured")
    else:
        customerID_query = accounts.query('customerID == @t_customer_id')

        # Case 0: If the customerID_query returns an empty dataframe, then customerID doesn't exist yet.
        if customerID_query.empty:
            accounts.loc[i] = transaction_data
        else: 
            date_query = accounts.query('customerID == @t_customer_id & `MM/YYYY` == @t_date')

            # Case 0a: If the customer_query is able to return a dataframe, requery with the addition of the date. If the requery returns an empty dataframe, then the customerID exists but not a date.

            if date_query.empty:
                bal.set_all(transaction_data, t_amount)
                accounts.loc[i] = transaction_data
                accounts.to_csv(OUTPUT_PATH, index=False)
                # print("Case 0a occured")

            # Case 0b: If the customer_query is able to return a dataframe and the requery was able to locate a date too.
            else:
                date_query['endingBalance'] = bal.set_end(date_query, t_amount)
                date_query['minBalance'] = bal.set_min(date_query)
                date_query['maxBalance'] = bal.set_max(date_query)

                index = accounts.index[(accounts['customerID'] == t_customer_id) & (accounts['MM/YYYY'] == t_date)]

                accounts.loc[index] = date_query
                accounts.to_csv(OUTPUT_PATH, index=False)