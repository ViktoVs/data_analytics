# for Google Drive API:
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# imports to write into google sheets
import gspread
import gspread_dataframe as gd

### Setup authentication to google sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("name_of_file")
g_client = gspread.authorize(creds)

def write_to_g_sheet(
                        df,
                        file_name,
                        tab_name
                    ):
    """
    Opens an existing g-sheet, clears the data in the given tab and writes in the
    data from the given dataframe
    :param df: Dataframe you want to write into the g-sheet
    :param file_name: Name of your g-sheet
    :param tab_name: Name of the tab in the g-sheet
    :return: success message string
    """
    ws = g_client.open(file_name).worksheet(tab_name)
    ws.clear()
    gd.set_with_dataframe(ws, df)
    return f"Written the dataframe to {filename} in tab {tab_name}"

def read_g_sheet(file_name
                 , tab_name
                ):
    """
    Open an existing tab in an existing g-sheet and save it into a pandas DataFrame
    :param file_name: Name of your g-sheet
    :param tab_name: Name of the tab in the g-sheet
    :return: pandas Dataframe containing all data from given tab
    """
    ws = g_client.open(file_name).worksheet(tab_name)
    data = ws.get_all_values()
    header = data.pop(0)
    return pd.DataFrame(data, columns=header)

def write_multiple_dfs_to_g_sheet(df_list
                                  , file_name
                                  , tab_name
                                  , vertical = False
                                 ):
    """
    Opens an existing g-sheet, clears the data in the given tab and writes in the
    data from the given dataframe list
    :param df_list: List of all Dataframes you want to write into the g-sheet
    :param file_name: Name of your g-sheet
    :param tab_name: Name of the tab in the g-sheet
    :param vertical: Defines if you want the Dataframes be inserted vertically or horizontally
    :return: success message string
    """    
    ws = g_client.open(file_name).worksheet(tab_name)
    ws.clear()
    
    r, c = (1, 1)
    for df in df_list:
        gd.set_with_dataframe(ws, df, row = r, col=c)
        if vertical:
            r = r + 2 + len(df) # add 2 plus the length of the DataFrame to the row pointer to have the startpoint for the next iteration
        else:
            c = c + 2 + len(df.columns) # add 2 plus the length of the DataFrame's columns to the columns pointer to have the startpoint for the next iteration

    return f"Written the dataframe to {filename} in tab {tab_name}"
