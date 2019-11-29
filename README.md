# Visitora

![LOGO] (screenshots/Logo.png)

## Introduction
Visitora is an entry management system which captures several details about the Visitor and had an intelligent intimation protocol. This project is entirely written in Python3, stores its data on [Firebase](https://firebase.google.com/) in real-time which use [Twilio SendGrid](https://sendgrid.com/) for Email Intimation. 

## Set Up
I recommend, you to work in a virtual environment because This project uses some older version of the libraries and preventing this project to interfere with other projects. In your project directory, let's start off by creating a virtualenv:
``` bash 
$ python -m venv venv/
```
And let's activate it with the source command:
``` bash
$ source venv/bin/activate
```
Then, let's use pip to install the requirements:
``` bash
$ pip install -r requirements.txt
```
Create a file details.py with API Key, API Secrets and API URL from Firebase and Twilio SendGrid and place it in project folder. Download Firebase Service Account Key from Firebase and name it visitor-a-firebase-adminsdk.json and place it in project Folder.

## Approach 
The approach behind this is to manage entries, exits and current status of the Visitor in realtime using same software for different geographical gates of an office. The entire project's approach and workflow is defined with help of screenshots given below:
