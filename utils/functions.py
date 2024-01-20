import openpyxl
import os
from utils.database import Database

db = Database("data/db.sqlite3")


def add_plus(number: str) -> str:
    if number.startswith("+"):
        return number
    return "+" + number


def get_salary(number):
    book = openpyxl.load_workbook("data/data.xlsx", read_only=True)
    try:
        sheet = book.active
        info = {}
        for item in range(1, sheet.max_row + 1):
            if sheet[item][0].value == number:
                for item2 in range(0, sheet.max_column):
                    if sheet[item][item2].value:
                        info[sheet[3][item2].value] = sheet[item][item2].value
                    else:
                        continue
                break
        if not info:
            return "<b>Hisob topilmadi!</b>"
        else:
            text = "\n".join([f"<b>{key}</b>:  {value}" for key, value in info.items()])
            return text
    finally:
        book.close()


def add_user(userid, username, lastname):
    if not db.user_exists(userid):
        db.add_user(userid, username, lastname)


def save_file(filepath):
    if os.path.exists("data/data.xlsx"):
        try:
            os.remove("data/data.xlsx")
        except Exception as ex:
            return f"<b>error: {str(ex)}</b>"
    with open(f'data/data.xlsx', 'wb') as new_file:
        new_file.write(filepath.read())
        return "<b>Файл сохранен успешно!</b>"
