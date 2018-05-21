# 对七牛cdn日志数据进行读取，清洗，分析，绘图和储存

要求的日志格式为七牛cdn日志格式
 ```
 110.110.110.110 HIT 10 [19/Apr/2016:00:00:00 +0800] "GET http://example.qiniu.info/in/2016/02/04/F01A9B39-45BF-AFF4-DB19-F85B9E4BD142.jpg?imageMogr2/format/png/thumbnail/480x%320E/quality/80! HTTP/1.1" 200 5136 "-" "Dalvik/1.6.0 (Linux; U; Android 4.4.4; 1105 Build/KTU84P)"
 ```

或满足下列标准格式

| ip| 命中 | 响应时间  | 请求时间|请求方法 | 请求URL|请求协议 |状态码 | 响应大小  |referer|UA|
| --: | -:| --: |---: | --:| --: |---: | ---:| :--: |---: | ---:|
| 14.163.128.14|HIT |1| 2017-07-12 22:38:18|GET |http://aaa.bbb.com/cc.jpg| -|200 |1024| www.baidu.com | "Mozilla/5.0 (Linux; Android ……|



| 函数名      |    API PATH | 数据类型  |
| --------: | --------:| :--: |
| get_data_by_factor      |    total_data | 根据限制条件返回清洗后的日志数据(不支持绘图)  |
| get_url_traffic  | url_traffic |  根据url返回对应的流量  |
| get_url_count     |   url_count |  根据url返回对应的访问次数  |
| get_ip_traffic      |    ip_traffic | 根据ip返回对应的流量  |
| get_ip_count      |   ip_count | 根据ip返回对应的访问次数  |
| get_code_count      |    code_count | 根据状态码返回对应的访问次数  |
| get_ip_url_code_count      |   ip_url_code_count | 根据ip、url返回不同状态码对应的访问次数  |
| get_url_code_count      |    url_code_count | 根据url和状态码返回对应的访问次数  |
| get_ip_code_count      |    ip_code_count | 根据ip和状态码返回对应的访问次数  |
| get_time_traffic      |    time_traffic | 返回指定时间段产生的流量  |
| get_time_count      |    time_count | 返回指定时间段对应的访问次数  |

### 1.配置日志路径和环境变量
```
# log_files指定日志的绝对路径
[log_files]
file_path:/Users/berniey/Documents/fun/Qiniu-cdnLog/log_path/aaa.bbb.com_2017-07-12-14_part-00000

# log_Path指定日志所在目录的绝对路径
[log_Path]
log_path:/Users/berniey/Documents/fun/Qiniu-cdnLog/log_path
```

>**注意：**数据库名称默认为cdnlog。

| name      |    Value | 含义  |
| :-------- | --------:| :--: |
| mysql_role  | work |  mysql数据库用户   |
| mysql_password     |   123 |  mysql数据库密码  |
| pg_role      |    work | pg数据库用户  |
| pg_password      |   123 | pg数据库密码  |

### 2.命令行调用
在data.py调用实例d的函数，通过命令`python3 data.py -s`获得指定的数据
数据格式如下

```
--日志行数--
205234

打印日志汇总信息
**************************************************

每个状态码所对应的访问次数

状态码      访问次数
200  :     195777
304  :       6177
206  :       3201
499  :         69
404  :          4

**************************************************

流量排名前5的url

流量(b)               url
757592832            : http://aaa.xxx.com/cc/aa/10000000/vn-p002/2_03.jpg
714420576            : http://aaa.xxx.com/cc/aa/10000000/vn-p002/2_01.jpg
688472529            : http://aaa.xxx.com/cc/aa/10000000/vn-watch/6.jpg
682368225            : http://aaa.xxx.com/cc/aa/10000000/vn-p002/2_06.jpg
675209964            : http://aaa.xxx.com/cc/aa/10000000/vn-watch/7.jpg

**************************************************

访问次数排名前5的url

访问次数                url
3768                 : http://aaa.xxx.com/cc/aa/10000000/vn-p002/2_02.jpg
3762                 : http://aaa.xxx.com/cc/aa/10000000/vn-p002/2_01.jpg
3738                 : http://aaa.xxx.com/cc/aa/10000000/vn-p002/e_01.jpg
3711                 : http://aaa.xxx.com/cc/aa/10000000/vn-p002/e_02.jpg
3690                 : http://aaa.xxx.com/cc/aa/10000000/vn-p002/2_03.jpg

**************************************************

流量排名前5的IP

流量                  IP
228015090            : 0.0.0.0
69567900             : 111.222.222.111
66124926             : 1.1.1.1
53028591             : 1.2.3.1
53028420             : 2.1.2.1

**************************************************

访问次数排名前5的IP

访问次数                IP
1350                 : 0.0.0.0
480                  : 1.2.1.2
345                  : 2.1.2.1
291                  : 3.2.1.3
288                  : 1.2.22.11
数据分析耗时
0.20561885833740234
总耗时
6.261575222015381
```
查询指定ip
```-i <ip> [limit]```

查询指定url
```-d <url> [limit]```



### 3.接口调用
`python3 api.py`
启动flask实例，用接口调用

请求格式：
```
http://127.0.0.1/api_path?<arg>=<value>&<arg>=<value>...
```



|参数名      |    值格式 | 备注  |
| --------: | --------:| :--: |
| limit      | x:y |正则表达式为r"^[0-9]*:[0-9]*"，如果不指定或不匹配，返回全部数据，***:100***返回top100数据，***1000:***返回1000之后数据，***10:20***返回11到20之间的数据  |
| code  | ddd或dxx |  返回指定状态码的数据，ddd<404>指定准确的状态码，dxx<4xx>指定某个类型的状态码  |
| ip     |   d.d.d.d |  正则表达式为r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"，目前仅支持ipv4  |
| url      |    http://aaa.bbb.com/ccc.jpg | 必须是完整的链接  |
| referer      |  无限制 | 必须准确完整  |
| start_time      |    2017-03-02 18:43:24 | 正则表达式r"^\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}$" 返回指定时间之**后**的数据  |
| end_time      |   2017-03-02 18:43:24 | 正则表达式r"^\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}$" 返回指定时间之**前**的数据  |
| save      |    mysql/pg/postgresql/csv/excel | 存储的类型，不指定则不存储  |
| pt      |    table_name/Users/user/Documents/d:\doc | 表名或路径，不指定表名默认为API_PATH+当前时间戳，路径为项目的目录  |
| is_show      |    任意字符 | 存在值则对返回的数据绘图  |
| kind      | 'line', 'hist', 'area', 'bar', 'barh', 'kde', 'area', 'pie' | 图像的形式  |
| use_index      |     boolean, default True | 使用index作为x轴  |
| dis_tick      |    x/y | 默认显示刻度值，指定x则不显示x轴刻度，指定y轴则不显示y轴刻度  |

### **示例**:

1. http://127.0.0.1:5000/get_total_data?limit=:100 

`查找前10000条数据里某一ip某一url的数据`

![Alt text](http://otp4la8ed.bkt.clouddn.com/22.png)
<br>
<br>
2. http://127.0.0.1:5000/get_url_traffic?limit=:100&is_show=t&kind=bar&dis_tick=x
<br>
`对前100条数据绘图，生成bar，隐藏x轴刻度`
<br>
![Alt text](http://otp4la8ed.bkt.clouddn.com/33.png)
<br>
<br>
3.http://127.0.0.1:5000/get_time_traffic?limit=:1000&start_time=2017-07-12%2022:00:00&end_time=2017-07-12%2022:16:47&is_show=t&kind=line
<br>
`前1000条数据中从2017-07-12 22:00:00到2017-07-12 22:16:47流量的线形图`
<br>
![Alt text](http://otp4la8ed.bkt.clouddn.com/55.png)
<br>
<br>
4.http://127.0.0.1:5000/get_code_count?is_show=t&kind=pie
<br>
`不同状态码数量的pie图`
<br>
![Alt text](http://otp4la8ed.bkt.clouddn.com/44.png)
<br>
<br>
5.http://127.0.0.1:5000/get_ip_url_code_count?limit=:1000&save=mysql&pt=ip_url_code_count
<br>
`将每个ip的每个url的状态码的统计数量中的前1000条保存在mysql，表名为ip_url_code_count`
<br>
![Alt text](http://otp4la8ed.bkt.clouddn.com/77.png)
<br>
<br>
6.http://127.0.0.1:5000/get_url_code_count?limit=:1000&save=csv&pt=/Users/l2017006/Documents/rm/test/get_url_code_count.csv
<br>
`将每个url的每个状态码的统计数量中的前1000条保存为csv文件，路径为/Users/l2017006/Documents/rm/test/get_url_code_count.csv`
<br>
![Alt text](http://otp4la8ed.bkt.clouddn.com/88.png)


