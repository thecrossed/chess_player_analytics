class GoogleSheet():
    def __init__(self, url, creds):
        self.url = url
        self.creds = creds
        
    def upload_df(self, df, sheet_url):
        """
        purpose:
        upload df to google sheet RCC_chess_game_result
        each class/csv/file represent one sheet
        
        input - 
        name: class name, sheet tab
        df: df that will be uploaded for each tab
        """
        #spreadsheet_key = '12R6hwzKys_DQE6vFpuOLGpe68hGHktSzd65AkR0nOsA' # sheet url from RCC_chess_game_result
        scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
        wks_name = name
        df = rp_nan_empty(df)
        d2g.upload(df, sheet_url, wks_name, credentials=creds)  