import tkinter as tk
from tkinter import messagebox, simpledialog


class LibrarySystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Library System")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="用户名:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="密码:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="登录", command=self.login)
        self.login_button.grid(row=2, column=0)
        # self.register_button = tk.Button(self.login_frame, text="注册", command=self.register)
        # self.register_button.grid(row=2, column=1)

        self.operation_frame = tk.Frame(self)
        self.operation_frame.pack()

        self.show_books_button = tk.Button(self.operation_frame, text="查看图书", command=self.show_books)
        self.show_books_button.grid(row=0, column=0)
        self.rend_books_button = tk.Button(self.operation_frame, text="借书", command=self.rend_books)
        self.rend_books_button.grid(row=0, column=1)
        self.return_books_button = tk.Button(self.operation_frame, text="还书", command=self.return_books)
        self.return_books_button.grid(row=1, column=0)
        self.mod_pwd_button = tk.Button(self.operation_frame, text="修改密码", command=self.mod_pwd)
        self.mod_pwd_button.grid(row=1, column=1)
        self.logout_button = tk.Button(self.operation_frame, text="退出登录", command=self.logout)
        self.logout_button.grid(row=2, column=0)

        self.operation_frame.pack_forget()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open('Users.txt', 'r', encoding='utf-8') as rstream:
            while True:
                user = rstream.readline()
                if not user:
                    messagebox.showerror("错误", "用户名或者密码输入有误！")
                    return False

                input_user = '{} {}\n'.format(username, password)
                if user == input_user:
                    messagebox.showinfo("成功", "用户登录成功！")
                    self.login_frame.pack_forget()
                    self.operation_frame.pack()
                    return username

    class UserRegistrationApp:
        def __init__(self):
            self.window = tk.Tk()

            # 创建用户名输入框
            username_label = tk.Label(self.window, text="用户名:")
            username_label.pack()
            self.username_entry = tk.Entry(self.window)
            self.username_entry.pack()

            # 创建密码输入框
            password_label = tk.Label(self.window, text="密码:")
            password_label.pack()
            self.password_entry = tk.Entry(self.window, show="*")
            self.password_entry.pack()

            # 创建注册按钮
            register_button = tk.Button(self.window, text="注册", command=self.register)
            register_button.pack()

        def register(self):
            username = self.username_entry.get()
            pwd = self.password_entry.get()

            if not username:
                messagebox.showerror("错误", "请输入用户名!")
                return 0

            user_exists = False
            with open('Users.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    existing_username, _ = line.split(' ')
                    if existing_username == username:
                        user_exists = True
                        break

            if user_exists:
                messagebox.showerror("错误", "用户名已存在!")
            else:
                rpwd = simpledialog.askstring("确认密码", "请输入确认密码", show="*")
                if rpwd == pwd:
                    with open('Users.txt', 'a', encoding='utf-8') as f:
                        f.write('{} {}\n'.format(username, pwd))
                    messagebox.showinfo("成功", "用户注册成功!")
                else:
                    messagebox.showerror("错误", "密码不一致！")

        def run(self):
            self.window.mainloop()

    app = UserRegistrationApp()
    app.run()
    def show_books(self):
        with open('Books.txt', 'r', encoding='utf-8') as rstream:
            books = rstream.readlines()
            books_str = "---------图书馆里面的图书有:----------\n"
            for book in books:
                books_str += book
            messagebox.showinfo("图书", books_str)

    def rend_books(self):
        to_rend = '《' + simpledialog.askstring("借书", "请输入要借的书名") + '》'
        username = self.username_entry.get()

        tm = False
        not_exist = True
        user_line = 0
        book_i = 0
        book_find = False
        booksbuffer = []

        with open('Books.txt', 'r', encoding='utf-8') as f:
            books = f.readlines()
            for i, book in enumerate(books):
                if to_rend in book:
                    book_i = i
                    book_find = True
                    break
            if book_find == False:
                messagebox.showerror("错误", "不存在这本书!")
                return False
            booksbuffer = books

        if int(booksbuffer[book_i].split(' ')[1]) > 0:
            with open('User_book.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if username in line:
                        not_exist = False
                        user_line = i
                        if to_rend in line:
                            tm = True
                            messagebox.showerror("错误", "不可以借阅同名书籍")

                if not_exist == False:
                    lines[user_line] = lines[user_line].rsplit('\n')[0] + ',' + to_rend + '\n'
                    if tm == False:
                        with open('User_book.txt', 'w', encoding='utf-8') as f:
                            for i in lines:
                                f.write(i)
                        messagebox.showinfo("成功", "借书成功")
                else:
                    msg = username + ' ' + to_rend + '\n'
                    with open('User_book.txt', 'a', encoding='utf-8') as f:
                        f.write(msg)
                        messagebox.showinfo("成功", "借书成功")

            if tm == False:
                booksbuffer[book_i] = booksbuffer[book_i].split(' ')[0] + ' ' + str(
                    int(booksbuffer[book_i].split(' ')[1]) - 1) + '\n'
                with open('Books.txt', 'w', encoding='utf-8') as f:
                    for i in booksbuffer:
                        f.write(i)
        else:
            messagebox.showerror("错误", "该书已借完")

    def return_books(self):
        to_return = '《' + simpledialog.askstring("还书", "请输入要还的书名") + '》'
        username = self.username_entry.get()

        book_i = 0
        book_find = False
        userbuffer = []

        with open('User_book.txt', 'r', encoding='utf-8') as f:
            users = f.readlines()
            for i, user in enumerate(users):
                if username in user:
                    tmp = user.split(' ')[1].split(',')
                    if (len(tmp) == 0):
                        messagebox.showerror("错误", "用户拥有书籍为空,不能还书哦！")
                        return
                    tmp[-1] = tmp[-1].rstrip('\n')
                    if (to_return not in tmp):
                        messagebox.showerror("错误", "要还的书不在用户拥有书籍中")
                        return
                    msg = username + ' '
                    tmp_list = []
                    for i in tmp:
                        if i != to_return:
                            tmp_list.append(i)
                    msg = msg + ','.join(tmp_list) + "\n"
                    userbuffer.append(msg)
                    continue
                userbuffer.append(user)

        with open('User_book.txt', 'w', encoding='utf-8') as f:
            for i in userbuffer:
                f.write(i)

        with open('Books.txt', 'r', encoding='utf-8') as f:
            books = f.readlines()
            for i, book in enumerate(books):
                if to_return in book:
                    book_i = i
                    book_find = True
            if book_find:
                books[book_i] = books[book_i].split(' ')[0] + ' ' + str(int(books[book_i].split(' ')[1]) + 1) + '\n'
                with open('Books.txt', 'w', encoding='utf-8') as f:
                    for i in books:
                        f.write(i)
                    messagebox.showinfo("成功", "还书成功！")
            else:
                messagebox.showerror("错误", "该书在书架中不存在！")

    def mod_pwd(self):
        username = self.username_entry.get()
        password = simpledialog.askstring("修改密码", "请输入原密码", show="*")

        with open('Users.txt', 'r', encoding='utf-8') as f:
            pwds = f.readlines()
            for i, pwd in enumerate(pwds):
                if password in pwd:
                    new_pwd = simpledialog.askstring("修改密码", "请输入新密码", show="*")
                    pwds[i] = username + ' ' + new_pwd + '\n'
                    with open('Users.txt', 'w', encoding='utf-8') as f:
                        for i in pwds:
                            f.write(i)
                    messagebox.showinfo("成功", "修改密码成功")
                    return
            messagebox.showerror("错误", "请输入正确的密码")

    def logout(self):
        self.operation_frame.pack_forget()
        self.login_frame.pack()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = LibrarySystem()
    app.mainloop()