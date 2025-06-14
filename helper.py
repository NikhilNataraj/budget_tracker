def get_data(item_id, data):
    item_id = int(item_id)
    item = None
    for i in data:
        if i['id'] == item_id:
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
