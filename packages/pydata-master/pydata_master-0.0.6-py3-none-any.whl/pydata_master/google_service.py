# Copyright 2022 Thinh Vu @ GitHub
# See LICENSE for details.
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from df2gspread import df2gspread as d2g

from google.oauth2 import service_account # to use gg search console
from googleapiclient.discovery import build
import json
import requests

# Authentication
def google_auth(json_cred_path):
    """
    Return a creds and gc to use Authenticate the Google service
    Args:
        json_cred_path (:obj:`str`, required): The path to the service account credential in json format.
    """
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_cred_path, scope)
    gc = gspread.authorize(creds)
    return creds, gc

# Google Sheets
def read_gsheet(sheet_id, sheet_name, gc):
    """
    Read a Google Sheets file to return a DataFrame. Given the fact that the target Google Sheets file has been shared to your Google Service Account.
    Args:
        sheet_id (:obj:`str`, required): Google Sheets ID. Ex: `YOUR_SHEET_ID` in the URI`https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
        sheet_name (:obj:`str`, required): Name of the worksheet
        gc (:obj, required): gc be assigned as to the result of google_auth() function.
    """
    wks = gc.open_by_key(sheet_id)
    worksheet = wks.worksheet(sheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def save_gsheet (dataframe, sheet_id, sheet_name, creds, row_names=False, clean=False, df_size=False, start_cell='A1'):
    """
    Export a DataFrame to Google Sheets file. Given the fact that the target Google Sheets file has been shared to your Google Service Account.
    Args:
        sheet_id (:obj, required): Target DataFrame to export.
        sheet_id (:obj:`str`, required): Google Sheets ID. Ex: `YOUR_SHEET_ID` in the URI`https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
        sheet_name (:obj:`str`, required): Name of the worksheet
        creds (:obj, required): creds be assigned as to the result of google_auth() function.
        rows_name (:obj:`boolean`, required): False as the default value.
        clean (:obj, required): False as the default value.
        df_size(:obj, required): False as the default value.
        start_cell (:obj, required): 'A1' as the default value.
    """
    d2g.upload(dataframe, sheet_id, sheet_name, credentials=creds, row_names=row_names, clean = clean, df_size = df_size, start_cell=start_cell)
    'https://docs.google.com/spreadsheets/d/' + sheet_id

def save_gspread (dataframe, sheet_id, sheet_name, gc):
    """
    Read a Google Sheets file to return a DataFrame. Given the fact that the target Google Sheets file has been shared to your Google Service Account.
    Args:
        sheet_id (:obj:`str`, required): Google Sheets ID. Ex: `YOUR_SHEET_ID` in the URI`https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
        sheet_name (:obj:`str`, required): Name of the worksheet
        gc (:obj, required): gc be assigned as to the result of google_auth() function.
    """
    try:
        wks = gc.open_by_key(sheet_id)
        wks.worksheet(sheet_name).update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        message = 'Data Frame has been exported to https://docs.google.com/spreadsheets/d/' + sheet_id
    except:
        wks = gc.open_by_key(sheet_id)
        rows, columns = dataframe.shape
        wks.add_worksheet(title=sheet_name, rows=rows, cols=columns)
        wks.worksheet(sheet_name).update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        message = 'Data Frame has been exported to https://docs.google.com/spreadsheets/d/' + sheet_id
    return message

# Google Search Console
def connect(key):
    """Create a connection to the Google Search Console API and return service object.
    Args:
        key (string): Google Search Console JSON client secrets path.
    """
    scope = ['https://www.googleapis.com/auth/webmasters']
    credentials = service_account.Credentials.from_service_account_file(key, scopes=scope)
    service = build(
        'searchconsole',
        'v1',
        credentials=credentials
    )
    return service

def query(service, site_url, payload):
    """Run a query on the Google Search Console API and return a dataframe of results.
    Args:
        service (object): Service object from connect()
        site_url (string): URL of Google Search Console property
        payload (dict): API query payload dictionary    
    """
    response = service.searchanalytics().query(siteUrl=site_url, body=payload).execute()
    results = []
    for row in response['rows']:    
        data = {}
        for i in range(len(payload['dimensions'])):
            data[payload['dimensions'][i]] = row['keys'][i]
        data['clicks'] = row['clicks']
        data['impressions'] = row['impressions']
        data['ctr'] = round(row['ctr'] * 100, 2)
        data['position'] = round(row['position'], 2)        
        results.append(data)
    return pd.DataFrame.from_dict(results)

def search_analysis_extract(key, site_url, start_date, end_date, dimension=["date","page","device","query"], limit=1000, start=0):
    """Extract Google Search Console data to a dataframe using connect and query functions defined above.
    Args:
        key (:obj:`str`, required): Google Search Console JSON client secrets path.
        site_url (:obj:`str`, required): URL of Google Search Console property
        start_date (:obj:`str`, required): Start date to extract data
        end_date (:obj:`str`, required): Start date to extract data
        dimension (:obj:`list`, optional): Available dimension: date, page, device, query, search-appearance (this one can only sit standalone). Default value =  ["date","page","device","query"]
        limit (:obj:`int`, optional): Maximum limit is 25000. Default value = 1000.
        start (:obj:`int`, optional): Start from the first result, default value = 0. 
    """
    service = connect(key)
    payload = {
        'startDate': f"{start_date}",
        'endDate': f"{end_date}",
        'dimensions': dimension, # 'search-appearance' can only sit standalone
        'rowLimit': f"{limit}",
        'startRow': f"{start}"
    }
    site_url = f"{site_url}"
    df = query(service, site_url, payload)
    return df