import tkinter as tk
from tkinter import ttk
from tkinter import *
import customtkinter
from tkinter.messagebox import showinfo
import pymysql

from tkinter import messagebox
import re
from PIL import Image, ImageTk
import sqlalchemy

root = Tk()
root.geometry('400x400')
root.title('Final Project G5')
root.resizable(False, False)
# root.configure(background='black')


class PostViewWindow(tk.Toplevel):
    def __init__(self, post_id, cursor):  # Add the 'cursor' parameter
        super().__init__()
        self.title("Post View")

        self.post_id = post_id
        self.cursor = cursor
        self.title("Post View")

        self.post_id = post_id

        self.post_content_label = tk.Label(self, text="Post Content:")
        self.post_content_label.pack()
        self.post_content_text = tk.Text(self, height=5, width=30)
        self.post_content_text.pack()

        self.comments_label = tk.Label(self, text="Comments:")
        self.comments_label.pack()
        self.comments_listbox = tk.Listbox(self)
        self.comments_listbox.pack()

        self.fetch_post_content()
        self.fetch_comments()

    def fetch_post_content(self):
        try:
            self.cursor.execute(
                "SELECT postContent FROM posts WHERE postId = %s", (self.post_id,))
            post_content = self.cursor.fetchone()[0]
            self.post_content_text.insert(tk.END, post_content)
        except pymysql.Error as e:
            messagebox.showerror(
                "Error", f"Failed to fetch post content: {str(e)}")

    def fetch_comments(self):
        try:
            self.cursor.execute(
                "SELECT commentContent FROM comments WHERE postId = %s", (self.post_id,))
            comments = self.cursor.fetchall()
            for comment in comments:
                self.comments_listbox.insert(tk.END, comment[0])
        except pymysql.Error as e:
            messagebox.showerror(
                "Error", f"Failed to fetch comments: {str(e)}")


class PostEditor:
    def __init__(self):
        self.db_conn = pymysql.connect(
            host='localhost',
            user='root',
            password='meroloka800',
            database='social_media'
        )
        self.cursor = self.db_conn.cursor()

        self.root = tk.Tk()
        self.root.title("Social Media App")

        self.create_widgets()

    def create_widgets(self):
        self.post_name_label = tk.Label(self.root, text="Post Name:")
        self.post_name_label.pack()
        self.post_name_entry = tk.Entry(self.root)
        self.post_name_entry.pack()

        self.post_content_label = tk.Label(self.root, text="Post Content:")
        self.post_content_label.pack()
        self.post_content_entry = tk.Text(self.root, height=5, width=30)
        self.post_content_entry.pack()

        self.add_post_button = tk.Button(
            self.root, text="Add Post", command=self.add_post)
        self.add_post_button.pack()

        self.post_listbox = tk.Listbox(self.root)
        self.post_listbox.pack()

        self.comment_label = tk.Label(self.root, text="Comment:")
        self.comment_label.pack()
        self.comment_entry = tk.Text(self.root, height=3, width=30)
        self.comment_entry.pack()

        self.add_comment_button = tk.Button(
            self.root, text="Add Comment", command=self.add_comment)
        self.add_comment_button.pack()

        self.remove_post_button = tk.Button(
            self.root, text="Remove Post", command=self.remove_post)
        self.remove_post_button.pack()

        self.view_post_button = tk.Button(
            self.root, text="View", command=self.view_post)
        self.view_post_button.pack()

        self.root.mainloop()

        self.root.mainloop()

    def add_post(self):
        post_name = self.post_name_entry.get()
        post_content = self.post_content_entry.get("1.0", tk.END)

        try:
            self.cursor.execute(
                "INSERT INTO posts (postName, postContent) VALUES (%s, %s)", (post_name, post_content))
            self.db_conn.commit()
            messagebox.showinfo("Success", "Post added successfully")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Failed to add post: {str(e)}")

        self.update_post_listbox()

    def remove_post(self):
        selected_post = self.post_listbox.curselection()
        if selected_post:
            post_id = self.post_listbox.get(
                selected_post[0]).split(":")[0].strip()

            try:
                self.cursor.execute(
                    "DELETE FROM comments WHERE postId = %s", (post_id,))
                self.cursor.execute(
                    "DELETE FROM posts WHERE postId = %s", (post_id,))
                self.db_conn.commit()
                messagebox.showinfo("Success", "Post removed successfully")
            except pymysql.Error as e:
                messagebox.showerror(
                    "Error", f"Failed to remove post: {str(e)}")

            self.update_post_listbox()
        else:
            messagebox.showinfo("Info", "Please select a post to remove")

    def add_comment(self):
        selected_post = self.post_listbox.curselection()
        if selected_post:
            post_id = self.post_listbox.get(
                selected_post[0]).split(":")[0].strip()
            comment_content = self.comment_entry.get("1.0", tk.END)

            try:
                self.cursor.execute(
                    "INSERT INTO comments (commentContent, postId) VALUES (%s, %s)", (comment_content, post_id))
                self.db_conn.commit()
                messagebox.showinfo(
                    "Success", "Comment added successfully")
            except pymysql.Error as e:
                messagebox.showerror(
                    "Error", f"Failed to add comment: {str(e)}")
        else:
            messagebox.showinfo(
                "Info", "Please select a post to add a comment to")
        self.update_post_listbox()

    def view_post(self):
        selected_post = self.post_listbox.curselection()
        if selected_post:
            post_id = self.post_listbox.get(
                selected_post[0]).split(":")[0].strip()
            post_view_window = PostViewWindow(
                post_id, self.cursor)  # Pass the 'cursor' object
            post_view_window.mainloop()
        else:
            messagebox.showinfo("Info", "Please select a post to view")

    def update_post_listbox(self):
        self.post_listbox.delete(0, tk.END)

        try:
            self.cursor.execute("SELECT * FROM posts")
            posts = self.cursor.fetchall()
            for post in posts:
                self.post_listbox.insert(tk.END, f"{post[0]}: {post[1]}")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Failed to fetch posts: {str(e)}")


def validate_email(email):
    # Regular expression pattern to match a valid email address
    pattern = r"[^@]+@[^@]+\.[^@]+"

    # Check if the email address matches the pattern
    if re.match(pattern, email):

        return True

    else:

        return False


def open_new_window():
    new_window = tk.Toplevel()
    new_window.title("New Window")

    new_window.mainloop()


def passer(pas, userr, roll):
    query = sqlalchemy.text(
        f"insert into users values ( {userr} {pas}, {roll})")


user_email = tk.StringVar()
user_password = tk.StringVar()
user_email1 = tk.StringVar()
user_password1 = tk.StringVar()


def on1(event=None):
    login_btn.config(background='black', foreground='white')


def lv1(event=None):
    login_btn.config(background='white', foreground='black')


def on2(event=None):
    signup_btn.config(background='black', foreground='white')


def lv2(event=None):
    signup_btn.config(background='white', foreground='black')


def hide(event=None):
    root.geometry('400x400')


def singg():

    email = user_email.get()
    pwd = user_password.get()
    # r0le = role_entry.get()
    # conf_pwd = confirm_password_entry.get()
    if pwd.isspace() or pwd == "":
        msg = f"password cannot be empty!"
        showinfo(title="Information", message=msg)
    elif validate_email(email) == False:
        msg = f"Email is not valid!"
        showinfo(title="Information", message=msg)
    elif validate_email(email) == True:

        msg = f"You have registered successfully!"
        showinfo(title="Information", message=msg)

        # ...

        if __name__ == '__main__':
            # create a new root window
            root1 = tk.Tk()

            # create a new instance of the PostEditor class
            post_editor = PostEditor()

            # place the post editor in the root window
            post_editor.pack()

            # start the main event loop
            root1.mainloop()

    email = user_email.get()
    pwd = user_password.get()
    full = fullname.get()
    # r0le = role_entry.get()
    # conf_pwd = confirm_password_entry.get()

    post_editor = PostEditor(new_window)
    post_editor.pack()
    new_window.mainloop()
    USERNAME = 'root'
    PASSWORD = 'meroloka800'
    HOST = 'localhost'
    PORT = '3306'
    DB_NAME = 'social_media'
    # Create the database connection string
    DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    engine = sqlalchemy.create_engine(DB_URI)
    connection = engine.connect()

    # Get the current maximum value of the id column
    max_id_query = sqlalchemy.text("SELECT MAX(userId) FROM users")
    result = connection.execute(max_id_query)
    max_id = result.fetchone()[0]

    # Increment the maximum id value by 1
    new_id = max_id + 1

    # Insert the new row into the users table with the incremented id value
    insert_query = sqlalchemy.text(
        f"INSERT INTO users VALUES ({new_id}, '{email}', '{pwd}', 'mosa ayman', 'member')")
    connection.execute(insert_query)
    connection.commit()

    # Retrieve all the users from the users table
    select_query = sqlalchemy.text("SELECT * FROM users")
    result = connection.execute(select_query)

    # Print the results
    for row in result:
        print(row)

    connection.close()

    # engine = sqlalchemy.create_engine(DB_URI)
    # connection = engine.connect()
    # insert_query = sqlalchemy.text(
    #    f"INSERT INTO users VALUES ('',{email}', '{pwd}', 'mosa ayman', 'member')")
    # connection.execute(insert_query)
    # connection.commit()
    # Retrieve all the users from the users table
    # select_query = sqlalchemy.text("SELECT * FROM users")
    # result = connection.execute(select_query)
    # Print the results
    # for row in result:
    #    print(row)
    # connection.close()
    # tk.Label(new_window, text=f'your role {r0le}').pack()


def Checker(varo, user_email, user_pwd):
    for row in varo:
        if row[0] == user_email and row[1] == user_pwd:
            print(row)
            return True
    print(varo)
    return False


def Checkerr(varoo, user_email, user_pwd):
    for row in varoo:
        if row[0] == user_email and row[1] == user_pwd:
            print(row)
            return True
    print(varoo)
    return False


def logg():
    user_email = user_email1.get()
    user_pwd = user_password1.get()

    USERNAME = 'root'
    PASSWORD = 'meroloka800'
    HOST = 'localhost'
    PORT = '3306'
    DB_NAME = 'social_media'
    # Create the database connection string
    DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
    engine = sqlalchemy.create_engine(DB_URI)
    connection = engine.connect()
    check_user_and_pass = sqlalchemy.text(
        "SELECT username, password FROM users")
    result = connection.execute(check_user_and_pass)
    rows = result.fetchall()

    if Checker(rows, user_email, user_pwd) and Checkerr(rows, user_email, user_pwd):

        msg = f"Logged in Successfully!"
        showinfo(title="Information", message=msg)

        # define the UI elements for the post editor

        # ...

        if __name__ == '__main__':
            # create a new root window
            root1 = tk.Tk()

            # create a new instance of the PostEditor class
            post_editor = PostEditor()

            # place the post editor in the root window
            post_editor.pack()

            # start the main event loop
            root1.mainloop()

    else:
        msg = f"Login failed!"
        showinfo(title="Information", message=msg)


def log(event=None):
    root.geometry('630x400')
    b1 = Button(root, text='<', height=21, bd=0,
                relief=SOLID, bg='black', cursor='hand2', fg='white', command=hide)
    b1.place(x=610, y=6)
    f1 = Frame(root, bg='white', bd=0, relief=SOLID)
    f1.place(x=400, y=5, width=205, height=330)
    l = Label(f1, text='LOGIN SYSTEM', fg='black',
              bg='white', font=('Times New Roman', 16))
    l.place(x=10, y=10)

    email_log = customtkinter.CTkEntry(
        master=f1, placeholder_text="Enter email", textvariable=user_email1)
    email_log.place(x=10, y=80)

    l2 = Label(f1, text='email :', fg='black',
               bg='white', font=('Times New Roman', 12))
    l2.place(x=10, y=50)

    password_log = customtkinter.CTkEntry(
        master=f1, placeholder_text="Enter password",  textvariable=user_password1, show="*")
    password_log.place(x=10, y=140)

    l3 = Label(f1, text='password :', fg='black',
               bg='white', font=('Times New Roman', 12))
    l3.place(x=10, y=110)

    bu1 = customtkinter.CTkButton(master=f1, text='LOGIN', font=(
        'Times New Roman', 12), command=logg)
    bu1.place(x=10, y=170)


def sing(event=None):
    root.geometry('630x400')
    b1 = Button(root, text='<', height=21, bd=0,
                relief=SOLID, bg='black', cursor='hand2', fg='white', command=hide)
    b1.place(x=610, y=6)
    f1 = Frame(root, bg='white', bd=0, relief=SOLID)
    f1.place(x=400, y=5, width=205, height=390)
    l = Label(f1, text='SIGNUP SYSTEM', fg='black',
              bg='white', font=('Times New Roman', 16))
    l.place(x=10, y=10)

    email_sign = customtkinter.CTkEntry(
        master=f1, placeholder_text="email", textvariable=user_email)
    email_sign.place(x=10, y=80)

    l2 = Label(f1, text='email :', fg='black',
               bg='white', font=('Times New Roman', 12))
    l2.place(x=10, y=50)

    password_sing = customtkinter.CTkEntry(
        master=f1,  placeholder_text="password", textvariable=user_password, show="*")
    password_sing.place(x=10, y=140)

    l3 = Label(f1, text='password :', fg='black',
               bg='white', font=('Times New Roman', 12))
    l3.place(x=10, y=110)

    fullName = customtkinter.CTkEntry(
        master=f1)
    fullName.place(x=10, y=200)

    NL = Label(f1, text='full name :', fg='black',
               bg='white', font=('Times New Roman', 12))
    NL.place(x=10, y=170)

    bu2 = customtkinter.CTkButton(master=f1, text='SIGNUP', command=singg)
    bu2.place(x=10, y=300)
    radio_var = tk.IntVar()
    # tk.Radiobutton
    # common_bg = '#' + ''.join([hex(x)[2:].zfill(2) for x in (181, 26, 18)])
    # common_fg = '#ffffff'  # pure white

    def radiobutton_event():
        print("radiobutton toggled, current value:", radio_var.get())
    # ctkL = Label(f1, text='role :', fg='black')
    radiobutton_1 = tk.Radiobutton(master=f1, text='member', cursor='hand2', bd=1, relief=SOLID,
                                   command=radiobutton_event, variable=radio_var, value=1, )
    # ctkL1 = Label(f1, text='role :', fg='black')
    radiobutton_2 = tk.Radiobutton(master=f1, text='admin', cursor='hand2', bd=1, relief=SOLID,
                                   command=radiobutton_event, variable=radio_var, value=2, )
    # ctkL.place(x=15, y=150)
    # ctkL1.place(x=15, y=220)
    radiobutton_1.place(x=10, y=240)
    radiobutton_2.place(x=10, y=270)


# ======== [images] =========


def resizeImage(img, newWidth, newHeight):
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x*oldWidth/newWidth)
            yOld = int(y*oldHeight/newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage


logoimg = PhotoImage(file="images/logo.png")
logo = resizeImage(logoimg, 300, 200)
loginimg = PhotoImage(file='images/img2.png')
login = resizeImage(loginimg, 200, 100)
signupimg = PhotoImage(file='images/img2.png')
signup = resizeImage(signupimg, 200, 50)
logo_lab = Label(root, image=logo)
logo_lab.place(x=50, y=10)
# ======== [buttons] =========
login_btn = Button(root, text='LOGIN',
                   fg='white',
                   width='125',
                   bg='black',
                   image=login,
                   compound=TOP,
                   cursor='hand2',
                   bd=1,
                   relief=SOLID,
                   command=log
                   )
login_btn.place(x=70, y=233)

signup_btn = Button(root, text='SIGNUP',
                    fg='white',
                    width='125',
                    bg='black',
                    image=login,
                    compound=TOP,
                    cursor='hand2',
                    bd=1,
                    relief=SOLID,
                    command=sing
                    )
signup_btn.place(x=210, y=233)


login_btn.bind('<Enter>', on1)
login_btn.bind('<Leave>', lv1)

signup_btn.bind('<Enter>', on2)
signup_btn.bind('<Leave>', lv2)

# insert_query = sqlalchemy.text(
#    f"INSERT INTO users VALUES (1, 'johndoe', 'password123', 'John Doe', 'member')")
# connection.execute(insert_query)
# connection.commit()
# Retrieve all the users from the users table
# select_query = sqlalchemy.text("SELECT * FROM users")
# result = connection.execute(select_query)

# Print the results
# for row in result:
#   print(row)

root.mainloop()
