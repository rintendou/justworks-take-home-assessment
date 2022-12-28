def set_all(transaction_data, amount):
    transaction_data['minBalance'] = amount
    transaction_data['maxBalance'] = amount
    transaction_data['endingBalance'] = amount


def set_end(queried_row, amount):
    ending_balance = queried_row.iat[0, 4]  # Get current ending balance

    if amount >= 0:  # Credit transaction
        ending_balance += amount
    else:  # Debit transaction
        ending_balance -= amount

    return ending_balance


def set_min(queried_row):
    current_min = queried_row.iat[0, 2]  # Get current minBalance
    current_end = queried_row.iat[0, 4]  # Get current endingBalance

    if current_min > current_end:
        current_min = current_end
        return current_min
    else:
        return current_min


def set_max(queried_row):
    current_max = queried_row.iat[0, 3]  # Get current maxBalance
    current_end = queried_row.iat[0, 4] # Get current endingBalance

    if current_max < current_end:
        current_max = current_end
        return current_max
    else:
        return current_max
