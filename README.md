###背景
   随着py的asyncio库成熟，稳定，异步写法越来相对简单，高效稳定。
   目前此项目是基python_3.8.1＋开法，为什么基于此版本以上？一句话回答，我们是展望未来的，紧随技术的潮流。
   常作开发，离不开两大功能, web和api, 希望以starlette为框架，集成常见web，api功能模版，减少重复工作量

### 前端
bootstrap v4
bootstrap-table 1.15.5

### 后端
starlette


### 运行方式
1.nginx
2.uvicorn
3.uvloop

###功能 
#### WEB
  -[ ] 登陆
  -[ ] index
###安全性
- web安全
-[x] session, cookies HMAC的SALT以及利用cookies本身一些安全属性，如httponly, security等
   没有用官方的session, auth。两个原因，一是官方的(0.13.0)的sessio，认证权限，还没成熟。二是自已实现一遍，有更多的思考。
-[ ] CSRF
-[ ] XSS 
-[ ] api接口的安全
         
        
###效果
####login
![login](https://upload-images.jianshu.io/upload_images/1500770-fc8f343707c11010.png)
#### index
![index](https://upload-images.jianshu.io/upload_images/1500770-138d098cee96326b.png)
     
        
###未来



