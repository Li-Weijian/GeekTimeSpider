# GeekTimeSpider
极客时间专栏文章爬虫, 转换保存为markdown文件。

### How Run
> python geekTimeSpider.py 专栏id 手机号码 登录密码 从第几篇开始下载
>
### 参数说明：  
   * 专栏id --> 必填， 从专栏网址可以查询，如： https://time.geekbang.org/column/intro/281， 281就是专栏id
   * 手机号码 --> 必填
   * 登录密码 --> 必填
   * 第几篇开始下载 --> 选填

### 注意事项
* 本程序使用了 ChromeDriver + selenium， 未安装情况下请搜索安装教程进行安装，
同时，需要将ChromeDriver 驱动包配置为环境变量
* 本程序供个人学习使用，不可传播和作为商业用途。下载的所有内容不允许用做商业用途

