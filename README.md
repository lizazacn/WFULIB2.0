# 图书馆座位预约辅助
WFU图书馆座位预约辅助

# 简介：
    该脚本使用纯python编写，使用多线程技术，提高成功率（经过多次试验得到当前合适的线程数为5，建议不要修改线程数量）
    脚本具有启动通知和预约成功通知(邮件方式)，只需正确设置相关数据即可
# 使用条件
    1、Windows/Linux电脑（最优：24小时开机， 最低：预约时间段开机）
    2、安装Python运行环境及必要的库如：request、PIL
      ubuntu安装：
          sudo apt-get install python3 -y
          sudo pip3 install requests pillow
      Centos安装:
          sudo yum install python3 -y
          sudo pip3 install requests pillow
      Windows安装方法自行百度
     3、了解Google的的开发模式
# 启动方法
    python seat_order.py [用户名， 密码， 座位id， 邮箱， 截止时间]
    详情见示例：
        Linux:      Start.sh
        Windows:    Start.bat
# 获取座位id的方法
    使用谷歌浏览器打开预约界面-->找到想要预约的座位-->鼠标右击该座位-->选择检查
    例如：
     <div id=“517” ......>187</div>
     101A 187座位对应的座位id为517
# 设置定时任务
    Centos：
        sudo yum install crond
        vim /etc/crontab
        根据示例添加对应信息
        systemctl start crond  #启动crond
        systemctl enabel crond #设置crond开机自启动
    Windows百度有很多，请自行百度
    注意：定时启动建议使用绝对路径
<img src="https://github.com/lizazacn/WFULIB2.0/blob/main/20201204092306.PNG?raw=true">

# 联系方式
    email: lizaza@lizaza.cn

# 声明：
本脚本仅供学习交流使用，禁止商用，禁止用于任何非法用途。
若用于非法用途，作者不承担任何责任。
如有侵权请邮件联系，将会在两个工作日内删除
