CREATE DATABASE social_media;

USE social_media;

CREATE TABLE users (
    userId INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    fullName  VARCHAR(100),
    role ENUM('admin', 'member')
);

CREATE TABLE posts (
    postId  INT AUTO_INCREMENT PRIMARY KEY,
    postName VARCHAR(100) ,
    postContent TEXT,
    userId INT,
    FOREIGN KEY (userId) REFERENCES users(userId)
);


CREATE TABLE comments (
    commentId INT AUTO_INCREMENT PRIMARY KEY ,
    commentContent TEXT,
    postId INT,
    userId INT,
    FOREIGN KEY (postId) REFERENCES posts(postId) ,
    FOREIGN KEY (userId) REFERENCES users(userId)
);