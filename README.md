# ScrapyDemo
ScrapyDemo : Redis MySQLdb logging IngoreHttpRequestMiddleware UserAgentMiddleware HttpProxyMiddleware rules

项目原名叫:webspider,如果不能使用请下载项目后修改为webspider再运行.

该项目是2015年底完成的,当时创建了github代码仓库忘了上传了.现在上传上来.只提供代码供大家参考,不保证代码正常运行.

项目使用了以下库,不完整,后续的有些忘了添加进来了.

- Scrapy 			[ 如果提示没有lxml,就安装lxml,一般来说会自动安装lxml的 ]
- Redis			reids 的python操作库
- Sqlalchemy 		orm 数据操作
- Pymssql			mssql的python操作库
- Whoosh 			全文搜索
- Jieba 			结巴分词 全文搜索中用到
- Flask			python 的web框架,提供搜索接口的时候使用
- Qiniu			当初想用七牛云存储的保存下载的图片
- Requests		python 发送request的库

## 项目说明
项目附带代理采集,代理使用,爬虫,保存数据库,结巴分词,whoosh索引,flask开放web搜索接口,qiniu自动图片下载.

### 注:由于项目在实际交接的过程中采用了mssql,但是用Sqlalchemy过渡,所以如果想用mysql的话,只需要少量的代码改动即可实现,我还是主张代码仅供参考,毕竟时间太长了,我也不想修改了.

