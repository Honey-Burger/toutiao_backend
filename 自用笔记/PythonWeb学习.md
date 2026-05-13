## 一、第一个FastAPI程序

### 1、创建Fastapi项目，安装依赖

新建项目（选 Pure Python）

​	File → New Project

​	左侧选 **Pure Python**

​	选好路径、起个名字，解释器选 Python3.8+

创建好项目之后，在终端运行：

```bash
pip install fastapi uvicorn
```

安装依赖

### 2、第一个接口`main.py`

```python
from fastapi import FastAPI,
import uvicorn  # 必须导入这个

app = FastAPI()

@app.get("/")
async def read_root():
    return {"msg": "Hello FastAPI888"}

# 👇 这段是让 PyCharm 能直接运行的关键
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
```

这里程序名默认为`main.app`，主机地址用的是`127.0.0.1`，默认端口为`port = 8000`,`reload=True`其中`reload`表示热重载，这里设为`Ture`表示允许服务器运行期间修改代码，每一次修改服务器都会自动重启再运行。

### 3、运行方式

#### （1）命令行

```bash
uvicorn main:app --reload
```

在终端中输入上述文字，敲击回车。其中--reload表示开启热重载。

在终端Ctrl+C即可停止运行

#### （2）PyCharm运行配置

在窗口工具栏寻找运行，点开编辑配置，点 `+` → 选 **Python**

Script: 选 `main.py`，interpreter: 选项目虚拟环境即可。

运行成功即有以下画面：![77729966513](C:\Users\BangeLu\AppData\Local\Temp\1777299665137.png)

且 http://127.0.0.1:8000可以成功进入。







## 二、FastAPI三大参数

同一段接口逻辑，根据参数不同返回不同的逻辑。FastAPI参数一般分为三类：

路径参数，查询参数，请求体

### 1、路径参数

​	位置：URL路径的一部分

​	作用：指向唯一的、特定的资源

​	方法：GET

示例代码：

```python
@app.get("/book/{id}")#路径参数
async def get_book(id: int = Path(...,gt=0, lt=101,description="书籍id，取值范围1-100之间")):
    #async表示异步进行
    return {"id": id, "title": f"这是第{id}本书"}
```

get方法的格式即为`"/地址/{参数}"`,这里`id: int`是对参数进行类型注解，约定其为 int 类型

#### Path(	)   注解

在路径参数添加注解中，有**Python原生注解**和**Path()注解**，这里了解Path()注解

FastAPI允许为参数声明额外的信息和校验。

在`getbook()`当中，我们可以看到

`Path(...,gt=0, lt=101,description="书籍id，取值范围1-100之间")`

这里是导入Path包，用 Path() 方法对参数注解进行额外的信息补充。

例如上述代码中,`...`表示这是必；`gt=0`表示此参数的最小值为0；`lt=101`表示小于101，即最大值为100；`description`则是对参数的描述。

填写完成后，可以进入FastAPI提供的测试网页进行测试，[FastAPI - Swagger UI](http://127.0.0.1:8000/docs#/)

![77730098266](C:\Users\BangeLu\AppData\Local\Temp\1777300982661.png)

**Path () 常用参数表**

| 参数名        | 作用                               | 示例                                 |
| ------------- | ---------------------------------- | ------------------------------------ |
| `default`     | **默认值**，路径参数必须设为 `...` | `default=...`                        |
| `title`       | 参数标题（文档显示）               | `title="用户ID"`                     |
| `description` | 参数描述（接口文档）               | `description="需要查询的用户唯一ID"` |
| `gt`          | 大于 (greater than)                | `gt=0` (必须大于 0)                  |
| `ge`          | 大于等于 (greater equal)           | `ge=1`                               |
| `lt`          | 小于 (less than)                   | `lt=101` (最大值 100)                |
| `le`          | 小于等于 (less equal)              | `le=100`                             |
| `min_length`  | 字符串**最小长度**                 | `min_length=2`                       |
| `max_length`  | 字符串**最大长度**                 | `max_length=50`                      |
| `regex`       | 正则匹配校验                       | `regex="^[0-9]+$"`                   |
| `deprecated`  | 标记参数弃用                       | `deprecated=True`                    |

### 2、查询参数

声明的参数不是路径参数时，路径操作函数会把该参数**自动解释为****查询参数**

​	位置：URL里`？`之后![77730190864](C:\Users\BangeLu\AppData\Local\Temp\1777301908642.png)

​	作用：对资源集合进行过滤、排序、分页等操作

​	方法：GET



设立一个需求：查询新闻的时候我们要进行分页查询，这个时候我们要知道跳过的记录数和返回的记录数。

示例代码：

```python
@app.get("/news/news_list")#不需要参数{xxx}
async def get_news_list(
        skip: int, limit: int = 10
        #limit: int = 10 这种方式是用Python原生类型注解方式给了默认值10
):
    return {"skip": skip, "limit" :limit}
```

容易发现的是，这里URL中并没有出现参数，只是一段URL

这里 def 方法里使用的是原生注解，`limit`设置默认值为10

#### Query(	)注解

当然，和路径参数一样，查询参数也有自己的额外注解方法`Query()`

使用方法也和`Path()`类似，直接上使用后的代码：

```python
@app.get("/news/news_list")#不需要参数{xxx}
async def get_news_list(
        skip: int = Query(0, description="跳过的记录量", lt = 100),
        limit: int = Query(10, description="返回的记录数")
        #这里用Query()方法来为参数进行类型注解，以及默认值的设定，还有描述，限制范围
        #和路径参数相似
        #limit: int = 10 这种方式是用Python原生类型注解方式给了默认值10
):
    return {"skip": skip, "limit" :limit}

```

这里Query()方法的第一个参数可以**设置默认值**，这样就可以代替Python原生注解，并且可以添加更多的条件限制和信息补充。

**Query()`常用方法**：

| 参数          | 说明                   | 常用示例                   |
| ------------- | ---------------------- | -------------------------- |
| `default`     | 路径参数**必须写 ...** | `default=...`              |
| `title`       | 文档标题               | `title="用户ID"`           |
| `description` | 参数说明               | `description="用户唯一ID"` |
| `gt`          | 大于                   | `gt=0`                     |
| `ge`          | 大于等于               | `ge=1`                     |
| `lt`          | 小于                   | `lt=1000`                  |
| `le`          | 小于等于               | `le=999`                   |
| `min_length`  | 字符串最小长度         | `min_length=1`             |
| `max_length`  | 字符串最大长度         | `max_length=20`            |
| `regex`       | 正则匹配               | `regex=r"^\d+$"`           |
| `deprecated`  | 标记废弃               | `deprecated=True`          |

运行上述代码后，我们去docs界面看一下：![77730324368](C:\Users\BangeLu\AppData\Local\Temp\1777303243687.png)

发现两个查询参数都有默认值，而且上方都有对应的描述。

### 3、请求体参数

在HTTP协议中，一个完整的请求由三部分组成：

​	①请求行：包含方法、URL、协议版本

​	②请求头：元数据信息

​	③**请求体：实际要发送的数据内容**

请求体参数的几个属性：

​	位置：HTTP请求的消息体(body)中

​	作用：创建、更新资源，携带大连数据，如：JSON

​	方法：POST、PUT等

假设一个需求：我们要注册一个用户，主要信息包含用户名和密码，示例代码：

```python
from pydantic import BaseModel#要先导入BaseModelm模块
'''
主体代码省略
'''
class User(BaseModel):#编写User类，继承自BaseModel，固定写法
    username: str
    password: str
	#设置两个属性，对其进行类型注解，都为str
#注册：用户名和密码 → str
@app.post("/register")#路径名设为register
async def register(user: User):#user注解为User类型
    return user
```

运行之后，进入docs界面：![77734511378](C:\Users\BangeLu\AppData\Local\Temp\1777345113781.png)

且可以修改：![77734518431](C:\Users\BangeLu\AppData\Local\Temp\1777345184319.png)

注意这里，请求体参数不在URL里面了，而是在请求体（body）里面，在大括号里面：![77734534627](C:\Users\BangeLu\AppData\Local\Temp\1777345346274.png)

**练习**：需求：设计接口新增图书，图书信息包含：书名、作者、出版社、售价

```Python
class Book(BaseModel):
    bookname: str
    author: str
    press: str
    price: float

@app.post("/register")
async def register(book: Book):
    return book
```



#### Field(	)注解

当然，请求体参数也有自己的额外注解方法`Field()`，使用方法和前两种类似，

使用时要**从 pydantic 导入 Field** :`from pydantic import Field`

直接上代码：

```python
class User(BaseModel):
    username: str = Field(default="张三",min_length=2,max_length=10,description="用户名,长度要求2-10个字")
    password: str = Field(min_length= 3,max_length=20)
```

这里不过多赘述，参数和前面的方法有很多可以互相参考的地方。

**Field（）`常用方法**：

| 参数              | 说明                     | 常用场景                 |
| ----------------- | ------------------------ | ------------------------ |
| `default`         | 字段默认值               | 可选字段设置默认值       |
| `default_factory` | 动态默认值（可调用对象） | 时间、随机数等动态默认值 |
| `gt` / `lt`       | 大于 / 小于              | 数字范围校验             |
| `ge` / `le`       | 大于等于 / 小于等于      | 分数、年龄等区间限制     |
| `min_length`      | 字符串最小长度           | 用户名、密码长度限制     |
| `max_length`      | 字符串最大长度           | 昵称、标题长度控制       |
| `pattern`         | 正则匹配校验             | 手机号、邮箱、验证码格式 |
| `alias`           | 字段别名                 | 接收前端小驼峰命名参数   |
| `title`           | 字段标题                 | 接口文档展示             |
| `description`     | 字段描述                 | 接口文档说明             |
| `examples`        | 示例值                   | 自动生成接口文档示例     |
| `exclude`         | 序列化时忽略该字段       | 密码等敏感信息不返回     |
| `repr`            | 是否在打印时显示         | 隐藏敏感字段             |
| `required`        | 是否为必填字段           | 标记必须传入的参数       |

**练习**：设计接口新增图书，图书信息包含：书名、作者、出版社、售价。具体要求如下：

- 书名不能为空

- 作者长度2-10

	 出版社：默认值为“黑马出版社”	

- 售价不能为空，价格要大于0元

  ```python
  class Book(BaseModel):
      bookname: str = Field(...,min_length=2,max_length=20,description="用户名,长度要求2-20个字")
      author: str = Field(min_length= 2,max_length=10)
      press: str = Field(default = "黑马出版社")
      price: float = Field(...,gt = 0)
  ```







## 三、FastAPI响应类型

### 1、响应类型设置方式

响应类型设置方式分为 装饰器中指定响应类 和 返回响应对象 两种

#### （1）装饰器中指定响应类

​	使用场景为固定返回类型（HTML，纯文本等）

​	

```Python
@app.get("/html", response_class=HTMLResponse)#这里固定了响应类型为HTMLResponse
async def get_html():
    return ""<h1>这是标题<h1>
```

#### （2）返回响应对象

​	使用场景为文件下载、图片、流式响应等

```Python
@app.get("/file")#这里没有固定了响应类型
async def get_file():
    file_path = "./files/1.jpeg"
    return FileResponse(file_path)
```

| 响应类名称            | 导入路径                                          | 核心用途          | 适用场景                   | 极简代码示例                                |
| --------------------- | ------------------------------------------------- | ----------------- | -------------------------- | ------------------------------------------- |
| **JSONResponse**      | `from fastapi.responses import JSONResponse`      | 默认 JSON 响应    | 接口返回数据、API 标准响应 | `return JSONResponse({"msg": "ok"})`        |
| **HTMLResponse**      | `from fastapi.responses import HTMLResponse`      | 返回 HTML 页面    | 简单网页、富文本展示       | `return HTMLResponse("<h1>Hello</h1>")`     |
| **PlainTextResponse** | `from fastapi.responses import PlainTextResponse` | 返回纯文本        | 文本信息、日志输出         | `return PlainTextResponse("Hello FastAPI")` |
| **FileResponse**      | `from fastapi.responses import FileResponse`      | 返回文件下载      | 图片、文档、压缩包下载     | `return FileResponse("test.pdf")`           |
| **StreamingResponse** | `from fastapi.responses import StreamingResponse` | 流式响应          | 大文件传输、实时数据流     | `return StreamingResponse(generator())`     |
| **RedirectResponse**  | `from fastapi.responses import RedirectResponse`  | 页面 / 接口重定向 | 跳转链接、路由转发         | `return RedirectResponse("/login")`         |
| **ORJSONResponse**    | `from fastapi.responses import ORJSONResponse`    | 高性能 JSON       | 大数据量、高性能要求       | `return ORJSONResponse({"data": [...]})`    |
| **Response**          | `from fastapi import Response`                    | 基础响应类        | 自定义状态码、响应头       | `return Response(status_code=201)`          |

### 2、JSON格式

默认情况下，FastAPI会自动将路径操作函数返回的Python对象（字典、列表，Pydantic模型等），经由jsonable_encoder转换为JSON兼容模式，并包装为JSONResponse返回。这省去了手动序列化的步骤，可以专注于业务逻辑。



![77737469332](C:\Users\BangeLu\AppData\Local\Temp\1777374693327.png)

可以很明显的看到，响应头里的响应文件格式JSON。

### 3、HTML格式

设置响应类为`HTMLResponse`，当前接口即可返回HTML内容，

记得导入`from fastapi.responses import HTMLResponse`。

```python
@app.get("/html",response_class=HTMLResponse)#设置响应格式
async def get_html():
    return "<h1>这是一级标题<h1>"
```

运行后，输入URL[`127.0.0.1:8000/html](http://127.0.0.1:8000/html)`，可以看到![77737696089](C:\Users\BangeLu\AppData\Local\Temp\1777376960897.png)





### 4、响应文件格式

**FileResponse** 是 FastAPI 提供的专门用于高效返回文件内容（如图片、PDF，音视频等）的响应

类。它能够只能处理文件路径、媒体类型推断、范围请求和缓存头部、是服务静态文件的推荐方

式。

假设我们需要一个接口，用来返回一张图片的内容。

首先，导入`from fastapi.responses import FileResponse`

然后：

```python
@app.get("/file")
async def get_file():
    path = "./Picture/emotion.png"#图片的相对路径
    return FileResponse(path)#返回响应对象
```

这里`path = "./Picture/emotion.png"`需要在当前文件夹下存在图片：![77737849007](C:\Users\BangeLu\AppData\Local\Temp\1777378490075.png)





### 5、自定义响应数据格式

response_model 是路径操作装饰器 （如@app.get 或 @app.post）的关键参数，**它通过一个Pydantic模型来严格定义和约束API短点的输出格式**。



假设需求：需要一个新闻接口，响应数据格式为 id、title、content

先导入`from pydantic import BaseModel`

```python
class News(BaseModel):
    id:int
    title:str
    content:str

@app.get(f"/news/{id}", response_model= News)#这里response_model设置为News，且只能为News
async def get_news(id:int):#外面传到后端的参数，需要注解
    return {
        "id":id,
        "title":f"这是第{id}本书",
        "content":"这是一本好书"
    }
#News设置了三个属性，则函数返回值也需要返回三个完整属性，否则会报错。
```

**注意**：只要是从**外面传给后端**的 → 必须注解

`					    id: int` 要注解

`             user: User` 也要注解

因为它们都是【进】的数据！

只有 return 出去的东西【不用注解】！





### 6、异常响应处理

对于客户端引发的错误（4xx，比如资源未找到、认证失败），应使用 `fastapi.HTTPException` 来中断正常处理流程，并**返回标准错误响应**。

使用之前，先导入包`from fastapi import HTTPException`

假设需求：在用户查找不存在的新闻id时，应抛出错误并有合理解释

```python
@app.get("/news/{id}")
async def get_news(id: int):
    id_list = [1, 2, 3, 4, 5]#假设有5条新闻
    if id not in id_list:
        raise HTTPException(status_code=404, detail="您查找的新闻不存在")
        #如果查找的新闻页不在列表范围内，就会抛出错误，并给出文字说明
    return {"id": id, "title": "新闻标题"}
```

这里 HTTPException里使用的位置参数主要为status_code，设置为404，detial位置参数则是用来抛出错误后显示具体的错误信息。

运行后，进入docs界面查看：![77743793904](PythonWeb学习.assets/1777437939049.png)

这里直接输入的错误的信息，可以看到直接报错404not Found,而且响应体里也 给出了相应的文字解释。







## 四、FastAPI进阶

### 1、中间件

中间件（Middleware）是一个在每次**请求进入 FastAPI 应用时都会被执行的函数**。它在请求到达实际的路径操作（路由处理函数）之前运行，并且在响应返回给客户端之间再运行一次。

中间件定义：函数的顶部使用装饰器`@app.middleware("http")`

示例代码：

```Python
@app.middleware("http")
async def middleware(request, call_next):#两个位置参数
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response
```

这里`middleware()`有两个位置参数，`request`是进来的请求，`call_next`则是把请求交给下一个中间件处理的方法。

将请求传给`call_next`，最终返回的响应赋给response变量，然后再返回。

为什么`call_next`前面会有await？因为`call_next`是一个异步函数，但在这里我们要等路由函数执行完成，再将响应传给`response`，否则`call_next`传入的是一个协程对象，导致无法运行。

在网页发送请求后，出现：![77746057013](PythonWeb学习.assets/1777460570132.png)

**注意**：当有多个中间件时，中间件的执行顺序是**自下而上**的，例如：

```Python
@app.middleware("http")
async def middleware(request, call_next):
    print("中间件1 start")
    response = await call_next(request)
    print("中间件1 end")
    return response

@app.middleware("http")
async def middleware(request, call_next):
    print("中间件2 start")
    response = await call_next(request)
    print("中间件2 end")
    return response
```

发送请求时，终端显示：

![77746080457](PythonWeb学习.assets/1777460804577.png)

就类似洋葱模型，从中间传过去，最先穿过的层的最后出来。



### 2、依赖注入

使用依赖注入系统来共享通用逻辑，避免代码重复。

- 依赖项：可重用的组件（函数/类）。负责提供某种功能或数据。
- 注入：FastAPI自动帮你调用依赖项，并将结果”注入“到路径操作函数中。

优点：

- 代码复用：一次编写，多处使用
- 解耦：业务逻辑与基础设施代码分离
- 易于测试：轻松地用模拟依赖替换真实依赖进行测试

依赖注入应用场景很广泛，处理请求参数 ，共享业务逻辑，共享数据库连接和安全认证等都用得到依赖注入。

依赖注入三步骤：

1. 创建依赖项：

   将依赖项的内部逻辑封装起来，创建依赖项；

2. 导入Depends：

   导入Depends包`from fastapi import Depends`；

3. 声明依赖项：

   在路由操作函数里，用`Depends(依赖项方法名)`方法注入。

假如现在我们有新闻和用户两个接口，但是都需要相同的查询的方法：

```python
async def comment_parameters(#创建依赖项
        skip:int = Query(0, ge=0),#因为这里是功能查询，所以使用Query方法来注解参数
        limit:int = Query(10, le=60)
):
    return {"skip": skip, "limit": limit}#返回参数

@app.get("/news/news_list")
async def get_news_list(common = Depends(comment_parameters)):
    #在路由执行函数里利用Depends方法注入，Depends方法的参数就是依赖项
    #Depends方法根据参数寻找依赖项，将依赖项的返回值再赋值给参数common，最后路由处理函数返回common
    return common

@app.get("/users/users_list")
async def get_news_list(common = Depends(comment_parameters)):
    return common
#刷新页面，进入docs文档进行测试，可以发现两个路由处理函数的响应体中都有依赖项中的参数。如果其中一个没有注入依赖项，则不会有
```



### 3、ORM简介及安装

ORM （对象关系映射）是一种编程技术，用于在**面向对象编程语言和关系型数据库之间建立映射**。它允许开发者通过操作对象的方式与数据库进行交互，而无序直接编写复杂的SQL语句。

优点：

- 减少重复的SQL代码
- 代码更简洁，可读性变高
- 自动处理数据库连接和实事务
- 自动防止SQL注入攻击

ORM工具有很多，这里以 SQLalchemy ORM 为例进行学习

**安装**：在Pycharm终端输入`pip install "sqlalchemy[asyncio]" aiomysql`



### 4、ORM建表

在实行ORM之前，要保证已经提前安装好MySQL，并创建了`FastAPI_first`数据库

#### （1）创建异步引擎

提前导入这些包：

```python
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.sql.sqltypes import String, Float, DateTime
```

```python

ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8"
#这是数据库连接字符串，告诉程序连哪个数据库
#mysql+aiomysql：用 MySQL 数据库 + 异步驱动 aiomysql
#root：数据库用户名
#123456：数据库密码
#localhost：数据库在本机
#3306：MySQL 默认端口
#FastAPI_first：要连接的数据库名
#charset=utf8：字符编码，支持中文
async_engine = create_async_engine(#异步引擎的配置
    ASYNC_DATABASE_URL,#数据库连接地址()
    echo=True,#可选，输出 SQL 日志
    pool_size=10,#设置连接池活跃的连接数
    max_overflow=20)#允许额外的连接数，也就是说对多能连接30个
```

#### （2）定义模型类

这里我们要定义基类和表对应的模型类。我们这里准备创建一个书籍表：

书籍ID、书名、作者、价格、出版社。

**基类**：

```python
class Base(DeclarativeBase):
    create_time : Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment = "创建时间")
    update_time : Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now(),comment="修改时间")
```

这里

`Mapped[类型]` 作用：声明这个字段在数据库里是什么类型

`mapped_column(...)` 作用：给字段配置详细规则：是不是主键、默认值、更新时间、注释等

`class Base(DeclarativeBase)`是所有数据库表的**公共父类**所有表继承它，自动拥有时间字段。

`insert_default=func.now()`只在**第一次插入**时生效，更新数据不会改变

`default=func.now`插入数据时，如果没给值，**自动填当前时间**，重点：**不加括号！**

调用方法带括号和不带括号的区别，以`func.now()`为例：

不带括号：`func.now`

传的是函数本身，执行插入时才生成时间，永远是当前时间。

带括号：`func.now()`

传的是函数执行结果，代码运行时就固定成一个时间值。

**模型类**：

```python
class Book(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍ID")
    bookname: Mapped[ str] = mapped_column(String(255), comment="书名")
    author: Mapped[ str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[ str] = mapped_column(String(255), comment="出版社")
```

`__tablename__ = "book"`指定该类对应的 **数据库表名**，生成的表就叫book

后面的几行都是给每个字段的配置设置详细规则，就不需要写SQL语句来设置了。



#### （3）定义函数建表

FastAPI启动的时候调用建表的函数

```python
async def create_tables():
    #获取异步引擎，创建事务 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)#Base 模型类的元数据创建表
```

`async with async_engine.begin() as conn`是将`async_engine.begin()`打开，并将其起个名字（as）为 `conn`

**with 的作用**

- **自动打开资源**（文件 / 数据库连接）
- **自动关闭资源**（不用手动关）
- 安全、不报错、不占内存
- ​

解释：`await conn.run_sync(Base.metadata.create_all)`

**await**：

- 因为是**异步操作**，必须等它干完才能继续。
- 作用：**等待建表完成**。

 **run_sync(...)**

- **运行同步方法**
- 因为建表是老方法，必须套这个才能在异步里用。

**Base.metadata**

- **所有表的结构、图纸**
- 包含写的 `Book` 表、字段、类型。

**create_all()**

- **创建所有表**
- 根据图纸，在 MySQL 里生成真实的表。

启动服务器,可得:

```bash
INFO:     Will watch for changes in these directories: ['E:\\Graduate\\FirstFastAPI']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [6324] using StatReload
INFO:     Started server process [143232]
INFO:     Waiting for application startup.
2026-04-30 16:20:03,468 INFO sqlalchemy.engine.Engine SELECT DATABASE()
2026-04-30 16:20:03,468 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-30 16:20:03,471 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
2026-04-30 16:20:03,471 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-30 16:20:03,472 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
2026-04-30 16:20:03,472 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-30 16:20:03,472 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-04-30 16:20:03,473 INFO sqlalchemy.engine.Engine DESCRIBE `fastapi_first`.`book`
2026-04-30 16:20:03,473 INFO sqlalchemy.engine.Engine [raw sql] ()
2026-04-30 16:20:03,476 INFO sqlalchemy.engine.Engine COMMIT
INFO:     Application startup complete.
```



### 5、在路由中使用ORM

核心：创建**依赖项**，使用**Depends**注入到处理函数

需求：查询功能的接口，查询图书 → 依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数

#### （1）创建异步会话工厂

```python
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, #指定异步会话类
    expire_on_commit= False#提交后会话不会过期，不会重新查询数据库
)#创建异步会话工厂
```

**Q:为啥要创建异步会话工厂？有啥用？**

**A:**它就是一个 “批量生产数据库会话” 的工具，统一管理所有数据库连接，不让你每次都重复写一堆代码。可以把引擎理解为总水管，会话工厂比喻为**水龙头制造机**，而每段会话都是一个个水龙头。统一配置这样后面的每次对话就可以直接用工厂生产的水龙头而不需要自己造。会话工厂也可以保证，每个请求对话都是**相互独立**的，不会互相干扰。

​	

三个参数

`bind=async_engine`： 绑定到之前的数据库引擎（连接池）

`class_=AsyncSession`：指定这是异步会话，不是同步的

`expire_on_commit=False`：提交事务后，查询结果不会失效，否则接口返回时会报错 “对象已过期”



#### （2）依赖项函数

```python
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session #返回数据库会话给路由处理函数
            await session.commit()#提交事务
        except Exception:
            await session.rollback()# 如果有异常，回滚
            raise
        finally:
            await session.close()#关闭会话
```

`get_database ()`给 FastAPI 路由**自动提供数据库会话**，并且自动管理。

流程可大致写为：创建 → 使用 → 提交 / 回滚 → 关闭

`async with AsyncSessionLocal() as session`：使用`with...as...`来自动创建会话，自动关闭会话

`yield session`：这里是FastAPI依赖注入的关键，把session交给调用依赖项的函数，也就是路由函数使用，等调用结束后，再执行依赖项函数后面的代码。

`await session.commit()`：当`yield session`执行完毕后，对数据库的增删改操作已经暂时被写入了内存里，但实际上**还没有真正执行**，这时必须实行commit，才能真正的将操作写入数据库中，也就是增删改真正的生效。

`except Exception: rollback()`：如果出现错误了 ，就**撤销所有操作**，保证原有数据不乱。

`finally: close()`：无论成功失败，**最后一定关闭会话**防止数据库连接泄漏，兜底操作。

**Q**：这个代码里，with...as...不是可以**自动开启关闭服务**吗？为什么finally还需要close()呢？

**A**：with确实会在退出时自动调用`await session.close()`，但为了防止代码半路崩溃，with可能来不及关闭，而 close() 就是保险，因为不论如何 close() 都会执行。可以比喻为：**async with = 自动关门，finally: close() = 再手动拉一下门，确认关紧了**



#### （3）将依赖注入路由中使用

```python
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)#依赖注入):
    result = await db.execute(select(Book))#查 book 表里所有数据
    book_list = result.scalars().all()
    return book_list
```

`db: AsyncSession`：对变量 db 做注解，为AsyncSession类型。AsyncSession 是异步数据库会话类型，可以生成一个能操作 MySQL 数据库的工具对象，这里 db 就是。

`db: AsyncSession = Depends(get_database)`：通过Depends调用依赖函数，拿到一个数据库会话，放进db里使用。

`result = await db.execute(select(Book))`：

​	`execute()` = **执行 SQL 操作**

​	`select(Book)` = ORM 查询 → 等价于 `SELECT * FROM book`

​	`await` = 异步必须加（必须要等操作执行完毕，才能进行下一步）

​	`result` = **查询返回的原始结果集**，但是还不能直接用，result是 SQLAlchemy 给的一个 **Result 对象**。可以理解成长这样：

```
[
    (Book对象1,),
    (Book对象2,),
    (Book对象3,),
]
```

可以看出来，每一条数据都被**包在元组里**，外面还有一层 Result 壳，不能直接 JSON 序列化，也不能直接 list 遍历。如果不进行进一步处理，这些数据就无法转化为json文件，前端也就拿不到东西。而`scalars().all()`就是做这个工作。

​	`.scalars().all()`：其中`.scalars()` = **把每一行的第一个东西拆出来**，变成可迭代的对象：

```
[Book1, Book2, Book3]
```

​	`.all()`= **把可迭代对象 → 变成真正的列表 list**，最终变成：

```
[
    Book(id=1, bookname="Python入门", ...),
    Book(id=2, bookname="FastAPI实战", ...)
]
```

**最简单的比喻**：

- `execute` → 买回来**一整箱水果**（result）
- `scalars` → 把箱子拆开，拿出水果
- `all` → 摆成一盘，能直接吃



### 6、ORM操作数据-查询数据

​	1、查询所有结果：

```python
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book))
    # book = result.scalars().all()#获取所有结果
    return book
```

​	2、获取表中第一条结果：

```python
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book))
    book = result.scalars().first()#获取符合条件的第一条结果
    return book
```

​	3、获取指定 ID 的结果

```python
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book))
   book = await db.get(Book, 5)#获取指定 ID 的结果
    return book
```

当然这里只是举了三个简单的例子，实际查询数据的操作语句有很多，后面会说。

#### （1）条件查询-比较判断

很多情况下用户的查询结果都是需要条件筛选的，举几个例子：

比较判断： == ; > ; < ; >= ; <=等

模糊查询：like()

与非查询：& ; | ; ~

包含查询：in_()

- 提出需求1： 根据路径参数 书籍ID，来获取表中对应的结果：

```python
@app.get("/book/get_book/{book_id}")
# async def get_book_list(book_id : int,db: AsyncSession = Depends(get_database)):
	result = await db.execute(select(Book).where(Book.id == book_id))
	book = result.scalar_one_or_none()
	return book
```

重点在于`db.execute(select(Book).where(Book.id == book_id))`，这里 select 后面跟上了where，并将**路径参数是否等于表中的id** 作为判断条件来筛选数据。

- 提出需求2：筛选出价格**大于等于**一个数的书籍：

```python
@app.get("/book/get_book/{book_price}")
async def get_book_list(book_price : int = Path(...,description="查找的最低价格"),db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= book_price))
    book = result.scalars().all()
    return book
```

重点在于`db.execute(select(Book).where(Book.price >= book_price))`，这里的where 是以**表中的价格大于等于路径参数**为筛选条件的。



#### （2）条件查询-模糊&与非&包含

- **模糊查询：like()**

提出需求1：书名以 P 开头的所有图书。

```python
@app.get("/book/search_book")
async def get_search_book1(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.bookname.like("P%")))
    #like()里面填 P% 即可，%可以匹配任意多个字符
    return result.scalars().all()
```

提出需求2：书名以 P 开头的一本图书，且图书名只有2个字。

```python
@app.get("/book/search_book")
async def get_search_book1(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.bookname.like("P_")))
	#like()里面填 P_ 即可,有几个 _ 就必须匹配几个
    #P__,必须匹配2个，P___,必须匹配3个，以此类推
    return result.scalars().all()
```

- **与非查询& ; | ; ~**

提出需求：书名以 P 开头的所有图书，而且价格大于等于65。

```python
@app.get("/book/search_book")
async def get_search_book1(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.bookname.like("P%")&(Book.price >= 65)))
    #在多个条件之间加上 & 即可，|、~同理
    return result.scalars().all()
```

- **包含查询：in_()**

提出需求：查询ID为1/3/5的图书

```python
@app.get("/book/search_book")
async def get_search_book1(db: AsyncSession = Depends(get_database)):
    book_list = [1 ,3 ,5]
    result = await db.execute(select(Book).where(Book.id.in_(book_list)))
    #使用Book.id.in_来查询条件包含在列表里的图书
    return result.scalars().all()
```



#### （3）聚合查询

聚合查询：`select( func.方法名( 模型类.属性 ) )`

```python
@app.get("/book/count")
async def get_count(db: AsyncSession = Depends(get_database)):
    #result = await db.execute(select(func.count(Book.id))) #统计总数
    #result = await db.execute(select(func.max(Book.price))) #找出最大值
    #result = await db.execute(select(func.avg(Book.price))) #算出平均值
    #result = await db.execute(select(func.sum(Book.price))) #算出总和
    result = await db.execute(select(func.min(Book.price))) #找出最小值
    return result.scalar() #这里是scalar() ,没有s，提取标量值配合聚合查询使用（就是只提取一个数据，一般最大，最小值用这个）
```



#### （4）分页查询

分页查询：`select().offset().limit()`，其中`offset()`为跳过的记录数，`limit()`为返回的记录数。

**重点：offset值 = （当前页码 - 1）* 每页数量**

示例代码：

```python
@app.get("/book/get_book_list")
async def get_count(
    page :int = 1,#查询的页码
    page_size :int =3,#每一页的记录数
    db: AsyncSession = Depends(get_database)):#对变量进行注解
    #路由函数主体
    skip = (page - 1) * page_size # 算出总共跳了多少记录数
    result = await db.execute(select(Book).offset(skip).limit(page_size))#链式调用offset方法和limit方法，这俩都是select自带的方法
    #通过offset和 limit，最终能筛选出想要的结果
    return result.scalars().all()
```



### 7、ORM操作数据-新增数据

核心步骤：定义ORM对象 → 添加对象到事务：add(对象) → commit提交到数据库。

假设需求：用户输入图书信息（id、书名、作者、价格、出版社） →新增到数据库。

设计思路： 用户输入信息作为参数，向数据库发送请求，将数据提交给数据库，最后把结果返回给用户。

示例代码：

```python
class BookBase(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str

@app.post("/book/add_book")#这里必须用post,因为是添加数据，需要将结果提交给数据库
async def add_book(book: BookBase , db: AsyncSession =Depends(get_database)):
    book_obj = Book(**book.__dict__)#把 book 里的数据变成字典，**是把字典拆成关键字参数
    db.add(book_obj)#把数据暂存到数据库会话
    await db.commit()#提交事务，真正存到硬盘里
    return book#返回给用户
```

这里我们要添加数据，就要使用添加数据的接口，涉及将数据提交给数据库，就要使用`app.post`，	那么也就涉及请求体参数。

要接收请求体，就必须先要对请求体进行注解校验。那么就需要设计一个模型类`BookBase`，用来给`book`注解用。`db`则是数据库对象，用来执行数据库相关的操作。

**重点**：但传过来的**book是Pydantc模型，不能直接存数据库**，而我们写的模型类**Book是ORM模型**，可以直接存进数据库。

- **第一步：`book.__dict__`**

把 Pydantic 模型里的**所有数据变成字典**：

比如前端传：

```json
{
  "id": 1,
  "bookname": "Python入门",
  "author": "张三",
  "price": 59.8,
  "publisher": "人民邮电"
}
```

`book.__dict__` 就会变成：

```python
{
    "id": 1,
    "bookname": "Python入门",
    "author": "张三",
    "price": 59.8,
    "publisher": "人民邮电"
}
```

- **第二步**：`**` （解包符号）

**把字典 “拆成” key=value 格式**

上面的字典经过 `**` 解包后，变成：

```python
id=1, bookname="Python入门", author="张三", price=59.8, publisher="人民邮电"
```

- **第三步：`Book(...)`**

把解包后的数据，**传给数据库模型，创建一个数据库能识别的对象**

最终等价于：

```python
book_obj = Book(
    id=1,
    bookname="Python入门",
    author="张三",
    price=59.8,
    publisher="人民邮电"
)
```



### 8、ORM操作数据-更新数据

核心步骤：查询 get → 属性重新赋值 → commit 提交到数据库

需求：修改图书信息，先查再改。

设计思路： 添加路径参数书籍ID，作用是查找；在添加请求体参数，作用是修改

示例代码：

```python
# 1. 定义更新用的请求体模型（前端传什么、什么类型）
class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str
# 2. PUT 请求：更新书籍，路径上必须传 book_id
@app.put("/book/book_update/{book_id}")
async def book_update(
    book_id: int,          # 路径参数：要更新的书籍ID
    data: BookUpdate,     # 请求体：前端传来的新数据
    db: AsyncSession = Depends(get_database)
):
    # 3. 根据 ID 去数据库查这本书
    db_book = await db.get(Book, book_id)
    # 4. 如果没找到 → 抛 404 错误
    if db_book == None:
        raise HTTPException(status_code=404, detail="Book not found")
        #这里n记得要导入fastapi.HTTPException
    # 5. 把前端传来的新数据 一一 赋值给数据库里的旧数据
    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher
    # 6. 提交保存到数据库（真正更新）
    await db.commit()
    # 7. 返回更新后的书籍数据
    return db_book
```

在 PUT 更新接口中，**路径参数与请求体参数是规范混用**。

路径参数 `book_id` 用于**定位要修改的数据库记录**，告诉后端“改哪条数据”；

请求体参数 `data` 用于**传递更新后的内容**，告诉后端“改成什么样”。



### 9、ORM操作数据-删除数据

核心步骤：查询 get → delete 删除 → commit 提交到数据库（实现思路和更新非常像）

需求：删除指定id的图书信息，先查再改。

设计思路： 添加路径参数书籍ID，作用是查找，如果找到了就删掉。

示例代码：

```python
class BookUpdate(BaseModel):
    bookname: str
    author: str
    price: float
    publisher: str

@app.delete("/book/book_delete/{book_id}")
async def book_delete(book_id: int, db: AsyncSession = Depends(get_database)):
    db_book = await db.get(Book, book_id)
    if db_book == None:
        raise HTTPException(status_code=404, detail="查无此书")
    await db.delete(db_book)
    await db.commit()
    return {"msg": "删除成功"}
```











## 五、头条项目

### 1、工程结构

新建项目`toutiao_backend`，在终端安装FastAPI环境`pip install fastapi uvicorn`

项目结构：

```markdown
toutiao_backend/
├── .venv/               # Python 虚拟环境（依赖隔离）
├── config/              # 配置模块
├── crud/                # 数据操作层
├── models/              # 数据库模型层
├── routes/              # API 路由层
├── schemas/             # 数据校验层（Pydantic）
├── utils/               # 工具函数层
└── main.py              # 项目入口文件
```

**各层核心作用**：

- **.venv/**：隔离项目依赖，避免全局环境污染
- **config/**：管理数据库连接、环境变量等全局配置
- **models/**：定义 ORM 模型，映射数据库表结构
- **schemas/**：用 Pydantic 定义请求 / 响应格式，自动校验数据
- **crud/**：封装数据库增删改查逻辑，解耦接口与数据库
- **routes/**：定义 API 接口，处理 HTTP 请求，调用业务逻辑
- **utils/**：存放密码加密、JWT 生成等通用工具函数
- **main.py**：创建 FastAPI 实例，注册路由，启动项目




### 2、模块化路由

模块化路由就是把每个业务功能的接口**拆分到独立文件里**，在统一挂在到主应用中。如果都放到

main.py 里面，那样会不方便维护。

优势：项目结构更清晰、项目更容易维护。

我们在 routers 文件夹中创建 news.py ，用来写新闻接口。

代码：

```python
from fastapi import  APIRouter
#创建APIrouter实例
# prefix 路由前缀 （主要根据API接口文档书写）
# tags 分组 标签
router = APIRouter(prefix = "/api/news", tags =["news"] )

@router.get("/categories")
async def get_categories():
    return {"message": "获取分类成功"}
```

- `from fastapi import APIRouter`：意思是从 FastAPI 里导入路由工具,作用是用来管理接

  口，不让所有代码都堆在 main.py 里

- `router = APIRouter(prefix = "/api/news", tags =["news"] )`：这是创建一个 “新闻接口

  管理器”，`prefix="/api/news`"相当于此分组下的所有接口前面自动加 `/api/news`，比如你写 

  `/categories`，真实访问地址就是：`/api/news/categories`；`tags =["news"]`给接口分组，

  在接口文档里归类，方便看、方便管理，不和default放一起。



### 3、数据库和ORM配置

连接MySQL数据库，导入提前准备好的SQL脚本文件，在config文件夹创建db_config.py文件，将

ORM的基本配置放进去。

```python
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Float, DateTime
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8"
#这是数据库连接字符串，告诉程序连哪个数据库
#mysql+aiomysql：使用 MySQL 数据库 + 异步驱动 aiomysql
#root：数据库用户名
#123456：数据库密码
#localhost：数据库在本机
#3306：MySQL 默认端口
#FastAPI_first：要连接的数据库名
#charset=utf8：字符编码，支持中文
#创建异步引擎
async_engine = create_async_engine(#异步引擎的配置
    ASYNC_DATABASE_URL,#数据库连接地址()
    echo=True,#可选，输出 SQL 日志
    pool_size=10,#设置连接池活跃的连接数
    max_overflow=20)#允许额外的连接数，也就是说对多能连接30个

class Base(DeclarativeBase):#创建基类
    create_time : Mapped[datetime] = mapped_column(
        DateTime,
        nsert_default=func.now(),
        default=func.now, comment = "创建时间")
    update_time : Mapped[datetime] = mapped_column(
        DateTime,
        insert_default=func.now(),
        default=func.now,
        onupdate=func.now(),
        comment="修改时间")
#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, #指定异步会话类
    expire_on_commit= False#提交后会话不会过期，不会重新查询数据库
)

#依赖项函数，用于获取数据库会话
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session #返回数据库会话给路由处理函数
            await session.commit()#提交事务
        except Exception:
            await session.rollback()# 如果有异常，回滚
            raise
        finally:
            await session.close()#关闭会话


```



### 4、接口实现流程

1. 模块化路由 →  API 接口文档
2. 定义模型类 → 数据库表（数据库设计文档）
3. 在 crud 文件夹；里面创建文件，封装操作数据库的方法
4. 在路由处理函数里面调用 crud 封装好的方法，响应结果

### 5、新闻模块

#### （1）获取新闻分类-模块化路由

根据API接口文档进行新闻分类接口的模块化路由。API 接口文档具体请看项目物料。

```python
from fastapi import  APIRouter
#创建APIrouter实例
# prefix 路由前缀 （主要根据API接口文档书写）
# tags 分组 标签
router = APIRouter(prefix = "/api/news", tags =["news"] )

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 10):
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": "新闻分类列表"
    }
```



#### （2）获取新闻分类-定义模型类-编写查询方法

定义模型类：

```python
from datetime import datetime
from sqlalchemy import DateTime, Integer,String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):#基类
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

class Category(Base):#模型类
    __tablename__ = "news_category"#表名要与数据库里的目标表名一致
    id: Mapped[int] = mapped_column(Integer,primary_key=True, autoincrement=True, comment="分类id")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序")

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"
    #__repr__ 是 Python 类里的特殊方法（魔术方法），用来定义对象被打印 / 查看时的字符串表现形式。
    # 给对象一个清晰、可阅读的字符串描述，方便调试和查看对象信息。
    # 当你执行 print(对象) 或在控制台直接输入对象名时，Python 会自动调用这个方法。
    # 好的 __repr__ 应该尽量能还原出创建这个对象的代码（方便调试）。
    #类似于 __str__，但 __str__ 更偏向用户。
```

编写查询方法：

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category

async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 10):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
```

前端调用接口：

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_database
from crud import news

#创建APIrouter实例
# prefix 路由前缀 （主要根据API接口文档书写）
# tags 分组 标签
router = APIRouter(prefix = "/api/news", tags =["news"] )

@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_database)):
    #先获取数据库里面新闻分类数据 →先定义模型类 → 封装查询数据方法
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "获取新闻分类成功",
        "data": categories
    }
```

#### （3）解决跨域问题

**跨域资源共享CORS**：跨域资源共享（CORS）是一种浏览器安全机制，用于允许运行在一个源

（Origin）的Web应用，通过浏览器想另一个源的服务器发起跨域HTTP请求，并在服务器授权的前

提下获取资源。

同源：协议、域名、端口完全相同，浏览器允许自由发送请求，不受限制。

跨域：只要协议、域名、端口任意一个不同，浏览器就会拦截请求，出现跨域报错。

同源要保证前后端两个地址必须 **3 个都一样**：

- 协议相同（http /https）
- 域名相同（[localhost](https://localhost) / 127.0.0.1）
- 端口相同（8000 / 8080）

如果没解决跨域问题，一般会报：

```error
Access to XMLHttpRequest at 'http://localhost:8000/xxx' from origin 'http://127.0.0.1:5500' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**解决(全局配置CORS中间件)**：在后端main文件下，导入：`from fastapi.middleware.cors import CORSMiddleware`

在文件中添加：

```python
# 导入跨域中间件（解决前端访问后端的跨域问题）
from fastapi.middleware.cors import CORSMiddleware

# 给 FastAPI 应用添加跨域支持
app.add_middleware(
    CORSMiddleware,        # 使用 FastAPI 自带的跨域中间件
    allow_origins=["*"],   # 允许所有来源（域名/IP）访问，* 代表全部
    allow_credentials=True,# 允许携带 Cookie/凭证跨域
    allow_methods=["*"],   # 允许所有请求方法（GET、POST、PUT、DELETE 等）
    allow_headers=["*"]    # 允许所有请求头信息
)
```

**注意**：开发过程中可以允许所有来源的请求，单是实际上线后，万万不可。

应该：

```python
app.add_middleware(
    CORSMiddleware,
    # 只允许你的前端域名访问
    allow_origins=[
        "https://www.你的域名.com",
        "https://你的域名.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 只开实际用到的请求方法
    allow_headers=["Content-Type", "Authorization"], # 只允许必要请求头
)
```



#### （4）获取新闻列表

注册路由：

```python
# 新闻列表接口：GET 请求 /api/news/list
@router.get("/list")
async def get_news_list(
        # 前端传分类ID，别名categoryId（驼峰），必填
        category_id: int = Query(..., alias="categoryId"),
        # 页码，默认第1页
        page: int = 1,
        # 每页条数，默认10，最大不超过100，别名pageSize
        page_size: int = Query(10, alias="pageSize", le=100),
        # 依赖注入：获取数据库异步会话
        db: AsyncSession = Depends(get_database)
):
    # 分页计算：offset = 第几条开始（跳过前面的数据）
    offset = (page - 1) * page_size

    # 调用DAO层方法：查询当前页的新闻列表
    news_list = await news.get_news_list(db, category_id, offset, page_size)

    # 调用DAO层方法：统计该分类下新闻总条数
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_list)) < total

    # 统一返回格式：code、message、data（列表+总数）
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {
            "list": news_list,    # 当前页新闻数据
            "total": total,       # 总条数（用于前端分页）
            "hasMore": has_more  # 是否有下一页（我帮你补全了）
        }
    }
```

编写模型类：

```python
class News(Base):
    __tablename__ = "news"

    # 创建索引：提升查询速度 → 添加目录
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),  # 高频查询场景
        Index('idx_publish_time', 'publish_time')  # 按发布时间排序
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
```

写获取新闻列表和统计分类新闻个数

（1）根据分类ID获取新闻列表（带分页）：

```python
# 2. 根据分类ID获取新闻列表（带分页）
async def get_news_list(
    db: AsyncSession,      # 数据库异步会话
    category_id: int,      # 新闻分类ID（要查哪个分类下的新闻）
    skip: int = 0,         # 分页：跳过N条
    limit: int = 10       # 分页：取N条
):
    # 构建SQL：查询News表，筛选分类ID=指定值，分页
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    # 执行SQL
    result = await db.execute(stmt)
    # 返回新闻列表
    return result.scalars().all()
```

（2）根据分类ID统计该分类下一共有多少条新闻（给分页用）

```python
# 3. 根据分类ID统计该分类下一共有多少条新闻（给分页用）
async def get_news_count(
    db: AsyncSession,      # 数据库异步会话
    category_id: int       # 分类ID
):
    # 构建SQL：统计News表中，该分类下的新闻总数量 count(id)
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    # 执行SQL
    result = await db.execute(stmt)
    # 返回唯一的统计结果（总条数）
    return result.scalar_one()
```





#### （5）获取新闻详情

先编写路由函数：

```python
@router.get("/detail")
async def get_news_detail(
    id: int = Query(..., alias="id"),
    db: AsyncSession = Depends(get_database)
):#获取新闻详情+浏览量+1+相关新闻
    news_detail = await news.get_news_detail(db, id)
    if not news_detail:#检查新闻是否存在，如果不存在，直接返回 404 给前端，终止后续流程
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:#检查更新操作是否真的命中了数据。
        raise HTTPException(status_code=404, detail="新闻不存在")
    return {
            "code": 200,
            "message": "success",
            "data": {
                "id": news_detail.id,
                "title": news_detail.title,
                "content": news_detail.content,
                "image": news_detail.image,
                "author": news_detail.author,
                "publishTime": news_detail.publish_time,
                "categoryId": news_detail.category_id,
                "views": news_detail.views,
                "relatedNews": []
            }
    }
```

编写查询函数（供路由函数调用）:

```python
# 4. 根据新闻ID获取新闻详情
async def get_news_detail(
    db: AsyncSession,
    news_id: int
):
    # 构建SQL：查询News表，筛选ID=指定值
    stmt = select(News).where(News.id == news_id)
    # 执行SQL
    result = await db.execute(stmt)
    # 获取结果并返回
    return result.scalar_one_or_none()
```

编写更新新闻浏览量函数：

```python
# 5. 根据新闻ID更新新闻浏览量
async def increase_news_views(
        db: AsyncSession,
        news_id: int
):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
# 我在异步引擎那里不是写了提交数据库吗？为啥这里还要写？
# db_config 里的 commit：管整个请求的事务，最后才执行。
# 函数里的 commit：管当前这条更新操作，让修改立刻生效。
# 你现在要的是「浏览量 +1 后马上能看到新值」，所以必须在 increase_news_views 里写 await db.commit()。

#更新 → 检查数据库是否是否真的命中了数据 → 命中了返回True
    return result.rowcount > 0 #如果本次更新操作影响了至少 1 行数据 → 返回 True，否则返回 False
```





#### （6）获取相关新闻

路由函数：在新闻详情里面进行了改动

```python
@router.get("/detail")
async def get_news_detail(
    id: int = Query(..., alias="id"),
    db: AsyncSession = Depends(get_database)
):#获取新闻详情+浏览量+1+相关新闻
    news_detail = await news.get_news_detail(db, id)
    if not news_detail:#检查新闻是否存在，如果不存在，直接返回 404 给前端，终止后续流程
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.increase_news_views(db, news_detail.id)
    if not views_res:#检查更新操作是否真的命中了数据。
        raise HTTPException(status_code=404, detail="新闻不存在")
        
    related_news = await news.get_news_list(#增加了这个
        db, 
        news_detail.id, 
        news_detail.category_id, 
        limit = 5)
    return {
            "code": 200,
            "message": "success",
            "data": {
                "id": news_detail.id,
                "title": news_detail.title,
                "content": news_detail.content,
                "image": news_detail.image,
                "author": news_detail.author,
                "publishTime": news_detail.publish_time,
                "categoryId": news_detail.category_id,
                "views": news_detail.views,
                "relatedNews": related_news#修改了这个
            }
    }
```

编写查询函数：

```python
async def get_related_news(
    db: AsyncSession,
    news_id: int,
    category_id: int,
    limit : int = 10
):
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(#排序
        News.views.desc(),#默认是升序，降序是desc()
        News.publish_time.desc()
    ).limit(limit)#限制5个
    result = await db.execute(stmt)
    related_news = result.scalars().all()
    # 列表推导式 推导出新闻的核心数据，然后再 return
    return [
        {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publishTime": news_detail.publish_time,
            "categoryId": news_detail.category_id,
            "views": news_detail.views
        }
        for news_detail in related_news
    ]
```

重点理解：排序与列表推导式的作用

列表推导式可以拆成两部分理解：

**① 循环部分：for news_detail in related_news**

- 遍历 `related_news` 列表，把每一个 `News` 对象，临时命名为 `news_detail`

- 就像写了个 

  for循环：

  ```python
  result_list = []
  for news_detail in related_news:
      # 做些事
      result_list.append(...)
  ```

**② 字典部分：{ ... }**

- 对每一个 `news_detail`对象，提取它的属性，

  重新命名成前端要的字段名：

  - `news_detail.id` → `"id"`
  - `news_detail.title` → `"title"`
  - `news_detail.publish_time` → `"publishTime"`（驼峰命名，前端习惯）
  - `news_detail.category_id` → `"categoryId"`

- 最后把这些字典**塞进一个大列表**里，就是最终返回给前端的 `relatedNews` 数组









### 6、用户模块

#### （1）基础路由

首先先在main函数进行路由注册：`app.include_router(users.router)`

编写路由函数文件：

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_database
from schemas.users import UserRequest

router = APIRouter(prefix = "/api/user", tags =["users"])

@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_database)):
    return {
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": user_data.username,
      "bio": "这个人很懒，什么都没留下",
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    }
  }
}
```

编写类型校验文件：

```python
from pydantic import BaseModel
#类型校验代码
class UserRequest(BaseModel):
    username: str
    password: str
```



#### （2）用户注册

整体思路：

```markdown
开始
  ↳ 接收注册参数
  ↳ 校验参数格式
  ↳ 查询用户名是否存在
        ↓ 存在        ↓ 不存在
  抛出用户名重复异常   密码加密
                      ↓
                  创建用户到数据库
                      ↓
                  生成访问 Token
                      ↓
            返回成功信息 + Token
结束
```

这节重点是注册密码的加密环节：

首先在utls里创建security.py，

```python
from passlib.context import CryptContext
# 创建密码上下文
pwd_context =CryptContext(schemes=["bcrypt"], deprecated="auto")
#全局密码加密工具实例
#密码加米
def get_hash_password(password: str):
    return pwd_context.hash(password)
```

然后在crud/user.py中添加以下代码：

```python
#创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    #先进行密码加密，切不可直接把密码保存在数据库中
    hashed_password = security.get_hash_password(user_data.password)#调用自己写的密码加密方法
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)#refresh 的作用：获取数据库自动生成的字段（特别是 id）！
    return user
```

**重点**：这里的`db.fresh()`的作用

1. 核心作用

   **从数据库重新加载当前对象的完整数据，同步数据库自动生成 / 更新的字段到内存对象中。**

2. 典型场景

- 插入新数据后（`INSERT`）：获取数据库自增 `id`、默认字段（如 `created_at`、`avatar`）
- 更新数据后：同步数据库 `onupdate` 自动更新的字段（如 `updated_at`）

3. 为什么需要它？

- `db.add()`：仅将对象加入**会话缓存**，未写入数据库
- `db.commit()`：将缓存写入数据库，但**内存中的对象不会自动更新**
- `db.refresh()`：主动去数据库查询当前对象，把最新数据覆盖到内存对象