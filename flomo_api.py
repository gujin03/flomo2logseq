# encoding:utf-8
import requests
import json
import pandas as pd
import os
import openpyxl
import re
'''
    这个小程序的0.1版本主要是利用2022年清明节假期完成的，实现了从flomo自动导出卡片到logseq
'''

def flomo_data():
    url_home = 'https://flomoapp.com/api/user/76676/stat/?tz=8:0'
    url = "https://flomoapp.com/api/memo/?tz=8:0"
    # url = "https://flomoapp.com/api/memo/?tag=zk&tz=8:0"
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br',
        'cookie': '' #请修改此处
        'referer': 'https://flomoapp.com/mine?tag=inbox',
        'user-agent': 'Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '' #请修改此处
    }
    response = requests.request("GET", url_home, headers=headers)
    memo_count = json.loads(response.text)['stat']['memo_count']
    page = memo_count // 50
    resp = []
    for i in range(page+1):
        offset = 50 * i
        url = f'https://flomoapp.com/api/memo/?offset={offset}&tz=8:0'
        response = requests.request("GET", url, headers=headers)
        resp += json.loads(response.text)['memos']
    data = [[i['slug'], i['content'], i['tags'], i['created_at'], i['updated_at'],
             'https://flomoapp.com/mine/?memo_id='+i['slug']] for i in resp]
    data_df = pd.DataFrame(
        data, columns=['memo_id', 'content', 'tags', 'created_at', 'updated_at', 'memo_url'])
    return data_df


def savexls():
    flomo_data().to_excel('flomo.xlsx', sheet_name='sheet1', index=False)

def process2(): #第二次的逻辑
    writer = pd.ExcelWriter('flomo.xlsx',mode = 'a')
    flomo_data().to_excel(writer, sheet_name='sheet2',index=False)
    writer.save()


def processn(): #后续的逻辑
    wb = openpyxl.load_workbook('flomo.xlsx')
    wb.remove(wb['sheet1'])
    wb['sheet2'].title = 'sheet1'     
    wb.save('flomo.xlsx')
    print('delete sheet1→rename sheet2to1→fetch latest data')
    process2()

def deal_excel(sheet='sheet2'):
    lspath = r'/pages/'  #请修改此处
    data = pd.read_excel('flomo.xlsx', sheet_name=sheet)
    data_line = len(data)
    for i in range(data_line):
    # for i in range(3):
        content = data['content'][i]
        memo_id = data['memo_id'][i]
        memo_url = data['memo_url'][i]
        if re.match(r'<p>\w+</p>', content):
            title_loc = re.match(r'<p>\w+</p>', content).end()  # 取到title的最后一个字符
            body_loc = re.search(r'<p>\D+</p>', content).span()[-1]
            title = re.match(r'<p>\w+</p>', content).group().replace('<p>',
                                                                     '').replace('</p>', '')
            tags = data['tags'][i].replace("[", '').replace("]", '').replace(
                "'", '').replace(" ", '').split(',')
            del_tags = ['#'+i for i in tags  ] 
            body = content[title_loc:body_loc].replace('<p>', '').replace('</p>', '').replace('<b>', '**').replace(
                '</b>', '**').replace('<strong>', '**').replace('</strong>', '**').replace('#zk', '')
            for i in del_tags:
                body = body.replace(i,'')
            if 'zk' in tags and len(tags) == 1:  # 只有一个zk标签的情况
                with open(f'{lspath+title}.md', 'w') as file:
                    file.write('type:: #zk \n')
                    file.write('tags:: \n')
                    file.write(f'memo_id:: [{memo_id}]({memo_url}) \n')
                    file.write('- ' + body)
            if 'zk' in tags and len(tags) > 1:  # zk和其他的复合标签
                tags.remove('zk')
                new_tags = ['#'+i if '/' not in i  else '#'+i.split('/')[1] for i in tags  ]  # add the #(tag flag of logseq)
                new_tags = str(new_tags).replace(
                    "[", '').replace("]", '').replace("'", '')
                with open(f'{lspath+title}.md', 'w') as file:
                    file.write('type:: #zk \n')
                    file.write(f'tags:: {new_tags} \n')
                    file.write(f'memo_id:: [{memo_id}]({memo_url}) \n')
                    file.write('- ' + body)
            else:
                pass
        else:
            pass

def main():
    if not os.path.exists('flomo.xlsx'):
        savexls()  # the first run to create xlsx with sheet1
        deal_excel(sheet='sheet1')
    else:
        df = pd.read_excel('flomo.xlsx', sheet_name=None)
        if 'sheet2' not in list(df): #第二次逻辑
            process2()
            deal_excel(sheet='sheet2') 
        else: #已经生成过2次的情况
            processn()
            deal_excel(sheet='sheet2') 



if __name__ == '__main__':
    main()
