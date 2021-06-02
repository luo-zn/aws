# [AWS Route 53](https://docs.aws.amazon.com/route53/index.html)

## [将域注册转移到Amazon Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-transfer-to-route-53.html#domain-transfer-to-route-53-requirements)

### 顶级域名的转移要求

大多数域名注册商有转移要求，主要是防止欺诈域名拥有者不断地转移域名。各个域名注册商要求各不相同，主要有以下几个：

* 在当前域名商注册时间至少超过60天，或者从其它域名注册商转到当前注册商的时间已经超过60天
* 如果域名注册过期，必须恢复，且域名转移时距离恢复的时间至少要超过60天
* 域名不能处于以下任何一种状态：
  * clientTransferProhibited
  * pendingDelete
  * pendingTransfer
  * redemptionPeriod
  * serverTransferProhibited
* 顶级域名的信息处于修改状态是不被允许转移的，如：域名拥有者处于修改当中

### 转移步骤

* 确认Amazon Route 53转移的顶级域名
  从[顶级域名列表](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/registrar-tld-list.html)中查看AWS能够支持转移到Route 53的顶级域名。  
* [可选的]转移DNS服务到Amazon Route 53或都其它的DNS服务提供商
  一些域名注册商会提供免费的DNS服务，当他们一收到Route 53的转移请求后便会停止这些服务。
* 在当前注册商修改设置，为每一个需要被转移的域名执行以下流程
  * 确认域名注册者的联系人的电子邮件是最新的  
    AWS会发一个授权转移邮件给注册者。邮件会有个链接需要注册者点击授权转移。如果不点击的话域名转移会被消息。
  * 解锁域名,这样它才能被转移  
    域名注册管理机构ICANN要求，开始转移它之前你需要解锁它
  * 确认域名状态，只有域名处于正常状态才能被转移  
    顶级域名转移的状态信息，查看[Transfer requirements for top-level domains](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-transfer-to-route-53.html#domain-transfer-to-route-53-requirements)
  * 关闭域名的DNSSEC  
    如果使用了DNSSEC的域名要转移到Route 53,在转移前要在前注册商里先关掉DNSSEC。当域名成功转移到Route 53后按要求设置DNSSEC。  
    操作步骤查看[Configuring DNSSEC signing in Amazon Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec.html)
  * 获取授权码  
    来自当前注册商的授权码用来授权AWS请求将域名注册转移到Route 53。在Route 53控制台操作的时候需要输入授权码。  
    有部分顶级域名转移时无需获取授权码： .co.za, .es, .jp, .uk, .co.uk, .me.uk, .org.uk  
    .uk, .co.uk, .me.uk, .org.uk 这些顶级域名转移到Route 53时不需要授权码，但需要改IPS tag的值
  * 将快要到期的域名续费
* 获取name servers的名称  
* 操作域名转移  
  转移的域名数量在5个以内的步骤：  
  * 打开Route 53控制台 <https://console.aws.amazon.com/route53/v2/home#GetStarted>
  * 在导航窗口，选择转移域
  * 输入需要转移的域名，点击检查
  * 如果检查结果是可转移，则添加到购物车。  
    如果检查结果是不可转移，Route 53会列出原因。联系当前域名的注册商，然后根据列出的原因解决转移的问题。
  * 重复3和4步，可以转移其它域名注册
  * 当所有想转移的域名都添加完成，点击继续
  * 对于每个转移的域名，输入如下合适的值：  
    * 授权码
    * Name server选项
      * 继续使用当前注册商或 DNS 服务提供的名称服务器  
        如果当前域名注册商提供DNS服务，建议转移域名前将DNS服务转移到另一个DNS服务提供商
      * 从与域同名的 Route 53 托管区域中导入名称服务器  
        选择此选项时，控制台会显示与域同名的托管区域列表。然后选择要用于为域路由流量的托管区域
      * 指定新的名称服务器来替换当前注册商的名称服务器(不推荐)  
        如果想使用其它DNS服务，需要在控制台显示的输入框里填入名称服务器
  * 域名的详细信息页里，填写注册人，管理员，技术联系人的联系信息
  * 对于某些顶级域名会要求填写额外的信息
  * 如果联系类型是个人，可以选择是否对WHOIS查询隐藏个人信息。更新信息查看<https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-privacy-protection.html>
  * 点击继续按钮
  * 选择是否自动续订域名注册
  * 检查输入的信息，阅读服务条款，然后选中复选框以确认您已阅读服务条款。
  * 点击完成购买  
    AWS会向该域名注册人发送电子邮件，请求授权转让该域名。
* 在收到的AWS邮件中点击确认和授权  
  在控制台完成操作后，AWS会发送一封或多封邮件到注册联系人。
