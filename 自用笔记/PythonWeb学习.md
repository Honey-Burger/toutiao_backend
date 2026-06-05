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
- 

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



#### （2）用户注册-创建用户

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

这节重点是**注册密码的加密环节**：

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



#### （3）用户注册-生成Token

Token:是服务器发给客户端的一段字符串，用来在后续请求中证明"你已经登录过了"

作用：解决HTTP是无状态的问题，在每次请求中“自我证明身份”

Token在请求中的位置：**请求头**

`Authorization: Bearer <token>`

`Authorization`:专门用来存放身份信息

`Bearer`:表示“持有者令牌”

`<token>`:真正的身份凭证



#### （4）封装通用成功响应格式

大致流程为下：抽取响应结果→定义数据类型→调用函数响应结果

- **抽取响应结果**

首先先封装响应结果：

```python
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
def success_response(message: str = "success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    #data的数据格式多变，重点是data的数据结构怎么定义。通过schemas/users.py中的UserAuthResponse类定义

    #目标：把任何的FastAPI、Pydantic、ORM 对象都要正常响应 → code、message、data
    return JSONResponse(content=jsonable_encoder( content))
    #jsonable_encode 就是把「Python 不能转成 JSON 的东西」变成「能转成 JSON 的东西」
    #JSONResponse = 告诉前端：我给你返回的是 JSON 格式！
```

这里定义了`success_response()`方法，将参数以及响应给前端的东西写进方法体里面。统一赋值给content，最后return给前端。

但这里发现，message的类型很好注解，但是传进来的data类型是多变的。那**怎么解决data的数据类型呢？**



- **定义数据类型**

在schemas文件夹中的users.py，来解决这个问题。我们在原来的基础上，分别定义了三个类：

`UserInfoBase(BaseModel)`，`UserInfoResponse(UserInfoBase)`，`UserAuthResponse(BaseModel)`

```python
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


#类型校验代码
class UserRequest(BaseModel):
    username: str
    password: str

#user_ info 对应的类：基础类 + Info 类 （id、用户名）
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="用户昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="用户头像地址")
    gender: Optional[str] = Field(None, max_length=10, description="用户性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象获取值
    )
#data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias = "userInfo")

    #模型类配置
    model_config = ConfigDict(
        populate_by_name = True, #alas / 字段名兼容
        #你可以写 UserAuthResponse(user_info=xxx) ✅
        #也可以写 UserAuthResponse(userInfo=xxx) ✅
        from_attributes = True,# 允许从 ORM 对象获取值
    )
```

先写一个最基础的类`UserInfoBase(BaseModel)`，里面定义的是经常要用到的数据，后面要特别定义的类，直接继承就可以。

然后定义类`UserInfoResponse(UserInfoBase)`，这个类就是在基础类的基础上特别定义了一个类。留着后面用来过滤我们从数据库取出来的ORM对象的字段，只留下我们在这个类里面定义的字段。

最后定义类`UserAuthResponse(BaseModel)`，这个类最终决定我们返回给前端的data的数据类型。其中有token，还有`UserInfoResponse(UserInfoBase)`里面定义的字段。



- **调用函数响应结果**

定义了data的数据类型，也定义了返回函数`success_response`，最终都要在路由函数里面统一调用：

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_database
from crud.users import create_token
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from crud import users
from utils.response import success_response

router = APIRouter(prefix = "/api/user", tags =["users"])

@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_database)):
    # 注册逻辑：验证数据库是否存在，创建用户，生成Token，响应结果
    exciting_user =  await users.get_user_by_username(db, user_data.username)
    if exciting_user:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    token =await users.create_token(db,user.id)
#     return {
#   "code": 200,
#   "message": "注册成功",
#   "data": {
#     "token": token,
#     "userInfo": {
#       "id": user.id,
#       "username":user.username,
#       "bio": user.bio,
#       "avatar": user.avatar
#     }
#   }
# }
    response_data = UserAuthResponse(
        token = token,
        userInfo = UserInfoResponse.model_validate(user)
        #直接接收ORM对象，转换成前端能看懂的 JSON 模型
        #这里useInfo只会存UserInfoResponse类里定义的字段，未定义的不会显示，会直接被过滤掉
    )
    return success_response(message = "注册成功", data = response_data)
```

这里我将原先的响应格式作注释，用来对比，可以很明显发现，现在响应体格式都被封装了起来，而且调整起来更加灵活，只需要在路由函数里调用`success_response(message = "注册成功", data = response_data)`即可。

这里是将`response_data`赋值给`data`，这里重点看`response_data`的数据类型是怎么定义的。

可以看到，对象`response_data`的数据类型是`UserAuthResponse`，也就是里面包含`token`，和一个`UserInfoResponsed`对象`userInfo`。而`userInfo`对象里面包含了其类定义的字段。

那么`UserInfoResponse.model_validate(user)`**是干嘛的呢**？

这里是根据`UserInfoResponse`定义的字段，**对从数据库里拿出来的ORM对象里的字段进行筛选**。`UserInfoResponse`类里定义的字段将**进行保留**，赋给`UserInfo`对象，而其他字段（密码、id等等）将直接过滤掉。

- 运行测试结果

这里随便注册一个用户，看看docs文档响应结果：

```
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "21b4055f-dd30-4531-9975-d85a01e4791e",
    "userInfo": {
      "nickname": null,
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
      "gender": "unknown",
      "bio": "这个人很懒，什么都没留下",
      "id": 13,
      "username": "wjy863"
    }
  }
}
```

可以看出来，响应体严格执行了我们定义的响应格式。这种封装可以使代码解耦，响应函数也可以在后续中通用，非常方便。



#### （5）封装全局异常处理器

全局异常处理器是注册在FastAPI应用级别的**异常处理函数**，用于捕获业务层、数据库层以及系统抛出的异常，并以**统一的响应格式返回给前端**。

大致为两个步骤：定义异常处理器 → 全局注册异常处理器

- **定义异常处理器**

这里先写4个异常处理器，分贝负责业务层报错、数据完整性约束、数据库层面的报错以及全局错误。

全局异常处理是**通用工具类代码**，所里这里在文件夹utils里面创建exception.py

```python
import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status

# 开发模式：返回详细错误信息
# 生产模式：返回简化错误信息
DEBUG_MODE = True  # 数字项目保持开启

async def http_exception_handler(request: Request, exc: HTTPException):
    # 处理 HTTPException 异常
    # HTTPException 通常是业务逻辑主动抛出的，data 保持 None
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    # 处理数据库完整性约束错误
    error_msg = str(exc.orig)

    # 判断具体的约束错误类型
    if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "FOREIGN KEY" in error_msg:
        detail = "关联数据不存在"
    else:
        detail = "数据约束冲突，请检查输入"

    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": detail,
            "data": error_data
        }
    )

async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    # 处理 SQLAlchemy 数据库错误
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "数据库操作失败，请稍后重试",
            "data": error_data
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    # 处理所有未捕获的异常
    # 开发模式下返回详细错误信息
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            # 格式化异常信息为字典，方便日志记录和调试
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": error_data
        }
    )
```

这里4种异常函数就写好了，接下来就是怎么调用的事情。

- **全局注册异常处理器**

这里我们要调用异常处理器，首先就要将其注册。但4种函数我们不能一一在main函数进行注册，这不符合工程化的思想。这里我们在utils再创建exception_handlers.py，编写一个函数专门负责注册异常处理函数，然后在main函数里面调用它。

```python
from utils.exception import http_exception_handler, integrity_error_handler, general_exception_handler, \
    sqlalchemy_error_handler

sqlalchemy_error_handler
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def register_exception_handlers(app):
    """
    注册全局异常处理：子类在前，父类在后；具体在前，抽象在后
    """
    app.add_exception_handler(HTTPException, http_exception_handler)#(异常类型，处理函数)，是业务层的报错
    app.add_exception_handler(IntegrityError, integrity_error_handler)#数据完整性约束
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)#数据库层面的错误
    app.add_exception_handler(Exception, general_exception_handler)#全局错误，兜底用

```

最后在main函数添加`register_exception_handlers(app)`，调用注册函数，这样一个封装的全局异常处理器就可以在测试中使用了。



#### （6）用户登录

登录逻辑：验证数据库是否存在用户，验证密码，生成Token，响应结果

路由函数添加：

```python
@router.post("/login")
async def login(user_data: UserRequest,db: AsyncSession = Depends(get_database)):
    # 登录逻辑：验证数据库是否存在用户，验证密码，生成Token，响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db,user.id)
    response_data = UserAuthResponse(
        token = token,
        userInfo = UserInfoResponse.model_validate(user)
    )
    return success_response(message = "登录成功", data = response_data)
```

其中多了`users.authenticate_user()`函数，用来验证用户是否存在，密码是否正确。

在crud/user.py中定义`users.authenticate_user()`：

```python
async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)#获取用户(有可能没有)
    if not user:#用户不存在,返回 None
        return None
    if not security.verify_password(password, user.password):#密码验证失败，返回 None
        return None
    return user#密码验证成功，返回用户对象
```

可以发现，这里面多了一个新函数`security.verify_password()`，这个函数是用来验证用户输入密码是否和数据库里的密码一样的。

这里将在utils/security.py 定义函数：

```python
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
    # 验证密码,返回值为布尔值
```

这样用户登录的基本逻辑就实现完成。



#### （7）获取用户信息

整体思路：查Token用户 → 封装CRUD → 在路由函数中调用

首先在crud/users.py里定义函数`get_user_by_token(db: AsyncSession, token: str)`：

```python
#根据 Token 查询用户 ： 验证 Token → 验证用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
    """
    这里为什么还要使用scalar_one_or_none()：
    如果数据库出现脏数据（比如 user_id 重复），
    scalar_one() 会直接炸，
    而 scalar_one_or_none() 至少能让你拿到 None，再在调用层处理。
    """
```

这里引申出一个思路，我们发现。获取用户信息需要查询用户Token，返回用户对象，修改用户信息也需要返回用户对象，删除用户信息也需要返回用户对象，那么就可以把获取用户**封装成一个通用函数**，放在文件夹utils里。

我们创建utils/auth.py，代码如下：

```python
#整合 根据 Token 查询用户，返回用户
from fastapi import Header, Depends,HTTPException
from starlette import status
from config.db_config import get_database
from crud import users

async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db = Depends(get_database)
):
    #前端传过来：Bearer eyJxxxxxxxxxxx.token.string, 这里只取token
    token = authorization.replace("Bearer", "")
    """
    方法二：token = authorization.split(" ")[1],也就是把列表分割，取后面那个。
    """
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的的令牌")
    return user
```

最后，在路由函数里调用函数：

```python
@router.get("/info")#查Token用户 → 封装CRUD → 功能整合成一个工具函数 → 路由导入使用：依赖注入
async def get_user_info(user :User = Depends(get_current_user)):
    return success_response(
        message = "获取用户信息成功",
        data = UserInfoResponse.model_validate( user))
```

这里采用依赖注入的方式调用`get_current_user`，只有 FastAPI 的路由函数 / 依赖函数 才能用依赖注入，普通函数则不行。

依赖注入 = FastAPI 自动帮你调用函数、自动帮你传参，你只需要声明要什么，不用自己调用和传参。



#### （8）修改用户信息

主要思路就是在查找用户的基之上修改对应的字段值，更新用户信息。

常规思路就是先写更新函数。然后在路由函数里调用更新函数。

但这里写更新函数时遇到一个新问题，我们怎么**精准的修改用户想修改的那些值，而不去动用户没有修改的那些值**呢？

我们可以像之前写用户信息那样，再写一个Pydantic类，用来限制和校验前端传来的对象，然后通过检测对象中的哪些字段改了，哪些字段没改，来精准的进行修改操作。

在schemas/users.py中定义`UserUpdateRequest(BaseModel)`模型类：

```python
class UserUpdateRequest(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None
```

这里字段默认值都设置为None，这样哪个字段真正进行了改动，就不会为None，改动的时候我们把None过滤掉就行，不然原本有东西的字段也被修改为没有了。

在crud/users.py中定义更新函数`update_user`

```python
#更新用户信息
async def update_user(db: AsyncSession,username: str,
                      user_data: UserUpdateRequest,
                      ):
    # update(User).where(User.name == username).values(字段 = 值)
    # user_data 是一个Pydantic类型对象，必须进行解包变成字典才能变成字段=值的形式使用
    #没有设置值的不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset= True,
        exclude_none= True  ))#修改操作
    result = await db.execute(query)#奖结果赋给result，以便后面检查是否真的进行了更新
    await db.commit()
    #检查更新
    if result.rowcount == 0:#如果用户不存在，更新失败，抛出异常
        raise HTTPException(status_code=404, detail="用户不存在")
    #获取更新后的用户信息
    updated_user = await get_user_by_username(db, username)
    return updated_user
```

可以注意到，这里我们是两个实参。这个函数的重点是，怎么解决过滤字段的问题。

在数据库操作中，我们可以发现`.values(**user_data.model_dump(exclude_unset= True,exclude_none= True  )`

`model_dump`函数就是将Pydantic模型转换成字典，参数`exclude_unset= True`表示未设置的值都给过滤掉，参数`exclude_none= True`表示值为None的都给过滤掉。这和函数就直接解决了过滤字段的问题。

然而ORM模型是接受不了字典的，需要接收字段=值的形式，所以这里前面还要加上**进行解包，才能使用。

最后在routers/users.py写路由函数：

```python
#修改用户信息：验证Token → 验证用户是否存在 → 修改用户信息（用户输入数据 put提交 → 请求体参数 → 定义Pydantic模型类）→ 响应结果
#参数： 用户输入的 + 验证Token的 + db（调用更新的方法）
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest,
                           user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_database)
                           ):
    user = await users.update_user(db, user.username, user_data)
    # 修改用户信息逻辑：验证数据库是否存在用户，修改用户信息，响应结果
    return success_response(message = "更新用户信息成功", data=UserInfoResponse.model_validate(user))
```



#### （9）修改用户名密码

大致思路：先进入请求，验证用户是否登录，登录之后再次验证密码，如果一致就将新密码转密文，更新密码，响应结果。

鉴于密码属于隐私字段，所以不推荐直接以参数的方式被函数调用。因此我们`schemas/users.py`创建Pydantic模型类：

```python
class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword",description="旧密码")
    new_password: str = Field(..., min_length=6,alias="newPassword",description="新密码")
```

这样可以保证密码字段不会直接裸露在外，而且可以对传进来的对象进行字段校验。



写好模型类，进行修改密码的逻辑部分开发。在`crud/users.py`里增加函数`change_password（）`：、

```python
#修改密码： 验证旧密码 → 新密码加密 → 修改密码
async def change_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False
    hashed_new_pwd = security.get_hash_password(new_password)
    user.password = hashed_new_pwd
    db.add(user)
    '''
    当你在这个函数里修改 user.password = hashed_new_pwd 时，
    只是改了 Python 对象的属性，并没有告诉当前的 db 会话 “我要更新这个对象”。
    新的 db 会话并不知道这个 user 对象的存在，也不知道它被修改了。
    对于已存在的数据库对象（不是新创建的），add() 不会执行 INSERT，
    而是把这个对象关联到当前会话，让会话知道：
    “这个对象被修改了，等下 commit() 的时候要帮我生成 UPDATE 语句。”
    在异步会话里，只要是修改已存在的数据库对象，就必须先 db.add() 让会话 “看见” 它，
    否则 commit() 不会生效。
    '''
    await db.commit()
    await db.refresh(user)
    return True
```

这里重点要理解`add(user)`的作用。

这两个都写好了，直接添加到路由函数里进行调用：

```python
@router.put("/password")
async def update_user_password(
        password_data: UserChangePasswordRequest,
        user: User = Depends(get_current_user),#验证Token,用户是否登录
        db: AsyncSession = Depends(get_database)
):
    res_change_pwd = await users.change_password(db, user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败哦，待会再试")
    return success_response(message = "修改密码成功")
```





### 7、收藏模块

#### （1）检查新闻收藏状态

大致思路：先进入请求，验证用户是否登录，检查用户是否收藏当前新闻，响应结果。

从路由函数下手，路由函数参数肯定要有news_id，user，然后进行检查操作，最后响应结果。

接着分析crud的函数，里面需要路由函数传参，然后在数据库表里进行数据库操作。

而数据库操作的语句要用到ORM模型类所以我们先写ORM模型类：

在文件夹models里创建favorite.py

```python
from datetime import datetime
from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.news import News
from models.users import User

class Base(DeclarativeBase):
    pass

class Favorite(Base):
    """
    收藏表ORM模型
    """
    __tablename__ = 'favorite'

    # 创建索引 & 联合唯一约束：一个用户不能重复收藏同一篇新闻
    #UniqueConstraint:唯一约束，当前用户，当前新闻，只能收藏一次
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('fk_favorite_news_idx', 'news_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="收藏时间")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, created_at={self.created_at})>"
```

这样模型类创建好之后，就方便写数据库操作语句了。

接下来在文件夹crud里面创建favorite.py：

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite


async def is_news_favorite(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    query = select(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
    result = await db.execute(query)
    #是否有收藏记录
    return result.scalar_one_or_none() is not None#判断语句：有收藏记录返回True，无收藏记录返回False
```

注意这里函数返回的是布尔类型的值，返回语句那里添加了一个 is not None，作用看代码里的解释。

接下来就是路由函数，但是在写路由函数之前，我们要考虑返回给前端的语句中`success_response(message: str = "success", data = None)`的data怎么写。

在API接口文档中，明确写出我们返回的数据类型是布尔型，但是即使这里只有一个返回值，我们还是要写Pydantic模型类，再将其塞到success_response函数中，统一格式。

在schema中创建favorite.py：

```python
from pydantic import BaseModel, Field


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(...,alias = "isFavorite")
```

最后完事具备，再编写路由函数，在routers文件夹里创建favorite.py：

```python
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_database
from crud import favorite
from models.users import User
from schemas.favorite import FavoriteCheckResponse
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")#检查新闻是否被收藏
async def check_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    is_favorite = await favorite.is_news_favorite(db, user.id, news_id)
    return success_response(message="查询收藏状态成功",data = FavoriteCheckResponse(isFavorite = is_favorite))
```



#### （2）添加收藏

大致思路：进入请求→验证用户是否登录→添加收藏→响应结果

先建立Pydantic模型类：

```python
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")
```

再编写操作函数：

```python
async def add_news_favorite(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    favorite = Favorite(user_id=user_id, news_id=news_id)
    #创建ORM实例
    db.add(favorite)
    """
    Favorite 实例是全新的、未被数据库管理的对象，
    db.add() 的作用就是把它 “注册” 到当前会话，让 SQLAlchemy 知道要把它插入到数据库。
    """
    await db.commit()
    await db.refresh(favorite)
    return favorite
```

编写路由函数调用：

```python
@router.post("/add")
async def add_favorite(
        data: FavoriteAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    result = await favorite.add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data = result)
```



#### （3）取消收藏

进入请求→验证用户是否登录→删除收藏表内当前新闻→检查命中结果＞0 → 响应结果

逻辑函数：

```python
async def remove_news_favorite(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    favorite =Favorite(user_id=user_id, news_id=news_id)
    if favorite:#如果收藏记录存在，则删除
        stmt = delete(Favorite).where(Favorite.user_id == user_id,Favorite.news_id == news_id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0#删除成功返回True，否则返回False
```

这里返回布尔值

路由函数：

```python
@router.delete("/remove")
async def remove_favorite(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    result = await favorite.remove_news_favorite(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")
    return success_response(message="删除收藏成功", data = result)
```

这里接口文档要求的是路径参数，所以就不特意创建Pydantic模型类了



#### （4）获取收藏列表

在编写路由函数之前，我们先书写CRUD函数。

在crud/favorite.py里创建函数`get_favorite_list`

```python
#获取收藏列表：获取某个用户的收藏列表 + 分页功能
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    # 总量 + 收藏的新闻列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    #这里的 func.count() 是聚合函数，数据库会计算后返回一行一列的结果
    count_result = await db.execute(count_query)#执行 SQL
    total = count_result.scalar_one()
    
    offset = (page - 1) * page_size
    #获取收藏列表 - 联表查询 join() + 收藏时间排序 + 分页
    #select(查询主体模型类，字段别名).join(联合查询的模型类，联合查询的条件).where(条件).order_by().offset().limit()
    #别名： Favorite.created_at.label("favorite_time")
    query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
                   .join(Favorite, Favorite.news_id == News.id).
                   where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())#按照收藏的时间降序
                   .offset(offset).limit(page_size)
             )
    result = await db.execute(query)
    row = result.all()
    return total, row
'''row = [
    (News对象1, datetime1, favorite_id1),
    (News对象2, datetime2, favorite_id2),
    (News对象3, datetime3, favorite_id3),
    ...
]
'''
```

首先规定传进来4个参数，分别是数据库会话对象，用户id，页数和每页大小。

这个函数目的是返回两个值：收藏新闻总数 total 和收藏的新闻列表 row 。两个返回值的作用将会在路由函数中详细说明。

这里的重点是联表查询语句，首先我们先搞清楚这里使用的联表查询的**语法格式**：

```python
query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id")).join(Favorite, Favorite.news_id == News.id).
where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())#按照收藏的时间降序
.offset(offset).limit(page_size))
```

select(查询主体模型类，字段别名).join(联合查询的模型类，联合查询的条件).where(条件).order_by().offset().limit()。

**首先，为什么要进行联表查询呢？**

因为我们这里获取收藏新闻列表，不仅要知道新闻的收藏时间，新闻ID（在favorite表），还要知道这条新闻的作者，标题（在news表），很显然，这是一张表做不到的。

所以我们把两张表贴在一起，这里就是把favorite表贴（join）在news表上，并且我们限制联合的条件是`Favorite.news_id == News.id`。

**在where里已经书写条件了，为什么还要在联表查询里面书写条件**？

两个条件各司其职

JOIN 条件：`Favorite.news_id == News.id`，作用：**定义两张表怎么"拼接"**，这就像在说："把 favorite 表的每一行，和 news 表中 id 匹配的行连在一起"，如果没有这个条件，数据库不知道该怎么对应两张表的数据。

WHERE 条件：`Favorite.user_id == user_id`，作用：**从拼接好的大表中"筛选"出需要的数据**，这就像在说："我只想要用户5的收藏记录"。

**关于字段别名**：

这里代码中写到`News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id")`

这里我们用`.label()`给这两个字段起了别名,但**为什么要起别名**呢？

主要原因是因为字段名冲突，两张表都有 id 和 created_at 字段：

`news.id` - 新闻ID

`favorite.id` - 收藏记录ID

`news.created_at` - 新闻创建时间

`favorite.created_at` - 收藏时间

如果不取别名，返回结果会有两个 id 和两个 created_at，数据库不知道哪个是哪个，会导致：
数据覆盖（后面的覆盖前面的），前端拿到错误的值。

这里数据库语句被执行之后，会将返回值给row，这里row的格式是元素为元祖的列表，每个元祖包含三个元素：

```python
'''row = [
    (News对象1, datetime1, favorite_id1),
    (News对象2, datetime2, favorite_id2),
    (News对象3, datetime3, favorite_id3),
    ...
]
'''
```



这里CRUD函数已经写完，此时应该去路由函数调用：

```python
@router.get("/list")
async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    favorite_list = [
        {
            **news.__dict__,
            "favorite_time": favorite_time,
            "favorite_id": favorite_id
        } for news, favorite_time, favorite_id in rows
    ]
    has_more = total > page * page_size
    rows, total =await favorite.get_favorite_list(db, user.id, page, page_size)
    return success_response(message="获取收藏列表成功")
```

在上面我们说过，row是元祖的形式，我们需要**转换成字典的格式**，方便转JSON传给前端，所以这里直接对news对象进行解包，展开里面的所有属性，再加上后面两个属性（此时字段别名的作用体现出来），再用列表推导式将每一行数据都处理成我们需要格式。

然后再加上一个变量`hasMore`，这个变量我们在获取新闻列表的时候就说到过，用来判断当前页的后面是否还有新闻。

现在有一个问题，我们最终要向前端返回data，这个data是什么数据结构呢？total和row又有什么用？

首先我们要明白我们最终要返回给前端什么东西，首先肯定是收藏的新闻列表，还有就是收藏总数，当然还要有`hasMore`，用来判断当前页的后面是否还有新闻，为bool类型。

我们要返回东西看起来比较多，那么可以考虑封装为一个模型，还能起到验证作用。

在schemas/favorite.py里面添加`FavoriteListResponse`类，

但这里的 `list` 数组元素是一个新闻对象，我们写一个专门表示收藏列表里每条新闻的类 `FavoriteNewsItemResponse`。这个类的字段很多，且有一部分和之前的新闻模块重复，所以**抽一个基类**来提高复用：

在 `schemas/base.py` 定义 `NewsItemBase`：

```python
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class NewsItemBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(None, alias="publishedTime")

    model_config = ConfigDict(
        from_attributes=True,   # 允许从 ORM 对象取值
        populate_by_name=True   # 同时支持字段名和别名
    )
```

然后在 `schemas/favorite.py` 里继承它：

```python
class FavoriteNewsItemResponse(NewsItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
```

`FavoriteNewsItemResponse` = 新闻基础字段 + `favorite_id` + `favorite_time`，刚好对应联表查询返回的三元组。

最后，修正路由函数里的顺序问题（先取数据，再构建列表）并传入 data：

```python
@router.get("/list")
async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    total, rows = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [
        {
            **news.__dict__,
            "favorite_time": favorite_time,
            "favorite_id": favorite_id
        } for news, favorite_time, favorite_id in rows
    ]
    has_more = total > page * page_size
    data = FavoriteListResponse(
        total=total,
        hasMore=has_more,
        list=favorite_list
    )
    return success_response(message="获取收藏列表成功", data=data)
```

**注意**：一定要 `total, rows = await ...` 写在列表推导式**之前**，不然变量未定义会报错。

最终补全路由函数：



```python
@router.get("/list")
async def get_favorite_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    rows, total =await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = [
        {
            **news.__dict__,
            "favorite_time": favorite_time,
            "favorite_id": favorite_id
        } for news, favorite_time, favorite_id in rows
    ]
    has_more = total > page * page_size
    data = FavoriteListResponse(
        total = total,
        hasMore = has_more,
        list = favorite_list
    )
    return success_response(message="获取收藏列表成功", data = data)
```



#### （5）清空收藏列表

大致思路：进入请求→验证用户是否登录→清空当前用户收藏新闻→响应结果

CRUD函数：

```python
#清空收藏列表：当前用户的所有收藏
async def remove_all_favorite(
        db: AsyncSession,
        user_id: int
):
    stmt=delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0 #有数量就返回数量，没有数量就返回0
```

`delete(Favorite).where(...)`：**先筛选再删除**，只清空当前用户的收藏，不会误删别人的数据。

`result.rowcount`：返回本次操作**影响的行数**（即删了多少条）。如果收藏表为空，`rowcount` 可能返回 `None`，所以用 `or 0` 兜底，保证返回数字。

路由函数：

```python
@router.delete("/clear")
async def clear_favorite(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    count = await favorite.remove_all_favorite(db, user.id)
    return success_response(message=f"清空了{count}条收藏记录")
```

这里不用传任何参数，**只依赖登录用户**，根据 Token 拿到 `user.id` 就能定位到该用户的所有收藏。返回消息里用 f-string 把删除条数带出来，方便前端展示。



### 8、浏览记录模块

#### （1）添加浏览历史

大致思路：进入请求→验证用户是否登录→创建浏览记录→响应结果

先写ORM模型类，在models文件夹里创建history.py：

```python
from datetime import datetime
from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.news import News
from models.users import User


class Base(DeclarativeBase):
    pass


class History(Base):
    """
    浏览记录表ORM模型
    """
    __tablename__ = 'history'

    # 创建索引
    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="浏览记录ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, comment="浏览时间")

    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, view_time={self.view_time})>"
```

浏览记录表有三个外键字段：`user_id` 关联用户表，`news_id` 关联新闻表，`view_time` 记录浏览时间。和收藏表不同，浏览记录表**没有设置唯一约束**，因为同一用户可能多次浏览同一篇新闻，每次都会产生一条新记录。

接着写Pydantic请求模型，在schemas/history.py中定义：

```python
from pydantic import BaseModel, Field

class HistoryAddRequest(BaseModel):
    """
    添加浏览记录的请求模型
    用于接收前端传来的新闻ID
    """
    news_id: int = Field(..., alias="newsId")  # 新闻ID，必填字段，使用驼峰命名别名
```

然后编写CRUD函数，在crud/history.py中定义`add_news_history()`：

```python
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_news_history(db: AsyncSession,
                           user_id: int,
                           news_id: int
):
    """添加浏览记录"""
    history_record = History(user_id=user_id, news_id=news_id)
    db.add(history_record)
    await db.commit()
    await db.refresh(history_record)
    return history_record
```

这里逻辑比较直接：创建ORM对象 → `db.add()` 注册到会话 → `commit()` 写入数据库 → `refresh()` 获取数据库自增ID等字段 → 返回记录对象。

最后编写路由函数，在routers/history.py中调用：

```python
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_database
from crud import history
from models.users import User
from schemas.history import HistoryAddRequest
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
        data: HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    result = await history.add_news_history(db, user.id, data.news_id)
    return success_response(message="添加浏览记录成功", data=result)
```

**重点**：浏览记录和收藏记录的差异——收藏表用 `UniqueConstraint` 约束同一用户+同一新闻只能有一条记录；而浏览记录**不加唯一约束**，用户每次浏览都会新增一条记录，这样可以保留用户完整的浏览轨迹。


#### （2）获取浏览历史

大致思路：进入请求→验证用户是否登录→联表查询（History + News）→分页+按浏览时间降序→返回总量、列表和是否有下一页

在crud/history.py中定义`get_history_list()`：

```python
async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    """获取浏览历史列表：获取某个用户的浏览历史 + 分页功能"""
    # 总量统计
    count_query = select(func.count()).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size

    # 获取浏览历史列表 - 从 History 表开始查询，JOIN News 表获取新闻详情
    query = (select(News,
                    History.view_time.label("view_time"),
                    History.id.label("history_id"))
             .select_from(History)
             .join(News, History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset(offset)
             .limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()

    return total, rows
```

**重点**：这里的联表查询和收藏列表有所不同：

- `.select_from(History)`：**显式指定以 History 表作为查询起点**（驱动表），然后 JOIN News 表。这与收藏列表的写法（`select(News).join(Favorite)`）等价，但 `select_from` 更明确地表达"以谁为主"。
- `History.view_time.label("view_time")`：给浏览时间起别名，避免和 News 表里的时间字段冲突。
- `History.id.label("history_id")`：给浏览记录ID起别名，因为 News 也有 id 字段。这个 `history_id` 会在删除单条记录时用到。
- `order_by(History.view_time.desc())`：按浏览时间**降序**排列，最近浏览的排在最前面。

然后编写响应模型。浏览历史的列表项需要新闻基本信息 + 浏览记录特有字段，这里直接复用 `schemas/base.py` 中的 `NewsItemBase`：

```python
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from schemas.base import NewsItemBase


class HistoryNewsItemResponse(NewsItemBase):
    """
    浏览历史项响应模型
    继承自 NewsItemBase，包含新闻基本信息 + 浏览记录特有字段
    """
    history_id: int = Field(alias="historyId")  # 浏览记录ID
    view_time: datetime = Field(alias="viewTime")  # 浏览时间

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )


class HistoryListResponse(BaseModel):
    """
    浏览历史列表响应模型
    """
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
```

最后在路由函数中调用，将联表查询返回的三元组 `(news, view_time, history_id)` 通过列表推导式转成字典格式：

```python
@router.get("/list")
async def get_history_list(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    total, rows = await history.get_history_list(db, user.id, page, page_size)
    history_list = [
        {
            "id": news.id,
            "title": news.title,
            "description": news.description,
            "image": news.image,
            "author": news.author,
            "categoryId": news.category_id,
            "views": news.views,
            "publishedTime": news.publish_time,
            "viewTime": view_time,
            "historyId": history_id
        } for news, view_time, history_id in rows
    ]
    has_more = total > page * page_size
    data = HistoryListResponse(
        total=total,
        hasMore=has_more,
        list=history_list
    )
    return success_response(message="获取浏览历史成功", data=data)
```

这里 `rows` 的每个元素是三元组 `(News对象, view_time, history_id)`，列表推导式遍历三元组，把每个 News 对象的属性一一映射到字典里，再加上浏览时间 `viewTime` 和浏览记录 ID `historyId`，最终以 `HistoryListResponse` 格式返回。


#### （3）删除单条浏览历史

大致思路：进入请求→验证用户是否登录→根据用户ID和新闻ID删除对应记录→检查是否命中→响应结果

在crud/history.py中定义`remove_history()`：

```python
async def remove_history(db: AsyncSession,
                         user_id: int,
                         news_id: int
):
    """删除单条浏览记录"""
    stmt = delete(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
```

这里使用 `delete(History).where(...)` 直接删除符合条件的记录。两个条件用逗号分隔（AND 逻辑），确保只删除**当前用户**的**指定新闻**浏览记录。

返回值 `result.rowcount > 0` 表示是否真的有记录被删除。如果用户没有浏览过该新闻，`rowcount` 为 0，返回 `False`。

路由函数：

```python
@router.delete("/remove")
async def remove_history(
        news_id: int = Query(..., alias="newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    result = await history.remove_history(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览记录不存在")
    return success_response(message="删除浏览记录成功", data=result)
```

这里 `news_id` 是查询参数（`Query`），从 URL `?newsId=xxx` 传入。如果删除失败（记录不存在），抛出 404 异常。


#### （4）清空浏览历史

大致思路：进入请求→验证用户是否登录→删除当前用户的所有浏览记录→返回删除条数→响应结果

在crud/history.py中定义`remove_all_history()`：

```python
async def remove_all_history(
        db: AsyncSession,
        user_id: int
):
    """清空浏览历史"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
```

`delete(History).where(...)`：**先筛选再删除**，只清空当前用户的记录，不会误删别人的浏览历史。

`result.rowcount or 0`：返回本次操作影响的行数。如果该用户没有任何浏览记录，`rowcount` 可能为 `None`，用 `or 0` 兜底，保证返回数字 0。

路由函数：

```python
@router.delete("/clear")
async def clear_history(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_database)
):
    count = await history.remove_all_history(db, user.id)
    return success_response(message=f"清空了{count}条浏览记录")
```

这里和清空收藏列表思路一致——不需要任何前端参数，只依赖 Token 拿到的 `user.id` 就能定位到该用户的所有记录。返回消息用 f-string 把删除条数带出来，方便前端展示提示信息。

**清空浏览历史 vs 删除单条浏览历史对比**：

| 对比维度 | 删除单条 | 清空全部 |
| -------- | -------- | -------- |
| 方法 | `@router.delete("/remove")` | `@router.delete("/clear")` |
| 是否需要参数 | 需要 `newsId` 查询参数 | 不需要，只依赖登录用户 |
| WHERE 条件 | `user_id + news_id` | 仅 `user_id` |
| 未找到时的处理 | 抛 404 异常 | 返回 count = 0（不报错） |





### 9、缓存模块

#### （1）缓存简介及安装Redis服务端

**数据缓存**：缓存是一种存储机制，用于临时存储数据或计算结果，当再次需要这些数据时，可以快速从缓存中检索，而不是重新进行耗时或昂贵的获取和计算过程。

在网站开发中，缓存（Cache）是一个非常重要的概念，其核心作用是提高性能、降低延迟和减轻服务器负载。

主要优势：提升性能和用户体验；减轻服务器/数据库负载；降低网络延迟；节省资源和成本。

**Redis**：Redis是一种高性能的Key-Value存储系统，它将数据存储在内存中，因此读写速度极快，非常适合作为应用层的缓存服务。

在FastAPI这样的额后端框架中，通常在应用层使用像Redis这样的内存数据存储作为缓存。

安装自己上网找教程。

#### （2）配置Redis客户端

首先安装 Redis 的 Python 异步客户端：

```bash
pip install redis
```

然后在 config 文件夹下创建 `cache_conf.py`，配置 Redis 连接：

```python
import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
#创建 Redis 的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,#Redis 服务器的主机名或 IP 地址
    port=REDIS_PORT,#Redis 服务器的端口号
    db=REDIS_DB,#Redis 数据库的索引

    decode_responses=True#告诉 Redis 返回的字符串结果，而不是字节结果
)
```

**参数说明**：

| 参数               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| `host`             | Redis 服务器地址，本地用 `localhost`                         |
| `port`             | Redis 端口号，默认 `6379`                                    |
| `db`               | Redis 数据库编号（0-15），默认 `0`                           |
| `decode_responses` | **设为 True** → 返回的数据自动转成 Python 字符串，否则返回 bytes（字节） |

**重点**：`import redis.asyncio as redis`

- 这里是**异步版本**的 Redis 客户端，FastAPI 是异步框架，必须用异步 Redis，否则会阻塞整个事件循环。
- 同步版本是 `import redis`，异步版本是 `import redis.asyncio`。

**decode_responses 的作用**：

如果不设置 `decode_responses=True`，从 Redis 取出来的数据都是 `b"xxx"` 这种 bytes 格式，每次都要手动 `.decode()`，很麻烦。设为 True 之后直接拿到字符串，省事。



#### （3）封装缓存操作方法

**封装缓存操作**：缓存操作就是围绕Redis做”存、取、删、判断、过期”等操作，让数据访问更快、数据库压力更小。

Redis存储数据：key - value

|  方法  |                   参数                   |                 描述                 |
| :----: | :--------------------------------------: | :----------------------------------: |
| setex  | key: str, expire:int（秒）, value(): str |        设置缓存并指定过期时间        |
|  get   |                 key: str                 | 获取缓存值。若缓存值不存在，返回None |
| delete |                 key: str                 |           删除指定的缓存键           |
| exists |                 key: str                 |    检查缓存键是否存在，返回布尔值    |

但在实际项目中，**不能每次都裸写 Redis 命令**。我们需要在 `config/cache_conf.py` 中对这些基础操作进行封装，好处有三点：

1. **统一错误处理**：Redis 连接可能断、数据可能损坏，封装后在函数内部统一 try/except，调用方不需要每次都写异常处理。
2. **屏蔽数据类型差异**：Redis 只存字符串，但我们经常要存字典/列表。封装后调用方只需传 Python 对象，序列化/反序列化都在函数内部自动处理。
3. **代码复用**：所有模块共用一套缓存函数，修改时只改一处。

---

首先，在文件顶部导入必要的包：

```python
import json
from typing import Any

import redis.asyncio as redis
```

**`json`**：用来将 Python 字典/列表 与 JSON 字符串互相转换（序列化 & 反序列化）。

**`typing.Any`**：Any 类型的参数/返回值不做类型检查，适合像 value 这种可能是字符串、也可能是字典或列表的场景。

---

**① 读取缓存 — 字符串：`get_cache()`**

```python
#读取：字符串
async def get_cache(key: str):
    try:#有可能获取不到
        return await redis_client.get(key)
    except Exception as e:
        print(f”获取缓存失败:{e}”)
        return None
```

**逐行解析**：

- `async def`：因为用的是异步 Redis 客户端，函数必须是异步的，否则 `await` 不生效。
- `key: str`：指定参数类型为字符串，Redis 的 key 都是字符串。
- `try...except`：因为网络波动、Redis 宕机等原因可能取不到数据，用 try 包裹，避免整个请求崩溃。
- `await redis_client.get(key)`：调用 Redis 的 GET 命令，异步等待结果返回。
- `except Exception as e`：捕获所有异常，打印错误信息，返回 `None`。**注意**：这里的 Exception 捕获范围较大，正式项目建议细化异常类型（如 `redis.ConnectionError`）。
- 返回值：成功返回缓存值（字符串），失败返回 `None`。

**使用场景**：适合存储简单的字符串数据，比如 Token、验证码、配置项等。

---

**② 读取缓存 — 字典/列表：`get_json_cache()`**

```python
#读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f”获取缓存失败:{e}”)
        return None
```

**逐行解析**：

- `data = await redis_client.get(key)`：先从 Redis 取出数据。此时 data 是**字符串**类型（因为设置了 `decode_responses=True`）。
- `if data:`：如果 key 不存在，Redis 返回 `None`，直接 pass 掉，返回 `None`。
- `return json.loads(data)`：**核心步骤**——将 JSON 字符串反序列化为 Python 对象（字典或列表）。
- `return None`：如果 data 为空（key 不存在），直接返回 None。

**`json.loads()` vs `json.dumps()`**：

| 函数          | 方向                  | 示例                                               |
| ------------- | --------------------- | -------------------------------------------------- |
| `json.loads`  | **字符串 → Python对象** | `'{“name”:”张三”}'` → `{“name”:”张三”}`            |
| `json.dumps`  | **Python对象 → 字符串** | `{“name”:”张三”}` → `'{“name”:”张三”}'`            |

**使用场景**：适合存储有结构的数据，比如新闻列表（list）、用户信息（dict）等。从缓存取出来后直接就能用 Python 对象操作。

---

**③ 设置缓存：`set_cache()`**

```python
#设置缓存 setex(key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value,(dict, list)):#如果是字典或列表
            #转字符串再存储
            value = json.dumps(value, ensure_ascii=False)#不转码，存储中文
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f”设置缓存失败:{e}”)
        return False
```

**逐行解析**：

- `value: Any`：value 可以是任意类型——字符串、数字、字典、列表等等。Any 表示不做类型限制。
- `expire: int = 3600`：过期时间，单位**秒**，默认 3600 秒（1 小时）。过期后 Redis 自动删除该 key，防止内存被撑满。
- `isinstance(value, (dict, list))`：**判断 value 是不是字典或列表**。如果是，就需要先转成 JSON 字符串再存，因为 Redis 只认字符串。
- `json.dumps(value, ensure_ascii=False)`：
  - `json.dumps()`：将 Python 对象转为 JSON 字符串。
  - `ensure_ascii=False`：**关键参数**！默认为 True，会把中文转成 `\uxxxx` 这种 Unicode 转义序列（比如 `”张三”` → `”张三”`）。设为 False 后直接存储原始中文，可读性好、也方便调试时直接在 Redis 里查看。
- `await redis_client.setex(key, expire, value)`：调用 Redis 的 SETEX 命令，**一次性完成”设值 + 设过期时间”**。等价于先 SET 再 EXPIRE，但 SETEX 是原子操作，更安全。
- 返回值：成功返回 `True`，失败返回 `False`。布尔类型的返回值方便调用方判断操作是否成功。

**重点：为什么要用 `isinstance` 做类型判断？**

因为 Redis 的 `setex` 要求 value 必须是字符串。如果你传一个 `{“name”: “张三”}` 这种字典进去，Redis 会直接报错。所以我们在函数内部自动判断：如果发现是字典/列表，先用 `json.dumps` 转成字符串再存，调用方完全不用关心这个细节。

**`ensure_ascii=False` 对比**：

```python
# ensure_ascii=True（默认）
json.dumps({“name”: “张三”})  # → '{“name”: “\\u5f20\\u4e09”}'

# ensure_ascii=False
json.dumps({“name”: “张三”}, ensure_ascii=False)  # → '{“name”: “张三”}'
```

---

**④ 三个函数的协作流程**

用一个典型场景串联三个函数 —— 获取新闻列表时，先查缓存，缓存没有再查数据库：

```python
# 1. 先从缓存拿
cached_data = await get_json_cache(“news_list:tech:page1”)
if cached_data:
    return cached_data  # 缓存命中，直接返回，不走数据库

# 2. 缓存没命中，查数据库
news_from_db = await query_database(...)

# 3. 把查到的数据写进缓存（下次就能命中）
await set_cache(“news_list:tech:page1”, news_from_db, expire=600)

return news_from_db
```

**流程图**：

```
前端请求
   ↓
查缓存（get_json_cache）
   ↓ 命中 → 直接返回（快！）
   ↓ 未命中
查数据库（慢）
   ↓
写缓存（set_cache，下次就快了）
   ↓
返回数据给前端
```

这就是经典的 **Cache-Aside 模式**（旁路缓存），也是后端开发中最常用的缓存策略。

---

**⑤ 缓存的 Key 命名规范**

从上面的例子可以注意到 key 写成 `”news_list:tech:page1”`，而不是简单的 `”news”`。良好的 key 命名规范可以避免 Key 冲突、方便管理和调试：

| 命名规则     | 示例                           | 说明                       |
| ------------ | ------------------------------ | -------------------------- |
| 用冒号分层   | `news:list:1:10`               | 类似目录结构，Redis 可视化工具会按层级展示 |
| 包含业务模块 | `user:token:13`                | 一眼看出是哪个模块的数据   |
| 包含关键参数 | `news:detail:5`                | 避免不同参数的缓存互相覆盖 |
| 避免过长     | 不建议超过 100 字符            | 太长浪费内存，可读性也差   |

---

**⑥ 异常处理的重要性**

三个函数都包裹了 `try/except`，因为 Redis 是**外部服务**，随时可能出现：

- 网络闪断
- Redis 进程挂了
- 内存满了写不进去
- 连接池耗尽

如果不对这些异常做兜底，**一次 Redis 故障就会导致整个接口 500 报错**。封装后，即使 Redis 挂了，也只是拿不到缓存数据，业务逻辑可以降级走数据库查询，不会影响核心功能。这就是所谓的**降级容错**——外部依赖出问题时，系统依然能正常运行。





#### （4）设计缓存策略

旁路缓存策略（Cache-Aside）是一种常见的缓存策略。其核心概念是应用程序主动管理缓存，**在读取数据时先检查缓存**。如果缓存中没有命中，则从数据库或其他数据源加载数据，并将数据存入缓存；当**数据更新或删除时，应用程序也负责更新或删除缓存中的数据**。

今天以"获取新闻分类"接口为例，走通"查缓存 → 未命中 → 查数据库 → 写缓存 → 返回"的完整链路。

---

**为什么需要单独抽一层缓存文件**

直接在路由函数里调用 `get_json_cache` / `set_cache` 也能跑，但有几个问题：路由会变臃肿；每个接口都要重复写"先查缓存再查库"的逻辑；Key 散落在各处容易写错。所以采用分层：

```
cache/news_cache.py      →  管理缓存 Key 和读写（缓存层）
crud/news_cache.py       →  业务逻辑 + 缓存策略判断（CRUD 层）
routers/news.py          →  接收请求、调用 CRUD、返回响应（路由层）
```

---

**缓存层 — `cache/news_cache.py`**

这一层只做 Key 常量化 + 包装读写。过期时间参考：分类 7200s / 列表 600s / 详情 1800s / 验证码 120s，数据越稳定越持久。

```python
from typing import List, Dict, Any
from config.cache_conf import set_cache, get_json_cache

CATEGORIES_KEY = "news:categories"

async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)

async def set_cached_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)
```

---

**CRUD 层 — `crud/news_cache.py`（Cache-Aside 核心）**

```python
from fastapi.encoders import jsonable_encoder
from cache.news_cache import get_cached_categories, set_cached_categories

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    # 1. 先查缓存
    cached = await get_cached_categories()
    if cached:
        print(f"✅ 命中缓存")
        return cached

    print("❌ 缓存未命中，查询数据库...")

    # 2. 查数据库
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    # 3. 写缓存（注意：空数据不写入，防止缓存穿透）
    if categories:
        categories_encoded = jsonable_encoder(categories)
        await set_cached_categories(categories_encoded)

    return categories
```

**流程**：查缓存 → 命中直接返回 → 未命中查数据库 → 有数据写缓存 → 返回。

两个重点：

`jsonable_encoder`：查出来的 `categories` 是 ORM 对象列表，不能直接 JSON 序列化存 Redis。`jsonable_encoder` 是 FastAPI 内置函数，把 ORM 对象递归转成 JSON 兼容的字典列表，之后 `json.dumps` 才能正常处理。

空数据不写缓存：如果数据库返回空列表 `[]` 也写进 Redis，下次请求缓存命中直接返回空，永远查不到后来新增的数据，这就是**缓存穿透**。所以只有确实查到数据才写缓存。

路由层只需把调用从 `news.get_categories` 改成 `news_cache.get_categories` 即可，其他不变。

---

**RESP3 协议踩坑 — `protocol = 2`**

今天配置 Redis 客户端时遇到了一个坑。`redis-py` 5.0 以上版本默认使用 RESP3 协议（`protocol=3`），但 RESP3 的响应格式和 RESP2 不同，会导致 `setex` 等方法返回的结果类型发生变化，代码直接报错无法运行。当时报的错误跟返回值解析有关，查了半天才发现是协议版本的问题。

解决方式：在 `redis.Redis()` 连接参数里显式指定 `protocol = 2`，强制使用 RESP2：

```python
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    protocol=2   # 强制 RESP2，解决 RESP3 兼容问题
)
```

RESP2 vs RESP3：

| 协议 | 特点 |
| ---- | ---- |
| RESP2（`protocol=2`） | 经典协议，所有版本都兼容，稳定可靠 |
| RESP3（`protocol=3`） | redis-py 5.0+ 默认，返回格式有变化，部分场景不兼容 |

**总结**：当前环境（redis-py 5.x）下，配上 `protocol=2` 才能正常运行。以后如果 redis-py 新版对 RESP3 的支持更完善了，可以再去掉这行。



#### （5）缓存新闻列表

这一节是缓存实战的进阶内容。和上一节"分类缓存"不同，新闻列表的缓存涉及**分页参数**、**更复杂的数据类型转换**、以及**列表推导式**的大量使用，第一次接触会非常绕。

---

**① 新闻列表缓存的 Key 设计**

新闻列表比分类缓存多了一个关键问题：**同一分类、不同页码、不同页面大小，是不同的数据**。所以 Key 必须包含这些参数：

```python
NEWS_LIST_PREFIX = "news:list:"

# Key 格式：news:list:{分类ID}:{页码}:{每页数量}
# 示例：
#   news:list:1:1:10   → 分类1，第1页，每页10条
#   news:list:all:2:20 → 全部分类，第2页，每页20条

async def set_cached_news_list(category_id, page, size, news_list, expire=600):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)
```

注意：参数里传入的是 `page`（页码），而不是 `skip`（跳过条数）。因为缓存 Key 应该用业务语义（第几页），而不是计算后的偏移量。在 CRUD 层做了转换：`page = skip // limit + 1`。

---

**② 本节最绕的部分：新闻列表写入缓存的数据类型全链路**

这是今天最难理解的地方。数据从数据库查出来到最终存进 Redis，经历了多次"变形"。核心代码在 `crud/news_cache.py` 第 97 行：

```python
news_data = [NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False) for item in news_list]
```

拆解这个列表推导式，每一步都在做类型转换：

```python
# 假设 news_list 是数据库查出来的 ORM 对象列表
# news_list = [<News id=1 title='xxx'>, <News id=2 title='yyy'>, ...]

news_data = []  # 最终要写入 Redis 的字典列表

for item in news_list:
    # item 是 SQLAlchemy ORM 对象，比如 <News id=1 title='xxx' category_id=2>

    # 第 1 步：ORM → Pydantic 模型
    # NewsItemBase.model_validate(item) 把 ORM 对象转成 Pydantic 对象
    # 为什么能转？因为 NewsItemBase 配置了 from_attributes=True，
    # 它可以直接从 ORM 对象的属性里读取值
    pydantic_obj = NewsItemBase.model_validate(item)
    # → NewsItemBase(id=1, title='xxx', category_id=2, publish_time=datetime(...))

    # 第 2 步：Pydantic 模型 → 字典
    # .model_dump(mode="json", by_alias=False) 把 Pydantic 对象转成普通字典
    # mode="json"  : 把 datetime 等特殊类型转成 JSON 兼容格式（ISO 8601 字符串）
    #                比如 datetime(2024,1,1) → "2024-01-01T00:00:00"
    # by_alias=False: 用 Python 风格字段名（category_id），不用前端风格（categoryId）
    dict_item = pydantic_obj.model_dump(mode="json", by_alias=False)
    # → {"id": 1, "title": "xxx", "category_id": 2, "publish_time": "2024-01-01T00:00:00", ...}

    news_data.append(dict_item)

# news_data = [
#     {"id": 1, "title": "xxx", "category_id": 2, "publish_time": "2024-01-01T00:00:00", ...},
#     {"id": 2, "title": "yyy", "category_id": 2, "publish_time": "2024-01-02T00:00:00", ...},
# ]
```

然后 `news_data` 被传给 `set_cached_news_list()` → `set_cache()` → `json.dumps()` 变成 JSON 字符串 → `redis_client.setex()` 写入 Redis。

---

**③ 为什么新闻列表不用 `jsonable_encoder`，而用 Pydantic 的 `model_validate + model_dump`？**

上一节分类缓存用的是 FastAPI 内置的 `jsonable_encoder(categories)`，一句话就搞定了。但新闻列表用了更复杂的 Pydantic 方式，原因是对比：

| 对比维度 | `jsonable_encoder` | `model_validate + model_dump` |
|---------|-------------------|------------------------------|
| 来源 | FastAPI 内置 | Pydantic |
| 字段控制 | 所有字段都转，无法筛选 | 只转 Schema 里定义的字段（精准控制） |
| 类型转换 | 自动处理 | `mode="json"` 精确控制（如 datetime → ISO 字符串） |
| 别名控制 | 不支持 | `by_alias` 精确控制字段名风格 |
| 适用场景 | 简单场景，字段少 | 复杂场景，需要字段筛选和精确类型控制 |

新闻列表用 Pydantic 方式的好处：ORM 模型里有很多字段（`created_at`、`updated_at`、`content` 全文等），但缓存只需要 Schema 定义的几个核心字段，不会把冗余数据存进 Redis，节省内存。

---

**④ 新闻列表读取缓存（写入的逆过程）**

```python
# crud/news_cache.py
page = skip // limit + 1                           # offset → 页码
cached_list = await get_cache_news_list(category_id, page, limit)
if cached_list:
    return cached_list  # 直接返回字典列表，FastAPI 也能处理
```

读取链路：Redis → `redis_client.get()` → JSON 字符串 → `json.loads()` → Python 字典列表 → 直接返回。

**关键理解**：缓存读出来的数据是**字典列表** `[{"id": 1, ...}, ...]`，不是 ORM 对象。但因为 FastAPI 返回响应时会自动序列化字典为 JSON，所以不需要再转回 ORM 对象。这就是为什么 `return cached_list` 可以直接用。

---

**⑤ 数据全链路总结（写入 + 读取一张图）**

```
【写入缓存】                              【读取缓存】
数据库 ORM 对象                            Redis
    │                                        │
    │ model_validate()                  redis_client.get()
    ↓                                        ↓
Pydantic 模型                            JSON 字符串
    │                                        │
    │ model_dump(mode="json")            json.loads()
    ↓                                        ↓
Python 字典列表                           Python 字典列表
    │                                        │
    │ json.dumps()                        直接 return
    ↓                                        ↓
JSON 字符串                              FastAPI 响应给前端
    │
    │ redis_client.setex()
    ↓
  Redis
```

记住这四步口诀：
- **写入**：ORM → Pydantic → 字典 → JSON 字符串 → Redis
- **读取**：Redis → JSON 字符串 → 字典 → 直接返回

---

**⑥ 列表推导式的阅读技巧**

今天代码里出现了大量列表推导式，比如 `get_related_news` 里的这个：

```python
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

阅读技巧：**先看 `for` 后面，再看 `for` 前面**。

1. `for news_detail in related_news` → 遍历 ORM 对象列表，每个元素叫 `news_detail`
2. `{ "id": news_detail.id, ... }` → 对每个元素，提取属性变成一个新字典

等价于传统写法：

```python
result = []
for news_detail in related_news:
    result.append({
        "id": news_detail.id,
        "title": news_detail.title,
        # ...
    })
return result
```

更复杂的如第 97 行的嵌套调用 `NewsItemBase.model_validate(item).model_dump(...)`，拆解方法一样：**从内到外、从左到右**，一步步拆开就清晰了。

---

**⑦ 本节涉及的缓存过期时间参考**

| 数据类型 | 过期时间 | 原因 |
|---------|---------|------|
| 新闻分类 | 7200s（2小时） | 分类几乎不变，可以缓存很久 |
| 新闻列表 | 600s（10分钟） | 新文章会发布，需要相对及时更新 |
| 新闻详情 | 1800s（30分钟） | 浏览量会变，但不需要实时 |
| 验证码 | 120s（2分钟） | 安全敏感，必须短 |

原则：**数据越稳定，缓存越持久**。同时要避免所有 Key 设置相同的过期时间，防止同一时刻大量缓存同时失效（缓存雪崩）。

