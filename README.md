# 大学生失物招领&社区分享平台

服务开发技术实验，不到一周时间手搓的FastAPI+VUE小网站

## 目录

1. 项目介绍
2. 资源设计
3. 关键功能实现
4. 总结与体会

## 项目介绍

### 项目背景

当前大学生群体在校园内丢失物品的情况较为普遍，传统的失物招领方式（如QQ群、人工询问）效率低下，信息传递不及时，导致失物难以寻回，给学生生活带来诸多不便。现有的校园论坛、社交媒体等平台信息分散，缺乏针对性和专业性，难以满足大学生对失物招领和社区交流的特定需求。

### 项目目标

构建一个高效、便捷的失物招领平台，同时提供一个活跃的校园社区交流空间，通过信息化的手段，实现失物信息的快速发布、精准匹配和及时反馈，提高失物寻回率，减少学生损失。优化校园服务，提升校园信息化水平，为学生提供更优质的学习和生活体验。

### 项目功能

#### 用户模块

- 登录/注册：用户可以通过注册账号并登录系统，进行个人信息的管理和使用其他功能。
- 个人信息管理：用户可以修改个人信息，如用户名、密码、联系方式等。

#### 失物招领模块

- 发布失物信息：用户可以发布捡到或丢失物品的信息，包括物品类型、丢失时间、地点、联系方式等。
- 浏览失物/招领信息：用户可以浏览所有失物和招领信息列表。
- 查看失物/招领详细信息：用户可以点击感兴趣的失物和招领信息，查看失物招领的详细信息，包括地点地图查看等，并且能查看同类别的相关失物/招领推荐。
- 设置物品状态：用户可以为自己发布的物品设置状态，如已找到/未找到。

#### 社区博客模块

- 发布博客：用户可以发布自己的博客，分享校园生活、学习心得等，支持图片上传。
- 浏览博客：用户可以浏览其他用户发布的博客列表。
- 点赞/评论博客：用户可以对感兴趣的博客进行点赞和评论互动，也可以对评论进行回复和点赞。

### 系统架构

技术栈：

- 前端：Vue.js
- 后端：FastAPI框架
- 数据库：MySQL
- 工具：Pydantic 数据建模，Postman 测试接口

系统架构：B/S架构，前后端分离

**为什么选择fastAPI？**
1. 天然支持RESTful风格（面向资源）
FastAPI 的核心就是围绕 HTTP 方法（GET、POST、PUT、DELETE）对“资源 URI”的操作来构建的
2. 自动生成 OpenAPI 文档
FastAPI 内置支持自动生成：
- Swagger UI（交互式 API 文档）
- ReDoc（结构化 API 文档）
- OpenAPI JSON schema

## 资源设计

### 资源定义

|资源名称|描述|
|---|---|
|User|平台用户，含身份信息和行为记录|
|LostItem|失物/招领物品的详细信息|
|BlogPost|社区分享内容，含标题/正文/图片等|
|Comment|附属于博客或物品的评论|
|Like|点赞操作，用户对博客/评论的支持|
|Image|图片资源，可附属于LostItem或BlogPost|

数据来源：用户发布与操作、地图资源（用于失物招领地点定位）

### 数据结构设计

#### LostItem

- uuid id
- enum type
- string title
- enum category
- string description
- string location
- datetime time
- enum contact_type
- string contact_value
- bool hide_contact
- enum status
- datetime created_at
- datetime updated_at
- int views_count

#### BlogPost

- uuid id
- string title
- enum category
- string summary
- string content
- bool allow_comments
- bool featured
- enum status
- list<string> tags
- datetime created_at
- datetime updated_at
- datetime published_at
- int views_count
- int likes_count
- int comments_count

#### User

- uuid id
- string email
- string hashed_password
- string username
- string avatar
- string dept

### 设计资源URI

设计资源URI的原则：

（1）资源路径统一采用名词

比如/api/users, /api/lost-items, /api/blog-posts，以资源集合名命名，符合 RESTful 命名习惯。

（2）操作用 HTTP 方法表达而不是路径动词

使用 GET, POST, PUT, DELETE来表示不同操作，而不是在路径中用register、get等动词。

（3）通过子路径表达资源层级关系

如 /api/blog-posts/{id}/comments 表示某个blog的评论，符合层级结构。

### 设计资源表述

使用JSON格式进行表述

```json
{
"type": "lost",
"title":"找到一部手机",
"category":"books",
"description":"今天在去食堂的路上捡到一部华为pura70pro手机",
"location":"软件园校区食堂主干道",
"time":"2025-06-02T10:55:00",
"contact_type": "phone",
"contact_value":"18596171369",
"hide_contact": false,
"id":"2cfff9e0-29a1-4bbb-9367-c8b6c86d3735",
"owner_id":"384e528d-e853-4311-9840-824ac4fa06b2",
"owner_username": "Ronronner",
"owner_avatar": "hello",
"status": "unclaimed",
"created_at":"2025-06-02T11:02:59",
"updated_at":"2025-06-02T11:02:59",
"views_count": 20,
"images":[
"http://localhost:8000/static/lost-items/2cff9e0-29a1-4bbb-9367-c8b6c86d3735/cec6f4
]
}
```

```json
{
"access_token": "eyJhbGci0iJIUzI1NiIsInR5cCI6IkpXVC
"token_type": "bearer",
"user_id": "384e528d-e853-4311-9840-824ac4fa06b2",
"username": "Ronronner",
"avatar": "hello"
}
```

```json
{
"title":"今天很开心",
"category":"life",
"summary":"今天真的真的好开心啊",
"content":"非常非常开心!!",
"allow_comments": true,
"featured": false,
"id": "c2aeeffd-9862-4fe0-8899-c0c884b06cf4",
"author_id": "384e528d-e853-4311-9840-824ac4fa06b2",
"author_name": "Ronronner",
"author_avatar": "hello",
"status":"draft",
"images":[],
"tags":[
"夜宵",
"自习"
],
"created_at":"2025-06-02T20:03:54",
"updated_at":"2025-06-02T20:03:54",
"views_count":0,
"likes_count":0,
" comments_count":0,
"liked": false,
"comments":[]
}
```

### 设计资源接口

以LostItem为例，使用FastAPI定义API接口

POST

```python
@router.post( path: "∠", response_model=LostItemPublic)
async def create_lost_item(
session: SessionDep,
current_user: CurrentUser,
type: ItemType = Form(...),
title: str = Form(...),
category: ItemCategory = Form(...),
description: str = Form(...),
Location: str = Form(...),
time: datetime = Form(...),
contact_type: ContactType = Form(...),
contact_value: str = Form(None),
hide_contact: bool = Form(False),
images: List[UploadFile]= File(None),
->Any:)
```

GET

PUT

```python
@router.put( path: "/{id}", response_model=LostItemPublic)
async def update_lost_item(
session: SessionDep,
current_user: CurrentUser,
id:uuid.UUID,
type: ItemType = Form(...),
title: str = Form(...),
category: ItemCategory = Form(...),)
```

DELETE

```python
@router.delete("/{id}")
def delete_lost_item(
session: SessionDep,
current_user: CurrentUser,
id: vuid.UUID,
) -> Message:)
```

### 设计资源服务的反馈

成功响应：返回状态码200 OK

错误响应：

- 请求数据格式错误：422 Unprocessable Content
- 未找到资源：404 Not Found
- 服务器内部错误：500 Internal Server Error
- 其他自定义的错误码：
    - 403 Forbidden：用户权限不足或未登录
    - 404 Not Found：数据未找到/用户不存在
    - 503 Service Unavailable：邮件发送失败
    - 400 Bad Request：其他各类错误

```python
@router.post("/emailCode")
async def verify_email_code (request: EmailValidateRequest):
if not EmailCodeService.validate_code(request.email, request.valid
raise HTTPException( status_code: 400, detail:"验证码错误或已过期")
return {"message":"验证成功"}
```

```python
except Exception as e:
Logger.error(f"邮件发送失败:{str(e)}")
raise HTTPException( status_code: 503, detail=str(e)))
```

让服务返回有意义的状态代码，并且令客户端懂得如何处理状态代码，给HTTP简单的请求响应机制增加了一层协调协议，提高了分布式系统的健壮性和可靠性

```javascript
} catch (error){
console.error('获取数据失败:',error)
posts.value =[]
if (error.response && error.response.status === 403) {
if(confirm('您的登录状态已过期,请先登录')){
router.push('/login')
})
```

当在此页面中返回403状态码时，意味着用户此时处于未登录状态。捕捉这一状态码并进行处理，弹出响应的提醒并将页面跳转至登录界面

## 关键功能实现

### 一、登录注册功能

身份验证和授权方法：JWT认证

```json
{
"access_token": "eyJhbGci0iJIUz I1NiIsInR5cCI6IkpXVCJ9.ey]]
"token_type":"bearer"
}
```

JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源

浏览器请求时在认证头中附加JWT Token

```
请求标头
原始
Accept
application/json, text/plain, */*
Accept-Encoding
gzip, deflate, br, zstd
Accept-Language
zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Authorization
Bearer
ey JhbGciOiJIUzI1NilsInR5cCl6lkpXVCJ9.ey JleHAiOjE3NDg5NTY4Mzg
sInN1Yil6ljM4NGU1MjhkLWU4NTMtNDMxMS05ODQwLTgyNGFjNG
ZhMDZiMiJ9.5JLh6IPiLucZDMRqGOhEICSGLrX_9DaQjxJCfRhlj7E
Connection
keep-alive
Cookie
Pycharm-111b08b2=7f131198-f6a7-4067-a4c3-6be9fc20be38;
SECKEY ABVK=GuL84m2 OsqRCdkBV7X1BsaZEYNTiy AW7Bv1Ut11yb
vE%3D; BMAP_SECKEY=7Tgy3ij6UGX712a-nmC8DmWe56SslYdg-
oDUPHKNxV8G9hzuh TaXW12x6VifJz8 Z88NH4O4xWyNC6sIbN
7wrreHjshx8a5N4eiy Z2hhuK8OvwAneUtEo1iGWoKnkktsAfh1JrSN8N
n5Z5glw8w2v-n55ng2mRFmqLoZXS5BVy_O4NeyRKt_ DVK3dO9xFJZ;
auth Token=eyJhbGciOiJIUzl1 NilsInR5cCl6lkpXVCJ9.eyJleHAiOjE3ND
g5NTY4MzgsinN1Yil6ljM4NGU1MjhkLWU4NTMtNDMxMS05ODQw
LTgyNGFjNGZhMDZiMiJ9.5JLh6IPiLucZDMRqGOhEICSGLrX_9DaQjxJC
fRhlj7E
localhost:4000
Host
```

认证流程：

1. POST/users/login 输入用户名和密码
2. 使用秘钥创建一个JWT
3. 返回JWT给浏览器
4. 在认证头中附加JWT
5. 检查JWT签名，从JWT获得用户信息
6. 返回响应给客户端

### 二、发布失物招领/博客功能

发布失物招领时，需要选择是失物还是招领，并填写描述，时间，地点，联系方式、上传照片等信息。

在选择地点时，有时用文字描述准确度较低，为了更加准确地对丢失物品进行定位，使用了百度地图的地图资源API，在填写信息的时候进行更加细致准确的定位，便于查找

```javascript
const script = document.createElement("script")
script.type = "text/javascript"
script.src ="http://api.map.baidu.com/api?v=2.0&ak=mK5CDIAi1mk8Le8
document.head. appendChild(script)
window.initBMap =()=>{
callback())
```

### 三、浏览失物招领/博客详情

在失物招领详情中显示地图中的位置

显示失物的各种信息以及当前状态

```
联系方式
联系方式:
微信
联系信息:
复制
weixinhao
标记为已认领/找到
删除信息
编辑信息
神思电子技术
股份有限公司
泰山财产保险
股份有限公司
伯乐路
山东大学
(软件园校区)
得安科技
三鼎电气
银丰科技公园
中国联合网络
通信有限公司
山东信息通信
簸箩顶
技术研究院
舜泰北路
菠萝山
科创金融公园
受春广场4品楼)
```

```
捡到一本书
算
机科
寻物启事
未认领/未找到
数据结构与算法 Python语言实现
数据结构与算法
发布时间:2025/06/03 20:39
浏览次数:0
Python语言实现
迈克尔·T.古德里奇(Michael T. Goodrich)
罗伯托·塔马西亚(Roberto Tamassia)
[美]
著
迈克尔·H.戈德瓦瑟(Michael H. Gollwaser)
张晓赵晓南等译
物品信息
Data Structures and Algorithms in Python
物品类型
丢失/拾取地点
Data Structures
& Algorithms
书籍资料
山东大学软件园校区食堂主干
道
丢失/拾取时间
当前状态
未认领/未找到
2025/06/03 20:34
in Python
机械工业出版社
详细描述
今天我在去食堂的路上看到一本写满笔记的黑色数据结构课本,
可能是哪个大二的学弟学妹遗失的。
```

### 三、博客点赞与评论

```
1喜欢
8评论
分享
评论(8)
写下你的评论...
nihao 2025-06-03 23:04
我也要去吃!!!!!
1回复
Ronronner 2025-06-03 23:45
你去吃的时候喊我一起!
€回复
Ronronner 2025-06-04 08:22
```

可以对博客进行点赞和评论，也可以对博客下的评论进行点赞和回复

对博客评论时，该方法的parent_id属性默认为None，而对评论进行回复时，前端会在传入参数中加入被回复的评论的id作为parent_id。

```python
@router.post( path: "/{id}/comments", response_model=CommentPublic)
def create_comment(
session: SessionDep,
current_user: CurrentUser,
id: uuid.UUID,
content: str = Form(...),
parent_id: Optional[uuid.UUID]=Form (None),
Any:)
```

## 总结与体会

本小组通过本次实验，不仅提升了后端接口设计能力，也加深了对 REST 架构、面向资源的服务设计以及接口设计的理解。

1. 以资源建模为基础，不要从“动作/功能”出发，而是要从系统中的“实体对象”出发进行建模

2. 以 HTTP 语义为表达方式，每个请求动作都应遵循 HTTP 协议所定义的语义，而不是自己随意创造请求方式。

3. 以标准化、可维护性为目标来设计服务接口，遵循统一的风格和规范，避免随意拼凑命名和结构，使得系统更容易理解、使用和维护。

感谢大家的观看

汇报人 : 王昕林
