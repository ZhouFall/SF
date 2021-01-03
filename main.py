import requests
import json
from time import sleep
import pandas as pd

headers = {
'Connection': 'keep-alive',
'Cookie': '',
'Host': 'www.sf-express.com',
'Referer': 'https://www.sf-express.com/cn/sc/dynamic_function/waybill/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
}

para = {
    'lang': 'sc',
    'region': 'cn',
    'translate':'',
    'pageNo': '1',
    'pageRows': '10',
}

url = 'https://www.sf-express.com/sf-service-core-web/service/waybills/list/send'

waybillinfos = []

def get_page_content():
    res = requests.get(url=url,headers=headers,params=para)
    with open('result.json','wb') as f:
        f.write(res.text.encode())

def parse_page_info():
    filepath = r'result.json'
    # 打开文件的时候加上打开编码格式
    with open(filepath, 'r', encoding='utf-8') as f:
        dict = json.load(f)
    waybillno_list = dict['result']['content']
    for item in waybillno_list:
        waybillinfo = []
        waybillinfo.append(item['waybillno'])
        waybillinfo.append(item['originateContacts'])
        waybillinfo.append(item['destinationContacts'])
        waybillinfos.append(waybillinfo)

if __name__ == "__main__":
    for i in range(1,10):
        para['pageNo'] = str(i)
        get_page_content()
        parse_page_info()
        print('第{}页快递单号爬取结束'.format(i))
        sleep(1)
    dataframe = pd.DataFrame(waybillinfos)
    dataframe.columns = ['快递单号', '寄件人', '收件人']
    dataframe.to_excel('result.xls',index=False)
    print(dataframe)