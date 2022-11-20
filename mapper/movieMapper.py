import time

import pymysql
import config
from dao.User import User


def connectdb():
    # 打开数据库连接
    try:
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        db = pymysql.connect(host=config.MYSQL_DB_URL['host'], user=config.MYSQL_DB_URL['username'],
                             password=config.MYSQL_DB_URL['password'], database=config.MYSQL_DB_URL['database'])
    except Exception as e:
        print(e)
    return db


# 关闭数据连接
def closedb(db):
    db.close()


# 支持模糊查询
def select_User(id, username):
    # 使用cursor()方法获取操作游标
    print("开始查询")
    db = connectdb()
    cursor = db.cursor()
    username = "\'%" + username + "%\'"
    if id != "-1":
        sql = "SELECT * FROM user where id=" + id + " and username like " + username
    else:
        sql = "SELECT * FROM user where username like " + username
    list = []
    try:
        # 执行SQL语句
        print(sql)
        cursor.execute(sql)
        # 获取所有记录数量
        num1 = cursor.fetchall()
        list = []
        if len(num1) > 0:
            for row in num1:
                node = {'id': row[0], 'username': row[1], 'password': row[2], 'root': row[4], 'createtime': row[5],
                        'sex': row[3]}
                list.append(node)
        else:
            return list
    except:
        print("获取失败！")
    return list


# 登陆验证
def select_userisok(username, password):
    db = connectdb()
    username = "\"" + username + "\""
    password = "\"" + password + "\""
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "SELECT root FROM  user WHERE username=" + username + "and password=" + password
    res = {
        'root': 0,
        'code': 0
    }
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录数量
        num1 = cursor.fetchall()
        print("登陆成功")
        res = {
            'root': num1[0][0],
            'code': len(num1)
        }
        return res
    except:
        print("登陆失败")
    # 上报到管理平台
    closedb(db)
    return res


# 检验是否修改或添加
def select_user_have(username):
    db = connectdb()
    username = "\"" + username + "\""
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = "SELECT id FROM  user WHERE username=" + username
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录数量
        num1 = cursor.fetchall()
        if len(num1) > 0:
            res = {
                'id': num1[0][0],
            }
        else:
            res = {
                'id': 0,
            }
        return res
    except:
        print("数据库连接失败")
    # 上报到管理平台
    closedb(db)


"moviedb.userdb (password,username,root,createtime,sex)"


# 添加电影
def add_Movie(Movie):
    db = connectdb()
    title = "\"" + str(Movie.getuser_name()) + "\""
    douban = "\"" + Movie.getuser_password() + "\""
    uptime = "\"" + Movie.getuser_createtime() + "\""
    country = "\"" + str(Movie.getuser_root()) + "\""
    type = "\"" + str(Movie.getuser_sex()) + "\""
    time_total = "\"" + str(Movie.getuser_sex()) + "\""
    cursor = db.cursor()
    sql = "insert into moviedb (title,douban,uptime,country,type,time_total) " + "values (" + title + "," + \
          douban + "," + uptime + "," + country + "," + type + ","+time_total+")"
    num = cursor.execute(sql)
    print('添加成功')
    db.commit()  # 提交数据
    return num


# 用户信息修改
def update_info(user):
    db = connectdb()
    cursor = db.cursor()
    id = str(user.getuser_id())
    username = "\"" + str(user.getuser_name()) + "\""
    password = "\"" + user.getuser_password() + "\""
    createtime = "\"" + user.getuser_createtime() + "\""
    root = "\"" + str(user.getuser_root()) + "\""
    sex = "\"" + str(user.getuser_sex()) + "\""
    try:
        update = "update user set  username=" + username + ",password=" + password + ",createtime=" + createtime + \
                 ",root=" + root + ",sex=" + sex + " where id=" + id
        cursor.execute(update)
        print('信息修改成功')
        db.commit()  # 提交数据
    except:
        print('信息修改失败')
        db.rollback()
        cursor.close()
        db.close()


# 用户信息删除
def del_user(id):
    db = connectdb()
    cursor = db.cursor()
    try:
        update = "DELETE FROM user" + " where id=" + id
        cursor.execute(update)
        print("删除数据成功")
        db.commit()  # 提交数据
    except:
        db.rollback()
        cursor.close()
        db.close()


def add_type(data):
    db = connectdb()
    cursor = db.cursor()
    typename = "\"" + data + "\""
    # 执行SQL语句
    sql = "insert into movietype (typename) values (" + typename + ")"
    try:
        num = cursor.execute(sql)
        print('添加成功')
        db.commit()  # 提交数据
        return num
    except:
        print("数据库连接错误")
    db.rollback()
    cursor.close()
    db.close()
    return 0


if __name__ == '__main__':
    type_list = ['喜剧', '爱情', '剧情', '惊悚', '动作', '奇幻', '战争', '动画', '冒险']
    for k in type_list:
        add_type(k)
        time.sleep(3)