import easygui
import pymysql
from easygui import *


# 连接数据库
def connect_db():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="310324"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS data1")
    cursor.execute("USE data1")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS jobs (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, location VARCHAR(255), salary DECIMAL(10, 2), user_id INT)")
    return connection


# 注册用户
def register_user():
    username = enterbox("请输入用户名：")
    password = enterbox("请输入密码：", "注册")
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    connection.commit()
    cursor.close()
    connection.close()
    easygui.msgbox("注册成功！")


# 添加兼职工作
def add_job():
    title = enterbox("请输入兼职标题：")
    description = enterbox("请输入兼职描述：")
    location = enterbox("请输入兼职地点：")
    salary = enterbox("请输入兼职薪资：")
    user_id = enterbox("请输入用户ID：")
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO jobs (title, description, location, salary, user_id) VALUES (%s, %s, %s, %s, %s)",
                   (title, description, location, salary, user_id))
    connection.commit()
    cursor.close()
    connection.close()
    easygui.msgbox("添加兼职工作成功！")


# 查询兼职工作
def query_jobs():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    cursor.close()
    connection.close()
    return jobs


# 主函数
def main():
    while True:
        msg = "请选择操作："
        title = "兼职管理系统"
        choices = ["注册用户", "添加兼职工作", "查询兼职工作", "退出"]
        reply = choicebox(msg, title, choices)

        if reply == "注册用户":
            register_user()
        elif reply == "添加兼职工作":
            add_job()
        elif reply == "查询兼职工作":
            jobs = query_jobs()
            job_list = ""
            for job in jobs:
                job_list += f"{job[0]}. {job[1]} - {job[2]} - {job[3]} - {job[4]}"
            easygui.msgbox(f"查询结果：{job_list}")
        elif reply == "退出":
            break
        else:
            easygui.msgbox("无效的选择，请重新选择！")


if __name__ == "__main__":
    main()
