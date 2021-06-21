# 超链接RESTful设计模式

转自：
https://www.javacodegeeks.com/2020/08/introduction-to-hypermedia-rest-apis.html

## 1、域名

尽量把API部署在专用域名下:https://api.example.com

如果确定API很简单，不会有进一步扩展，可以考虑放在主域名下：https://example.org/api/

## 2、版本（Versioning）

将API的版本号放入URL中
```buildoutcfg
http://www.example.com/api/1.0/foo
http://www.example.com/api/1.1/foo
http://www.example.com/api/2.0/foo
```

另一种方法就是将版本号放在HTTP头信息中，放入URL方便和直观。github就采用的是这种方法。不同版本就是同一资源的不同表现形式，所以应该采用同一个URL。版本号可以在HTTP请求头信息的Accept字段中进行区分。
```buildoutcfg
Accept: vnd.example-com.foo+json; version=1.0
Accept: vnd.example-com.foo+json; version=1.1
Accept: vnd.example-com.foo+json; version=2.0
```

## 3、路径（Endpoint）

路径又称终点（endpoint），表示API的具体网址，每个网址代表一种资源。资源作为网址，只能是名词，不能是动词，而且名词与数据库表名对应，对于简洁的结构，始终用名词，此外利用HTTP方法可以分离网址中的资源名称的操作。API中的名词应该使用复数。无论子资源或者所有资源。就像下面例子，获取产品API可以这样定义。
```buildoutcfg
获取单个产品：http://127.0.0.1:8080/AppName/rest/products/1
获取所有产品: http://127.0.0.1:8080/AppName/rest/products
```

## 4、HTTP动词

对于资源的具体操作类型，由HTTP动词表示，常用的HTTP动词有四个（括号里是对应SQL命令）

```buildoutcfg
GET（SELECT）：从服务器取出资源（一项或多项）。
POST（CREATE）：在服务器新建一个资源。
PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
DELETE（DELETE）：从服务器删除资源。
```

还有三个不常用的HTTP动词：
```buildoutcfg
PATCH（UPDATE）：在服务器更新(更新)资源（客户端提供改变的属性）(更新局部的资源)。
HEAD：获取资源的元数据。
OPTIONS：获取信息，关于资源的哪些属性是客户端可以改变的。
```

```buildoutcfg
GET /zoos：列出所有动物园
POST /zoos：新建一个动物园（上传文件）
GET /zoos/ID：获取某个指定动物园的信息
PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
DELETE /zoos/ID：删除某个动物园
GET /zoos/ID/animals：列出某个指定动物园的所有动物
DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物
```

## 5、过滤信息（Filtering）
记录的东西多的话，API应该提供参数，过滤返回结果，服务器不可能全部返回。
```buildoutcfg
?limit=10：指定返回记录的数量
?offset=10：指定返回记录的开始位置。
?page=2&per_page=100：指定第几页，以及每页的记录数。
?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
?animal_type_id=1：指定筛选条件
```

参数设计允许冗余，即API路径和URL参数偶尔有重复，比如GET /zoos/ID/animals 与 GET /animals?zoo_id=ID 的含义是相同的。

## 6、状态码（Status Codes）
服务器向客户端返回的状态码和提示信息，常见的以下信息：（方括号是该状态码对应的HTTP动词）
```buildoutcfg
200 OK - [GET]：服务器成功返回用户请求的数据
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。登陆失败
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
302 FOUND [GET] 找到用户查询的数据
```

## 7、错误处理（Error handling）
如果状态码是4xx，服务器就应该向用户返回出错信息。一般来说，返回信息中将error作为键名，出错信息作为键值就可以了。
```buildoutcfg
{
    error: "Invalid API key"
}
```

## 8、返回结果
针对不同操作，服务器向用户返回的结果应该符合以下规范
```buildoutcfg
GET /collection：返回资源对象的列表（数组）
GET /collection/resource：返回单个资源对象
POST /collection：返回新生成的资源对象
PUT /collection/resource：返回完整的资源对象
PATCH /collection/resource：返回完整的资源对象
DELETE /collection/resource：返回一个空文档
```

## 9、超媒体

一个没有Hypermedia的简单示例：
```buildoutcfg
GET /orders/ 123
{
 
    "buyer_id" : 456 ,
    "order_date" : "2020-15-08T09:30:00" ,
    "total_price" : 4.99 ,
    "payment_date" : null ,
    "status" : "open" ,
    "items" : [
        {
            "product_id" : 789 ,
            "quantity" : 1 ,
            "price" : 4.99
        }
    ]
}
```
请注意，字段Buyer_id和product_id是对其他资源的引用。 如果客户想要获得有关买方的更多信息，则必须构造一个新的请求URI，如下所示：
```java
String buyerUrl = "/customer/" + order.getBuyerId();
```
在这里，客户端必须知道相关资源的确切URI格式。 这类似于不使用超链接浏览网络。 不必单击链接，我们必须为要访问的每个子页面手动更新浏览器请求行。

为了向订单表示中添加Hypermedia支持，我们必须将ID替换为相关资源的链接。
```buildoutcfg
{
    "buyer_url" : "/customers/456" ,
    "order_date" : "2020-15-08T09:30:00" ,
    "total_price" : 4.99 ,
    "payment_date" : null ,
    "status" : "open" ,
    "items" : [
        {
            "product_url" : "/products/789" ,
            "quantity" : 5 ,
            "price" : 4.99
        }
    ]
}
```
超媒体响应格式通常在单独的JSON对象中将链接分组在一起。 使用JSON对象表示链接也是一个好主意。 这使我们可以选择以后向链接添加更多信息。

如果将其应用于订单表示，则可能如下所示：
```buildoutcfg
{
    "order_date" : "2020-15-08T09:30:00" ,
    "total_price" : 4.99 ,
    "payment_date" : null ,
    "status" : "open" ,
    "items" : [
        {
            "quantity" : 5 ,
            "price" : 4.99 ,
            "links" : [
                { "rel" : "product" , "href" : "/products/789" }
            ]
        }
    ],
    "links" : [
        { "rel" : "buyer" , "href" : "/customers/456" }
    ]
}
```

## 10、状态转换(HATEOAS)

到目前为止，我们仅使用链接来指示与其他资源的关系。 链接也可以用于指示对资源的可能操作。 例如，可以付款和取消订单。 我们可以使用链接指向以下操作：
```buildoutcfg
{
    "order_date" : "2020-15-08T09:30:00" ,
    "total_price" : 4.99 ,
    "status" : "open" ,
    "payment_date" : null ,
    "items" : [ ... ],
    "links" : [
        { "rel" : "buyer" , "href" : "/customers/456" },
        { "rel" : "payment" , "href" : "/orders/123/payment" },
        { "rel" : "cancellation" , "href" : "/orders/123/cancellation" }
    ]
}
```
为了取消订单，我们现在可以简单地将PUT请求发送到取消链接。 取消订单后，资源表示可能如下所示：
```buildoutcfg
{
    "order_date" : "2020-15-08T09:30:00" ,
    "total_price" : 4.99 ,
    "status" : "cancelled" ,
    "payment_date" : null ,
    "items" : [ ... ],
    "links" : [
        { "rel" : "buyer" , "href" : "/customers/456" },
    ]
}
```
请注意，订单状态已更改，取消和付款链接已消失。 当然，已取消的订单无法再次取消，为已取消的订单付款是没有意义的。 因此，链接不仅指向操作，而且还告诉我们在当前资源状态下可以执行哪些操作。

## 11、API入口点

如果客户端不知道任何资源URI，则它们需要用于初始请求的某些入口点。 然后，此初始入口点提供了可访问资源的链接。 我们的示例API的API入口点可能如下所示：
```buildoutcfg
GET /

{
    "version" : "1.2.3" ,
    "description" : "Example API to manage orders" ,
    "links" : [
        { "rel" : "orders" , "href" : "/orders" },
        { "rel" : "customers" , "href" : "/customers" },
        { "rel" : "customer-by-id" , "href" : "/customer/{id}" },
        { "rel" : "customer-by-email" , "href" : "/customer{?email}" },
        ...
    ]
}
```
使用URI模板，我们可以确保客户端不需要浏览大型集合即可找到所需的资源。

## 12、为什么这样做有用，缺点是什么？

将Hypermedia引入REST API具有很多好处。 它减少了服务器和客户端之间的耦合。 服务器能够在不中断客户端的情况下重构和发展其URI结构。 客户端不再需要构造请求URI。

它还减少了客户端所需的逻辑。 让我们用可以取消或付款的订单来回顾前面的示例。 但是，这次没有链接：
```buildoutcfg
{
    "order_date" : "2020-15-08T09:30:00" ,
    "total_price" : 4.99 ,
    "status" : "open" ,
    "payment_date" : null , 
    "items" : [ ... ],
}
```
客户如何确定是否可以取消或支付此订单？ 也许只要订单处于打开状态就可以取消订单？ 只要订单处于未结状态且payment_date为null ，就可以付款。

该逻辑已经存在于服务器上，可以与HATEOAS进行通信。 因此，客户端不必检查逻辑，而只需要检查是否存在特定的链接。 例如：如果存在取消链接，则可以取消订单，因此应在用户界面中显示“取消订单”按钮。

相同的方法对于传达允许的操作非常有用。 服务器已经包含根据用户的权限/角色来决定允许其执行操作的逻辑。 因此，如果用户无权取消订单，请不要添加取消链接。

### 这些观点都很好，但是不利之处是什么？

在服务器端，为资源关系和状态转换添加链接可能是一项巨大的工作。 您必须构造链接，列出可能的状态转换，并检查客户端是否具有使用它们的权限。 仅当客户端实际使用API​​提供的超媒体元素并且不使用硬编码URI时，此工作才有用。

使用Hypermedia还可以大大增加响应大小。

超媒体REST API使用链接来指向相关资源以及可能的资源状态转换。 这使REST API成为可发现的，并减少了客户端与服务器之间的耦合。 客户端可以与服务器提供的链接进行交互，而不必自己构造URI。 它还减少了客户端的逻辑重复。

*但是，在服务器端实施Hypermedia可能是一项巨大的工作。*

有许多不同的超媒体响应格式可用，一种简单而流行的HAL格式。

## 13、RESTful API是无状态的，那么身份认证是不是RESTful

在REST应用程序中，每个请求必须包含服务器需要理解的所有信息，而不是依赖于服务器记住先前的请求。

在服务器上存储会话状态违反了REST体系结构的无状态约束。因此，会话状态必须完全由客户端处理。

### 会话状态

> 传统web应用程序使用远程会话。在这种方法中，应用状态完全保存在服务器上。
>
> 远程会话样式是客户机-服务器的一个变体，它试图最小化客户端组件的复杂性，或者最大限度地重用客户机组件，而不是服务器组件。每个客户端在服务器上启动一个会话，然后在服务器上调用一系列服务，最后退出会话。应用程序状态完全保留在服务器上。...
>
> 虽然这种方法带来了一些优点，但它降低了服务器的可伸缩性：
>
> 远程会话样式的优点是更容易集中维护服务器上的接口，在扩展功能时减少对已部署客户端中的不一致性的关注，如果在服务器上使用扩展的会话上下文，则提高效率。缺点是，由于存储的应用程序状态，它降低了服务器的可伸缩性，降低了交互的可见性，因为监视器必须知道服务器的完整状态。

### 无状态约束

> REST体系结构样式定义在一组约束的顶部，其中包括服务器的无国籍状态。根据菲尔丁的说法，其余的无状态约束定义如下：
>
> 客户端到服务器的每个请求都必须包含理解请求所需的所有信息，并且不能利用服务器上存储的任何上下文。因此，会话状态完全保留在客户端上。
>
> 这个约束导致了能见度，可靠性，和可伸缩性:
>
> 可见性得到了改善，因为监控系统不必只看单个请求数据，就可以确定请求的全部性质。可靠性的提高是因为它简化了从部分故障中恢复的任务。可伸缩性得到了改善，因为不需要在请求之间存储状态，可以让服务器组件快速释放资源，并进一步简化实现，因为服务器不必管理跨请求的资源使用情况。

### 认证和授权

> 如果客户端请求需要身份验证的受保护资源，则每个请求必须包含所有必要的数据必须经过适当的认证/授权。
>
> HTTP身份验证被认为是无状态的：验证请求所需的所有信息必须在请求中提供，而不是依赖于服务器记住先前的请求。

### 基于状态的Web服务

> 在基于状态的Web服务中，Client与Server交互的信息(如：用户登录状态)会保存在Server的Session中。再这样的前提下，Client中的用户请求只能被保存有此用户相关状态信息的服务器所接受和理解，这也就意味着在基于状态的Web系统中的Server无法对用户请求进行负载均衡等自由的调度(一个Client请求只能由一个指定的Server处理)。同时这也会导致另外一个容错性的问题，如果指定的Server在Client的用户发出请求的过程中宕机，那么此用户最近的所有交互操作将无法被转移至别的Server上，即此请求将无效化。

### 基于无状态的Web服务

> 在无状态的Web服务中，每一个Web请求都必须是独立的，请求之间是完全分离的。Server没有保存Client的状态信息，所以Client发送的请求必须包含有能够让服务器理解请求的全部信息，包括自己的状态信息。使得一个Client的Web请求能够被任何可用的Server应答，从而将Web系统扩展到大量的Client中。

### 总结两者的区别

> 因为无状态原则的特性，让RESTful在分布式系统中得到了广泛的应用，它改善了分布式系统的可见性、可靠性以及可伸缩性，同时有效的降低了Client与Server之间的交互延迟。无状态的请求有利于实现负载均衡，在分布式web系统下，有多个可的Server，每个Server都可以处理Client发送的请求。有状态的请求的状态信息只保存在第一次接收请求的Server上，所以后来同一个Client的请求都只能由这台Server来处理，Server无法自由调度请求。无状态请求则完全没有这个限制。其次，无状态请求有较强的容错性和可伸缩性。如果一台服务器宕机，无状态请求可以透明地交由另一台可用Server来处理，而有状态的请求则会因为存储请求状态信息的Server宕机而承担状态丢失的风险。Restful风格的无状态约束要求Server不保存请求状态，如果确实需要维持用户状态，也应由Client负责。
>
> 例如：
>
> 使用Cookies通过客户端保持登陆状态：
>
> 在REST中，每一个对象都是通过URL来表示，对象用户负责将状态信息打包进每一条信息内，保证对象的处理总是无状态的。在HTTP服务器中，服务器没有保存客户端的状态信息，客户端必须每次都带上自己的状态去请求服务器。客户端以URL形式提交的请求包含了cookies等带状态的数据，这些数据完全指定了所需的登录信息，而不需要其他请求的上下文或内存。
>
> 传递User credentials是Restful，而传递SessionID是Un-Restful的,因为session信息保存在服务器端。
>
> 无状态请求：Server不保存任何请求状态信息，Client的每一个请求都具有User credentials等所需要的全部信息，所以能被任意可用的Server应答。
>
> 有状态请求：Server保存了Client的请求状态，Server会通过Client传递的SessionID在Server中的Session作用域找到之前交互的信息，并以此来实现应答。所以Client只能由某一个Server来应答。

## 14、RESTful API的安全问题

传统的网站的话，那不用说，肯定是用户名+密码在登录页获得登录Token，并把登录Token记在Cookie和Session中作
为身份标识的这种方式，但现在不同了，关键是RESTful，这意味着我们设计出来的这些API是无状态的（Stateless）
，下一次的调用请求和这一次的调用请求应该是完全无关的，也就是说，正宗的RESTful Web API应该是每次调用都应
该包含了完整的信息，包括身份信息。