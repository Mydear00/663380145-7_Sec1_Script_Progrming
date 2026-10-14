"""Placeholder for a future Google Sheets API integration.

This module intentionally does not connect to Google Sheets. A real integration
requires Google Cloud setup, API credentials, and the gspread/google-auth packages.
"""
class GoogleSheetsUtils:
    def __init__(self):
        self.connected = False

    def read_sheet(self, spreadsheet_id, range_name):
        raise NotImplementedError("Google Sheets API ยังไม่ได้ตั้งค่า")

    def write_sheet(self, spreadsheet_id, sheet_name, data, start_cell="A1"):
        raise NotImplementedError("Google Sheets API ยังไม่ได้ตั้งค่า")
