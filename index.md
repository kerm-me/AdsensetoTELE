
# AdsensetoTELE

每天登陆Google Adsense查看收益有些麻烦，而平常用TG又比较多，所以尝试将每日收益推送到TG。可以使用免费VPS Linuxone进行托管（参考本文）。

# 使用教程 

参见本文



```shell
crontab -e
```

添加以下命令，转到项目目录，运行脚本（根据你自己的项目目录进行修改），也可以修改时间，由于不同的VPS时区不一致，所以得到的结果可能相差很多，不过只要在当天执行都OK吧。。。。

```
0 4 * * *   cd /home/linux1 && python3 generate_report.py
```

重启cron

```
service cron restart
```

**注意：不同用户的cronjob不同。在Linuxone下的，直接使用linux1用户无法运行cron restart命令（需要输入密码）。故推荐直接使用root用户编辑和运行。**

## 已知出现的错误

### 网页授权错误

错误 400： redirect_uri_mismatch

将应用类型选成了web。改成桌面应用。

### pip错误

ValueError: check_hostname requires server_hostname

开了代理，把代理关掉。

https://stackoverflow.com/questions/67297278/valueerror-check-hostname-requires-server-hostname

### SSL错误

ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:997)

网络不行，用国外的服务器就好了。

https://stackoverflow.com/questions/33410577/python-requests-exceptions-sslerror-eof-occurred-in-violation-of-protocol

### Windows Wget

wget 不保存文件

写全：

```powershell
wget -Uri "https://raw.githubusercontent.com/googleads/googleads-adsense-examples/master/v2/python/adsense_util.py" -OutFil "adsense_util.py"
```

https://blog.csdn.net/chongminglun/article/details/102306762

## python int 和 str

添加`str(intvalue)`

http://c.biancheng.net/view/4237.html

参考：

1. https://developers.google.com/identity/protocols/oauth2?hl=zh-TW
2. https://developers.google.com/adsense/management/reference/rest/v2/accounts.reports/generate
3. https://github.com/googleads/googleads-adsense-examples/tree/master/v2/python
4. https://blog.jialezi.net/?post=179
5. https://segmentfault.com/a/1190000016897341