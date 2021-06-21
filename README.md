# DRFTutorial

为了搞明白django-restframework的用户验证我去学习了django的自定义验证那一块的文档，然后就对djang-restframework框架
的有关带认证的api稍微懂了些，然后为了继续深入DRF框架（django-restframework）我专门去了学习了超链接api和
restful api的设计模式。

DRF框架是标准的restful设计模式的一种体现，另外还实现了超链接api设计模式中的”可供性“。

DRF框架还实现了数据权限控制，例如只有数据的拥有者才能进行编辑和删除，只有认证的用户才能编辑数据。

DRF框架总的来说可以快速的构建标准的restful api服务，用户几乎不用写多少代码，比如说为了实现restful api通常就要
写get, put, patch, delete, post方法的实现，而且还有判断参数是否合法，这本身就是个体力活。现在，我学会了
DRF框架之后，我可以减少在做这些体力活的时间，而把更多的时间用于其它更有价值的事情上。

DRF框架是restful api应用的最佳实践。相比使用flask和django能大大的提高程序员的工作效率。flask用1天时间来
完成的事情，现在用DRF可能只需要几十分钟，如果熟练使用DRF的话。

这个部分主要是理解超链接API的用法和链接谁由谁来链接。