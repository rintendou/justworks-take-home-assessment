def set_all(transaction_data, amount):
    transaction_data['minBalance'] = amount
    transaction_data['maxBalance'] = amount
    transaction_data['endingBalance'] = amount


def set_end(accounts, queried_row, amount):
    customer_id = queried_row.iat[0, 0] # Get queried row's ID
    date = queried_row.iat[0, 1]  # Get  queried row's MM/YYYY
    ending_balance = queried_row.iat[0, 4]  # Get current ending balance
    print(customer_id)
    print(date)
    print(ending_balance)

    if amount >= 0:  # Credit transaction
        ending_balance += amount
    else:  # Debit transaction
        ending_balance -= amount

    accounts.loc[(accounts['customerID'] == customer_id) & (accounts['MM/YYYY'] == date)] = ending_balance


def set_min(accounts, queried_row, amount):
    current_min = queried_row['minBalance']
    queried_row['minBalance'] = amount


def set_max(accounts, queried_row, amount):
    queried_row['maxBalance'] = amount
