import requests
import io
# import json
import os
import pandas as pd
from .util import lmt_detect

def appsflyer_report(token_key, app_id, report_type, start_date, end_date, api_version='v5'):
  """
  Export AppsFlyer Data to csv and save on your local machine.
  Args:
      token_key (:obj:`str`, required): AppsFlyer token key
      app_id (:obj:`str`, required): ID of your app. Ex: 'com.moneytap.vn.app','id1522245972'
      report_type (:obj: `str`, required): One of available AppsFlyer reports. Ex: 'installs_report', 'installs_report', 'in_app_events_report', 'organic_installs_report', 'organic_in_app_events_report', 'blocked_installs_report', 'blocked_in_app_events_report', 'detection', 'fraud-post-inapps'
      start_date (:obj: `str`, required): Using '%Y-%m-%d' format. Ex: '2022-09-25'
      end_date (:obj: `str`, required): Using '%Y-%m-%d' format. Ex: '2022-09-25'
      export_path (:obj: `str`, required): Local path to save the export file.
      api_version (:obj: `str`, optional): Leave it as is. See more: https://support.appsflyer.com/hc/en-us/articles/207034346-Aggregate-data-via-Pull-API-in-real-time#pull-api-for-developers
  """
  request_url = 'https://hq.appsflyer.com/export/{}/{}/{}'.format(app_id, report_type, api_version)
  params = {
      'api_token': '{}'.format(token_key),
      'from': '{}'.format(start_date),
      'to': '{}'.format(end_date)
    }
  res = requests.get(request_url, params=params)
  if res.status_code != 200:
    if res.status_code == 404:
      print('There is a problem with the request URL. Make sure that it is correct')
    else:
      print('There was a problem retrieving data: ', res.text)
  else:
    rawData = res.content
    df = pd.read_csv(io.StringIO(rawData.decode('utf-8')))
  return df