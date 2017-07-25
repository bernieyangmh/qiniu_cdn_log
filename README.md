# 对访问日志数据进行读取，清洗，分析，绘图和储存

要求的日志格式为七牛cdn日志格式
 ```
 110.110.110.110 HIT 10 [19/Apr/2016:00:00:00 +0800] "GET http://example.qiniu.info/in/2016/02/04/F01A9B39-45BF-AFF4-DB19-F85B9E4BD142.jpg?imageMogr2/format/png/thumbnail/480x%320E/quality/80! HTTP/1.1" 200 5136 "-" "Dalvik/1.6.0 (Linux; U; Android 4.4.4; 1105 Build/KTU84P)"
 ```

或满足下列标准格式

| ip| 命中 | 响应时间  | 请求时间|请求方法 | 请求URL|请求协议 |状态码 | 响应大小  |referer|UA|
| --: | -:| --: |---: | --:| --: |---: | ---:| :--: |---: | ---:|
| 14.163.128.14|HIT |1| 2017-07-12 22:38:18|GET |http://aaa.bbb.com/cc.jpg| -|200 |1024| www.baidu.com | "Mozilla/5.0 (Linux; Android ……|

