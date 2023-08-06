import pandas as pd
import requests
import json
import io
import time
from datetime import datetime
# from .util import yaml_cred

def fb_ad_report(token, ad_account_id, report_level, date_preset, fields= 'date_start, date_stop, account_name, campaign_name, spend', start_date='', end_date='', filtering='', time_increment=1, api_version='v15.0', wait_time=10):
    """
        Return Facebook Ads report as a Dataframe using Facebook Marketing API.
    Args:
        token (:obj:`str`, required): The Marketing API token string. This value can be read from a yaml config file.
        ad_account_id (:obj:`str`, required): Ad Account ID. Ex: '1210183442581521'
        report_level (:obj:`str`, required): 'account' or 'campaign', 'adset', or 'ad'
        fields (:obj:`str`, optional): Default value = 'date_start, date_stop, account_name, campaign_name, spend'. See the full available list of fields [here](https://developers.facebook.com/docs/marketing-api/insights/parameters/v15.0)
        date_preset (:obj:`str`, optional): This setting will be ignored when date range (`start_date` and `end_date` were input) is specified. Use one of these values: 'today', 'yesterday', 'this_month', 'last_month', 'this_quarter', 'maximum', 'data_maximum', 'last_3d', 'last_7d', 'last_14d', 'last_28d', 'last_30d', 'last_90d', etc. See the full list [here](https://developers.facebook.com/docs/marketing-api/insights/parameters#param)
        start_date (:obj:`str`, optional): Input date value in the format of YYYY-MM-D. Ex: '2022-11-13'
        end_date (:obj:`str`, optional): Input date value in the format of YYYY-MM-D. Ex: '2022-11-13'
        filtering (:obj:`str`, optional): No filtering applied as default. Read the full reference [here](https://developers.facebook.com/docs/marketing-api/insights/parameters#param)
        time_increment (:obj:`str`, optional): Default value = 1 to get the daily report data. 
        time_increment (:obj:`str`, optional): Default value = 'v15.0' as the current value. You can find the latest version by visiting the reference site [here](https://developers.facebook.com/docs/marketing-api/insights/parameters#param)
        wait_time (:obj:`int`, optional): Wait time to wait for the report to be generated as a CSV file before loading to the Dataframe. Increase wait time in seconds when you download a report with a long date range
    """
    date_range = "{'since':'" + start_date + "','until':'" + end_date + "'}"
    async_url = f"https://graph.facebook.com/{api_version}/act_{ad_account_id}/insights?level={report_level}&fields={fields}&date_preset={date_preset}&time_range={date_range}&filtering={filtering}&time_increment={time_increment}&access_token={token}"
    report_run_id = json.loads(json.dumps(requests.post(async_url).json())).get('report_run_id') # extract report_run_id
    time.sleep(wait_time) # add sleep time to wait for data download
    export_url = f"https://www.facebook.com/ads/ads_insights/export_report?report_run_id={report_run_id}&format=csv&locale=en_US&access_token={token}"
    rawData = requests.get(export_url).content
    df = pd.read_csv(io.StringIO(rawData.decode('utf-8')))
    return df
