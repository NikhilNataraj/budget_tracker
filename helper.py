def get_total(arr):
    """Calculates the sum of amounts from a list of transactions."""
    total = 0
    for t in arr:
        # SQLite returns data with lowercase keys
        total += t['amount']
    return total


def unpack_data(form_data):
    """Extracts and formats data from a submitted form."""
    description = form_data.get('description')
    amount = float(form_data.get('amount'))
    method = form_data.get('method')
    tran_date = form_data.get('date')
    data = {
        "date": tran_date,
        "description": description,
        "amount": amount,
        "method": method
    }
    return data
