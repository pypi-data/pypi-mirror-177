
from __future__ import print_function

import os.path


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from crgoauth.auth import Auth



# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Ni5B7zolPKD2J0CXQSaLec31AXw8HpcdM_xPJKPILRw' #'1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Rechnung!F5:G8'

def main():
    """ Shw basic usage of the Sheets API.
        Prints values from a sample spreadsheet
    """
    auth = Auth()
    creds = auth.get()

    print(os.getcwd())
    
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        
        print('result:', result)

        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[1], row[0]))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
