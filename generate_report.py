#!/usr/bin/python
#
# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Retrieves a saved report or generates a new one.

To get saved reports, run get_all_saved_reports.py.

Tags: accounts.reports.generate
"""
import requests
import adsense_util
import argparse
import sys
import google.auth.exceptions
from googleapiclient import discovery


# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=True)
argparser.add_argument(
    '--report_id',
    help='The ID of the saved report to generate.')

args = argparser.parse_args()
saved_report_id = args.report_id

def main(argv):
  # Authenticate and construct service.
  credentials = adsense_util.get_adsense_credentials()
  with discovery.build('adsense', 'v2', credentials = credentials) as service:
    try:
      # Let the user pick account if more than one.
      account_id = adsense_util.get_account_id(service)

      # Retrieve report.
      if saved_report_id:
        result = service.accounts().reports().saved().generate(
            name=saved_report_id, dateRange='LAST_7_DAYS').execute()
      else:
        result = service.accounts().reports().generate(
            account=account_id, dateRange='YESTERDAY',
            metrics=['PAGE_VIEWS', 'AD_REQUESTS', 'AD_REQUESTS_COVERAGE',
                    'CLICKS', 'AD_REQUESTS_CTR', 'COST_PER_CLICK',
                    'AD_REQUESTS_RPM', 'ESTIMATED_EARNINGS','TOTAL_EARNINGS']).execute()
      # print(result)
      date = result['startDate']
      total = result['totals']['cells']
      # print(total)
      massage='GoogleAdsense每日报告\n'+str(date['year'])+'-'+str(date['month'])+'-'+str(date['day'])+'\n'+"浏览量："+total[0]['value']+"\n"+"广告请求数量："+total[1]['value']+"\n"+"广告展示率："+total[2]['value']+"\n"+"点击次数："+total[3]['value']+"\n"+"点击率："+total[4]['value']+"\n"+"每次点击出价："+total[5]['value']+"\n"+"每千次展示收益："+total[6]['value']+"\n"+"估算收入："+total[7]['value']+"\n"+"总收益："+total[8]['value']+"\n"


      # 向TG发送消息

      baseuri = 'https://api.telegram.org/bot'
      method = '/sendMessage?chat_id='
      chat_id = ""  # Userid
      token = ""  # 机器人 TOKEN
      
      # bot = telegram.Bot(token=token)
      # bot.send_message(chat_id=chat_id, text=massage)
      uri = baseuri+token+method+chat_id+'&text='+massage
      # print(uri)
      requests.get(uri)

      # # Display headers.
      # for header in result['headers']:
      #   print('%25s' % header['name'], end=''),
      # print()

      # # Display results.
      # if 'rows' in result:
      #   for row in result['rows']:
      #     for cell in row['cells']:
      #       print('%25s' % cell['value'], end='')
      # print()

      # Display date range.
      # print('Report from %s to %s.' % (result['startDate'], result['endDate']))
      # print()

    except google.auth.exceptions.RefreshError:
      print('The credentials have been revoked or expired, please delete the '
            '"%s" file and re-run the application to re-authorize.' %
            adsense_util.CREDENTIALS_FILE)


if __name__ == '__main__':
  main(sys.argv)
