def get_data(item_id, data):
    item_id = int(item_id)
    item = None
    for i in data:
        if i['ID'] == item_id:
            item = {
                'id': item_id,
                'description': i['Description'],
                'amount': i['Amount'],
                'method': i['Method'],
                'date': i['Date'],
            }
    return item


def get_total(arr):
    total = 0
    for t in arr:
        total += t['Amount']

    return total


def unpack_data(form_data):
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
