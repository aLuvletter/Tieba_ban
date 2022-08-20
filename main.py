import json
import requests
import re
import os

def get_page():
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    html = response.text
    page_number = int(re.findall('page">共(.*?)页', html)[0]) + 1  # 获取已封禁用户页数
    get_id()

def get_id():
    for i in range(1, 3):  # 循环获取已封禁用户列表
        url = 'https://tieba.baidu.com/bawu2/platform/listUserLog?stype=op_uname&svalue=%DA%A4%CB%BC%BE%B2%D7%F8&begin=&end=&op_type=&word=%BB%DD%B6%AB&pn=' + str(i)  # 贴吧用户管理页面
        response = requests.get(url, headers=headers)
        response.encoding = 'gbk'
        html = response.text
        ban_info = re.findall('<img class="portrait".*?/item/(.*?)\' />                                    (.*?)</a>.*?此处输入小吧管理百度用户名</a></td><td>(.*?)</td></tr>', html)  # 获取用户 id、用户名、封禁时间
        with open('user.txt') as f:
            user_data = f.readlines()  # 白名单用户
            user_text = str(user_data)
        f.close()
        if os.path.getsize('blacklist.json') == 0:  # 初次使用直接写入数据
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
                json_text = str(json_data)  # 黑名单数据
            f.close()
            for k in list(json_data.keys()):  # 删除在黑名单内的白名单用户
                if k in user_text:
                    del json_data[k]
            for item in ban_info:
                if item[0] in user_text or item[0] in json_text:  # 检查新数据否在黑名单或白名单内
                    pass
                else:
                    ban_data[item[0]] = {'user_name': item[1], 'ban_time': item[2]}
            json_data.update(ban_data)
    with open('blacklist.json', 'w') as f:  # 未在记录用户写入文件
        f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
    f.close()
    ban_id(ban_data)

def ban_id(ban_data):
    true_msg = 0
    error_msg = 0
    if os.path.getsize('user.txt') == 0:  #判断白名单是否为空
        pass
    else:
        with open('user.txt', encoding='utf-8') as f:
            for line in f.readlines():
                with open('blacklist.json') as f:
                    json_all = json.load(f)
                    if lines in str(ban_data) and line in str(json_all):
                        del ban_data[line]
                        del json_all[line]
        f.close()
    with open('blacklist.json') as f:  # 获取黑名单数据
            json_data = json.load(f)
    f.close()
    for k, v in json_data.items():  # 遍历 json
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
    if not os.path.isfile('tieba.config'):  # 判断配置文件是否存在
        f = open('tieba.config', 'w', encoding='utf-8')
        f.write('fid=\ntbs=\nCookies=')
        f.close()
    elif not os.path.isfile('blacklist.json'):  # 检查黑名单文件是否存在
        f = open('blacklist.json', 'w')
        f.close()
    elif not os.path.isfile('user.txt'):
        f = open('user.txt', 'w', encoding='utf-8')
        f.close()
    else:
        with open('tieba.config', encoding='utf-8') as f:
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
    url = 'https://tieba.baidu.com/bawu2/platform/listUserLog?word=%BB%DD%B6%AB'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Referer': 'https://tieba.baidu.com/bawu2/platform/listPostLog?stype=&svalue=&begin=&end=&op_type=&word=%BB%DD%B6%AB&pn=8',
        'Cookie': Cookies
    }
    get_page()
