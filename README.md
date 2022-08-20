# 使用说明

### tieba.config
填入贴吧id、tbs以及cookie.

xx吧主页右键查看源代码即可获取

![1](https://github.com/aLuvletter/Tieba_ban/raw/main/images/20220820142411.png)

### user.txt

白名单用户id

![2](https://github.com/aLuvletter/Tieba_ban/raw/main/images/20220820144107.png)

### blacklist.json

初次使用默认为空

### main.py

需要修改的地方：吧务用户名、贴吧管理页面第一页地址、xx吧主页地址

进入到贴吧用户管理页面筛选吧务后

![3](https://github.com/aLuvletter/Tieba_ban/raw/main/images/20220820135019.png)

任意点击其一页码后复制，并把最后的数字改成1

![4](https://github.com/aLuvletter/Tieba_ban/raw/main/images/20220820144929.png)

### 定时执行

可通过宝塔任务进行定时循环封禁。

### 使用建议

建议使用单独一个吧务用户封禁广告用户，避免对普通违规用户循环封禁。
