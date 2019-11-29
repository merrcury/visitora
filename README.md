<p align="center">
  <a href="https://github.com/merrcury/visitora/">
    <img src="https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/Logo.png" alt="Bootstrap logo" width="150" height="150">
  </a>
</p>
<h1 align="center">Visitora</h1>

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
Create a file details.py with API Key, API Secrets and API URL from Firebase and Twilio SendGrid and place it in the project folder. Download Firebase Service Account Key from Firebase and name it visitor-a-firebase-adminsdk.json and place it in project Folder.

Security Rules for the firebase is defined later in this markdown. 

## Approach 
The approach behind this is to manage entries, exits and current status of the Visitor in realtime using the same software for different geographical gates of an office. The entire project's approach and workflow are defined with the help of screenshots given below:
* A Visitor has to tell the name of the person to the operator whom he/she wants to meet. Considering the possibility of multiple people with the same name in one office, Visitor should tell one another details about the host to an operator(like Email, Phone No., Location). A Unique 9-Digit Alpha Numeric reference number is also issued to the Visitor. 
![NewVisitor](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/newVisitor.png)

* As soon as Visitor enter the premises, Host gets the email with details of Visitor. 
![Email2Host](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/emailHost.png)

* When Visitor approaches any final exit, He/She need to reproduce the Reference Number(Printed on Visitor ID Card) to mark him successfully exited. 
![exitVisitor](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/exitVisitor.png)

* Visitor receives a summary of his visit as he/She exits the premises. 
![Email2Visitor](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/visiternotify.png)

* Once a person exited the premises and you enter his/her reference number again at exit portal, You will see a warning saying "Visitor already LEFT at (time)" with time when they left. 
![alreadyLeft](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/alreadyleft.png)

* You can always check the details of the visitors who are currently inside the premises. 
  * When someone is inside
  ![inside0](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/inside0.png)
  * When someone is not inside
  ![inside1](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/inside1.png)  

* Another program crudEmployee.py is used to perform special operations on Databases related to Employees.
  * Adding a new employee,
  ![newEmployee](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/newEmployee.png)  
  * Removing an employee from db, 
  ![removeEmployee](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/removeEmployee.png)
  * Updating Details about Employee. So, Visitor don't get trouble due to Outdated Information. 
  ![updateEmployee](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/updateEmployee.png)  
  
## Firebase
* Structure of the database is diven below:
  * Closed Overview of Visitora.
  ![firebase1](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/firebase1.png)
  * Expanded View of Feedback DB. Feedback to this product can be given using feedback.py.
  ![firebase2](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/firebase2.png)
  * Data Organisation in Host Corner can be seen below:
  ![firebase3](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/firebase3.png)
  * Management of Visitors Portion is shown below:
  ![firebase4](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/firebase4.png)

* **Security Rules of Firebase is to be defined as follows:**
![firebase5](https://raw.githubusercontent.com/merrcury/visitora/master/screenshots/firebaserules.png)

## Extended Approach 
* At the time of Entry, Face of Visitor can be registered for Facial Recognition which will keep track of the visitor's movement in and around the premises and will increase security.
* Self-service kiosks can be programmed at entry and exit to register details, dispersing Visitor's ID and to get details of Visitor by using an ADMIN Key. 
