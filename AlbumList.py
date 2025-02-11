import gspread
from datetime import date, datetime

class AlbumList:
    def __init__(self, login_file, sheet_key):
        self.gs = gspread.service_account(login_file)
        self.sheet = self.gs.open_by_key(key=sheet_key).sheet1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.sheet
        del self.gs

    def get_row(self, index):
        row = self.sheet.row_values(index)
        date_parts = row[4].split('/')

        row_dict = {
            'Timestamp': datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S'),
            'Artist': row[1],
            'Album': row[2],
            'Release_Year': row[3],
            'Listened_Date': date(int(date_parts[2]), int(date_parts[0]), int(date_parts[1])),
            'Link': row[5]
        }

        return row_dict
    
    def get_last_row(self):
        return self.get_row(self.sheet.row_count)