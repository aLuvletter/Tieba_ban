import json
import requests
import re
import os

def get_page():
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    html = response.text
    page_number = int(re.findall('page">共(.*?)页', html)[0]) + 1
    get_id(url)

def get_id(url):
    for i in range(1, 3):  # 查询页数根据需求自行调整
        url = url.replace('&pn=1', '&pn=') + str(i)
        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'
        html = response.text
        ban_info = re.findall('<img class="portrait".*?/item/(.*?)\' />                                    (.*?)</a>.*?管理员用户名</a></td><td>(.*?)</td></tr>', html)
        with open('user.txt') as f:
            user_data = f.readlines()
            user_text = str(user_data)
        f.close()
        if os.path.getsize('blacklist.json') == 0:
            for item in ban_info:
                if item[0] in user_text:
                    pass
                else:
                    ban_data[item[0]] = {'user_name': item[1], 'ban_time': item[2]}
            with open('blacklist.json', 'w') as f:
                f.write(json.dumps(ban_data, indent=4, ensure_ascii=False))
                f.close()
            f.close()
            ban_data.clear()
        else:
            with open('blacklist.json') as f:
                json_data = json.load(f)
                json_text = str(json_data)
            f.close()
            for k in list(json_data.keys()):
                if k in user_text:
                    del json_data[k]
            for item in ban_info:
                if item[0] in user_text or item[0] in json_text:
                    pass
                else:
                    ban_data[item[0]] = {'user_name': item[1], 'ban_time': item[2]}
            json_data.update(ban_data)
    with open('blacklist.json', 'w') as f:
        f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
    f.close()
    ban_id(ban_data)

def ban_id(ban_data):
    true_msg = 0
    error_msg = 0
    if os.path.getsize('user.txt') == 0:
        pass
    else:
        with open('user.txt') as f:
            for line in f.readlines():
                with open('blacklist.json') as f:
                    json_all = json.load(f)
                    if lines in str(ban_data) and line in str(json_all):
                        del ban_data[line]
                        del json_all[line]
        f.close()
    with open('blacklist.json') as f:
            json_data = json.load(f)
    f.close()
    for k, v in json_data.items():
        url = 'https://tieba.baidu.com/pmc/blockid'
        payload = {
            'day': 1,  # 封禁天数默认 1 天
            'fid': fid,  # 吧 id
            'tbs': tbs,  # 帖子 tbs
            'ie': 'gbk',  # 网页编码
            'portrait[]': k,  # 用户 id
            'reason': '发表政治贴、色情贴，此处不宜，给予封禁处罚。'
        }
        response = requests.post(url, headers=headers, data=payload).json()
        if response['errmsg'] == '成功':
            true_msg = true_msg + 1
            print(v['user_name'], '封禁成功')
        else:
            error_msg = error_msg + 1
            print(v['user_name'], response['errmsg'])

    print('本次共封禁：%s用户,封禁失败%s用户' % (true_msg, error_msg))

if __name__ == '__main__':
    if not os.path.isfile('tieba.config'):
        f = open('tieba.config', 'w', encoding='utf-8')
        f.write('fid=\ntbs=\nCookies=')
        f.close()
    elif not os.path.isfile('blacklist.json'):
        f = open('blacklist.json', 'w')
        f.close()
    elif not os.path.isfile('user.txt'):
        f = open('user.txt', 'w', encoding='utf-8')
        f.close()
    else:
        with open('tieba.config') as f:
            for line in f.readlines():
                lines = line.strip('\n')
                if line.split('=')[1] == '':
                    print('检查配置是否正确')
                else:
                    if 'fid' in line:
                        fid = lines.replace('fid=', '')
                    elif 'tbs' in line:
                        tbs = lines.replace('tbs=', '')
                    elif 'Cookies' in line:
                        Cookies = lines.replace('Cookies=', '')
    ban_data = {}
    url = '贴吧用户管理第一页地址'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Referer': '贴吧主页地址',
        'Cookie': Cookies
    }
    get_page()
