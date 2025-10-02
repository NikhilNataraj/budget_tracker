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
    return response.json()


# === 2. CREATE ROW (POST) ===
def create_row(sheet, info):
    data = {
        "action": "create",
        "sheet": sheet,
        "data": info
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# === 3. UPDATE ROW (POST) ===
def update_row(sheet, row, info):
    data = {
        "action": "update",
        "sheet": sheet,
        "row": row,
        "data": info
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# === 4. DELETE ROW (POST) ===
def delete_row(sheet, row):
    data = {
        "action": "delete",
        "sheet": sheet,
        "row": row
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# === 5. CREATE NEW SHEET (POST) ===
def create_sheet(new_name):
    data = {
        "action": "createSheet",
        "newSheetName": new_name
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


# === 6. DELETE SHEET (POST) ===
def delete_sheet(sheet_name):
    data = {
        "action": "deleteSheet",
        "sheetToDelete": sheet_name
    }
    response = requests.post(BASE_URL, json=data)
    print(response.text)


def convert_to_dict(data):
    """
    Function to convert data from list to list of dictionaries for income and expense data
    :param data: list
    :return: list of dictionaries
    """
    data_dict_arr = []
    for index in range(len(data)):
        if index > 0:
            data_dict_arr.append({
                'ID': data[index][0],
                'Date': data[index][1],
                'Description': data[index][2],
                'Amount': data[index][3],
                'Method': data[index][4]
            })
    return data_dict_arr
