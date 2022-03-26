# buffdvp_django

数据可视化平台BuffDVP后端源码

基于Django REST framework开发符合Restful规范的后端API

实现两套认证方式：

web端基于 `SessionAuthentication` + `csrf_token`

移动端基于 `JWTAuthentication`

模块说明：

`buff_data` : 数据中心api，将文件转化为标准化图表存储DB

`buff_echart` : 可视化api，使用pandas处理标准化图表，处理结果使用pyecharts生成可视化图表

`buff_file` : 文件管理api，实现文件上传、下载、查询等基本功能

`buff_user` : 用户管理api，实现用户登录、注册、查询、更新等基本功能，并拥有一套自定义的权限控制

推荐IDE：PyCharm

## 一、 开发环境部署

### 1 拉取项目

```shell
git clone xxx
```

### 2 创建虚拟环境

使用pycharm打开项目，File => Settings => Project => Python Interpreter => add => 创建虚拟环境

注意：Python 版本 >= 3.9

### 3 安装依赖

```shell
pip install -r requirements.txt
```

### 4 配置数据库

开发环境使用本地文件数据库 sqlite3 , pycharm 会自动生成，无需另外配置

需要使用远程 mysql 数据库可自行配置

```shell
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': '数据库账户',
        'PASSWORD': '数据库密码',
        'HOST': '数据库ip',
        'PORT': 3306,
    }
}
```

### 5 数据库迁移

sqlite 无需配置, mysql 需要创建数据库 your_db_name

```sql
CREATE DATABASE `your_db_name`;
```

teminal下执行命令生成数据表

```shell
python manage.py makemigrations
python manage.py migrate
```

### 6 运行开发环境

```shell
python manage.py runserver
# or
python manage.py runserver 0.0.0.0:8000
```
