import gspread

gc = gspread.service_account(filename="creds.json")

sh = gc.open("scraper_sample").sheet1

sh.update("A1", "Test Update")

sh.append_row(["first", "second", "third"])
