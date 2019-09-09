# KUNPENG-AI-Competetion
华为2019年鲲鹏AI大赛32强源码分享
比赛链接：https://developer.huaweicloud.com/competition/competitions/1000005050/introduction
## 心得
本次比赛一开始是抱着玩一玩的心态做的，在央企工作比较闲，锻炼锻炼自己，以防脑子生锈。后来无意过了初赛，又经过几天集中改进策略修改bug之后过了复赛第一轮，而且在复赛第二轮前的小组热身赛中表现一直不错。这时我才发现原来我可以冲刺一下决赛，遗憾的是决赛换了地图，我的算法复杂度瞬间上升，在比赛服务器上超时了，0分惨败出局。让人不甘心的是看超时前的表现，进决赛应该是没问题的，而我只需要将一个搜索步长减一，就完全能满足每轮800ms延时的要求，由此带来的性能下降也就一丢丢。如果比赛方在复赛第二轮当天开方AI以提供测试环境就好了。怎么说呢，人生总是充满各种意外，因为意外（幸运）进了复赛，也因为意外憾别决赛，唯一能做好的，就是充实现在，放眼未来了。共勉。
## 主要思路
核心思想是两个词，一个是损益计算，另一个是WFS宽度优先搜索。
### 损益计算
对当前回合的每一个本方player，分别起算其可能动作的损益值gain，选取损益值最大的动作。损益值由一系列因素决定，包括但不限于与最近的enemy的距离，与最近的power的距离，与本方其它player的距离，与虫洞的距离，与最近的不在视野内的greatPower（定义分值大于3的power为greatPower）的距离等等，thief mode 与 police mode 考虑的因素有所不同。
### WFS
WFS的作用就是用来搜索上述最近距离，使用了队列模块Queue，相信了解WFS的人都不用多做解释了。

## 思考
### 1. WFS是否复杂度太高，不考虑用动态规划Dijkstra算法计算两点间最近路径吗？
哈哈一开始我是想到用Dijkstra的，但是由于对动态规划的敬畏导致我最后没去实现（手动捂脸），据说效率蛮高的，应该有大佬开源了相关代码。另一方面，利用Dijkstra计算需要对当前每一个我方player和每一个可见enemy以及power计算最短路径，感觉总体耗时也挺高的。当然，可以用一个dict存储已经计算过的最短路径，这样越到后面所需要的计算量越小，也可以一开始就把所有可能的两点间最短路径都算出来，存在表里，反正前几个回合一般也没什么危险，只是需要注意不要超过10回合，否则判为掉线，而一旦顺利计算完成，就一劳永逸了。而用WFS的话，所有上述所需计算的最短步数，都是可以在同一个WFS里一起搜索的（除了thief mode 下寻找最近的enemy，因为时空隧道的存在，两点间的最短路径是不对称的），整体效率其实也差不了多少。
### 2. constans.py里面定义了太多权重值以及搜索步数值，有什么依据吗？
没有哈哈，纯靠感觉！另一方面，如果计算资源够的话，可以暴力grid search一发，找到最佳组合啧啧。
### 3. 没考虑强化学习吗？
一开始我以为会有很多大佬用强化学习，结果据我所知没一个用的（手动狗头）。一来是状态太多不好建模，复杂度太高，而且激励函数不好定；另一方面是比赛方只提供了Windows版的服务端可执行程序，没有源码，没法去自己调整一些变量，输出一些必要信息以供训练。当然，肯定是我对强化学习不够了解，真正的大佬应该觉得这根本不是问题，毕竟围棋这么复杂的游戏都能用强化学习解决的很好，这肯定不在话下。

最后，代码中肯定还有bug，有心人如果发现还请告知，不胜感激~~~

备注：server/map_generator.py是群里大佬提供的。个人源码在Client_Python/client/ballclient/service下。PS：用GitHub还不多，有些地方没有完全交代清楚还请见谅~
