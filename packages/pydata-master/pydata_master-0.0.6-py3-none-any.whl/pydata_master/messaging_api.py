import requests
import json
import os
from .util import lmt_detect

# SLACK API
def slack_send_file(token_key, slack_channel, text_comment, file_path, title=None):
  """
  Send a file to a Slack channel using either a bot or a user token
  Args:
      token_key (:obj:`str`, required): a bot token (start with 'xoxb-..') or a user token (start with 'xoxp-..')
      slack_channel (:obj:`str`, required): name of the target channel. Ex: '#mkt_daily_tracking'
      text_comment (:obj:`str`, required): The text comment for your file.
      file_path (:obj:`str`, required): The path to your target file
  """
  file_name = file_path.split(lmt_detect())[-1]
  file_type = file_name.split('.')[-1]
  file_bytes = open(file_path,'rb').read()
  url = 'https://slack.com/api/files.upload'
  payload =  {'token': token_key,
              'filename': file_name,
              'channels': slack_channel,
            'fi1letype': file_type,
              'initial_comment': text_comment,
              'title': title
              }
  r = requests.post(url, payload, files={ 'file': file_bytes })
  return r.json()


def slack_send_message (token_key, slack_channel, message):
  """
  Send a file to a Slack channel using either a bot or a user token
  Args:
      token_key (:obj:`str`, required): a bot token (start with 'xoxb-..') or a user token (start with 'xoxp-..')
      slack_channel (:obj:`str`, required): name of the target channel. Ex: '#mkt_daily_tracking'
      message (:obj:`str`, required): The text message for your file.
  """
  header = {'Content-type': 'application/json; charset=utf-8',
          'Authorization': 'Bearer {}'.format(token_key)
          }
  payload = json.dumps({
    "channel": "{}".format(slack_channel),
    "text": "{}".format(message)
    })
  r = requests.post('https://slack.com/api/chat.postMessage',
      data=payload, headers = header)
  return r.json()

# TELEGRAM API
def telegram_send_photo(token_key, chat_id, message, file_path):
    """
    Send a file to a Telegram group.
    Args:
        token_key (:obj:`str`, required): telegram token key
        chat_id (:obj:`str`, required): id of the target telegram channel/group. Ex: '-1001439492355'
        message (:obj:`str`, required): Your text message.
        file_path (:obj:`str`, required): path of your file/photo to send via telegram.
    """
    file_name = file_path.split(lmt_detect())[-1]
    file_type = file_name.split('.')[-1]  
    files=[('photo',(file_name, open(file_path,'rb'),'image/{}'.format(file_type)))]
    url = 'https://api.telegram.org/{}/sendPhoto'.format(token_key)
    payload = {'chat_id': chat_id,'caption': message}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response

def telegram_send_message(token_key, chat_id, message):
    """
    Send a message to a Telegram group.
    Args:
        token_key (:obj:`str`, required): telegram token key
        chat_id (:obj:`str`, required): id of the target telegram channel/group. Ex: '-1001439492355'
        message (:obj:`str`, required): Your text message.
    """
    tel_url = 'https://api.telegram.org/{}/sendMessage?chat_id={}&text={}'.format(token_key, chat_id, message)
    return requests.post(tel_url)