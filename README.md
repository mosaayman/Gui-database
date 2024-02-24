# Social Media App README

## Overview

This is a simple social media application implemented in Python using the Tkinter library for the GUI and MySQL for the backend database. The application allows users to sign up, log in, create posts, add comments to posts, view posts, and remove posts.

## Features

- **User Authentication**: Users can sign up with a unique username and password. Passwords are stored securely in the database.
- **Post Management**: Users can create posts, view posts, and remove their own posts.
- **Commenting System**: Users can add comments to posts.
- **Role-based Access Control**: Users are assigned roles of either 'admin' or 'member'.

## Dependencies

- Python 3.x
- Tkinter
- MySQL
- pymysql
- sqlalchemy
- Pillow (PIL)

## Setting up the Database

1. Create a MySQL database named `social_media`.
2. Use the `social_media` database.
3. Run the provided SQL script to create the necessary tables: `users`, `posts`, and `comments`.

## Running the Application

1. Clone this repository to your local machine.
2. Ensure you have all dependencies installed.
3. Run the `social_media.py` file using Python.

## Usage

1. Launch the application.
2. Sign up for a new account or log in with an existing account.
3. Once logged in, you can create posts, view posts, add comments to posts, and remove your own posts if you're the author.
4. As an admin, you have additional privileges such as viewing all posts and removing any post.

## File Structure

- `social_media.py`: Main Python script containing the application logic.
- `images/`: Directory containing image resources used in the GUI.
- `README.md`: Readme file providing an overview of the application.
