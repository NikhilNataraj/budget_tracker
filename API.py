import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SHEETS_API")


# === 1. READ (GET) ===
def read_data(sheet):
    params = {
        'action': 'read',
        'sheet': sheet
    }
    response = requests.get(BASE_URL, params=params)
    print(response.json())


expense_data = read_data("Expenses")
print(type(expense_data))
# data_dict_arr = []
# for index in range(len(expense_data)):
#     if index > 0:
#         data_dict_arr.append({
#             'ID': expense_data[index][0],
#             'Date': expense_data[index][1],
#             'Description': expense_data[index][2],
#             'Amount': expense_data[index][3],
#             'Method': expense_data[index][4]
#         })


# === 2. CREATE ROW (POST) ===
def create_row(sheet, info):
    data = {
        "action": "create",
        "sheet": sheet,
        "data": info
        # "data": {
        #     "Date": "03-06-2025",
        #     "Description": "Test",
        #     "Amount": 101,
        #     "Method": "Card"
        # }
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# create_row("Expenses")


# === 3. UPDATE ROW (POST) ===
def update_row(sheet, row, info):
    data = {
        "action": "update",
        "sheet": sheet,
        "row": row,
        "data": info
        # "data": {
        #     "Date": "03-06-2025",
        #     "Description": "Test",
        #     "Amount": 101,
        #     "Method": "Cash"
        # }
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# update_row("Expenses", 4)


# === 4. DELETE ROW (POST) ===
def delete_row(sheet, row):
    data = {
        "action": "delete",
        "sheet": sheet,
        "row": row
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# delete_row("Expenses", 4)


# === 5. CREATE NEW SHEET (POST) ===
def create_sheet(new_name):
    data = {
        "action": "createSheet",
        "newSheetName": new_name
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# create_sheet("CreditCard")


# === 6. DELETE SHEET (POST) ===
def delete_sheet(sheet_name):
    data = {
        "action": "deleteSheet",
        "sheetToDelete": sheet_name
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# delete_sheet("CreditCard")