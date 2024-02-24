import pymysql
import tkinter as tk
from tkinter import messagebox


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


class SocialMediaApp:
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
                    "DELETE FROM posts WHERE postId = %s", (post_id,))
                self.cursor.execute(
                    "DELETE FROM comments WHERE postId = %s", (post_id,))
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


socialmediaapp = SocialMediaApp()
