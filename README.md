# 百度直播弹幕评论助手 - 支持人气协议、直播点赞、直播关注、直播分享

## API协议版本说说明：【请看完操作软件，不看操作的，出现问题，别找我解决！】

	百度风控系统：https://cloud.baidu.com/product/afd.html 

	是的你们没有看错，百度升级了自己的风控，并且已经在公测中...

	本文件夹软件版本为API协议版本，说明一下此次风控的说明事项；

	本次风控升级，经过两天两夜的风控测试对抗，最终发现了主要的问题所在；


## 1、第一个风控点：
 
  CK账号的问题=> CK账号之前检测时候，只要是可以登陆上的，基本上可以发送，
		
	但是目前有些账号如果没有进行手机绑定的情况下，发送弹幕在部分百度识别的黑名单（部分地区诈骗多）ip段中的可能无法发送，会被过滤；

	本人在自己本地电脑测试，只要CK可以登陆的，都可以发送内容，但是在客户的远程电脑中发送，却发送不了，使用手机绑定的账号发送，可以正常发送！

	还有就是CK账号本身就是万人骑的账号，有些人做了百度产品的营销推广或者是诈骗的话，CK也是不会正常发送的。


## 2、第二个风控点：
 
   长时间的大量发送重复弹幕数据，会导致当前的CK风控，服务器直接过滤弹幕信息，即使软件提示发送成功，但是不会返回到展示弹幕中！

## 3、第三个风控点：
 
  发送时间间隔问题，发送的时间过短，直接会监控当前ip下的弹幕信息，后续也第二个风控点一样，直接被过滤处理，但是不会封IP

## 4、第四个风控点：
 
  还是ip问题，你所在地区如果一些网络诈骗案件多的情况下，IP 会进入百度黑名单库，那么从这个IP上发送的内容，都不容易发出去！

	
## 解决方案：
 
		目前协议已经重写，与当前的版本匹配，本机测试发送了5个小时，没有任何的问题，

		先打开软件，使用软件中我提供的CK ，进行发送测试，如果发送成功的话，说明你的本地ip环境属于正常！

		弹幕ADS文档需要重新改写，一个文档中的内容，竟然不要少于100行，并且不要有重复的内容出现，

		在弹幕中，可以适当增加逗号，句号，问号，之类的，或者在最后加个字母啥的。规避检测

		时间间隔都调节到30秒之上；先单开测试，测试通过，在使用多开，多开的时候，CK最好不一样，

		如果出现发送弹幕 不想展示的现况，去买手机绑定的CK号即可，或者自己用自己的账号提取ck测试，尝试发送时候可以发送成功
	
		如果可以的话，说明是CK的问题，如果自己的账号也发送不了，说明您的本地IP被过滤处理，您就只能租服务器使用了！

=============================================================================================

【重要说明，不看浪费了！】

	这次写了两个版本，是的，你没有看错，是两个版本，这两个版本可是不一样的，别搞错了！

	一个版本是API协议版本，一个版本模拟执行版本（需要在本地下载Chrome浏览器，最新版本的，去官网下载）！

	尼玛，我两天两夜没日没夜的测试对抗风控，烟抽了快一条烟了。。。。，才获取到部分信息，在这里说明一下

	【之前所有的版本的文件，全部删除，备份好自己的CK、ADS、和setting.ini 文档】别怪我没提醒！
	

	第一就是CK的检测比之前严格，之前只要是可以登陆上去的就可以发送，但是这次不一定，如果购买的CK没有绑定手机号，或者长时间没有进行过登陆的

	就会在安全中心检测到账号异常，会导致弹幕无法发送，或者是CK原本操作过其他百度项目，被封禁过，导致账号异常的。也会出现这样的情况！

	第二就是IP 检测的问题，是的，IP的问题，是一个大难点，如果您的地区网络诈骗案件多的情况下，百度在风控数据库中会记录ip，如果在这个IP段中

	你发送数据的话，极大可能的，你的弹幕也会被过滤掉！


	以上的问题也有部分解决方案：

	第一个就是购买CK手机绑定的账号，这样极大可能性的可以正常发送内容！

	第二个就是租用动态ip的服务器进行推送。



	
