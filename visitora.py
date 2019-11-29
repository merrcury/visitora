import pyrebase #REST-API Client for firebase
import details #Confidential file Containing API Keys & Secret
from datetime import datetime
import secrets #Library with Secret Algo, , for  generating unique ref no.
import string 
from collections import OrderedDict
from sendgrid import SendGridAPIClient #Import Twilio SendGrid
from sendgrid.helpers.mail import Mail
# import only system from os 
from os import system, name 

# config = {
#   "apiKey": "apiKey",
#   "authDomain": "projectId.firebaseapp.com",
#   "databaseURL": "https://databaseName.firebaseio.com",
#   "storageBucket": "projectId.appspot.com",
#   "serviceAccount": "path/to/serviceAccountCredentials.json"
# } Get These details from Firebase

config = {
  "apiKey": details.apiKey,
  "authDomain": details.authDomain,
  "databaseURL": details.databaseURL,
  "storageBucket": details.storageBucket,
  "serviceAccount": "visitor-a-firebase-adminsdk.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database() #databse object creation

sg = SendGridAPIClient(details.twilioKey) #SendGrid Client Init

time_format = "%d/%m/%Y, %H:%M:%S" #Time format, for keeping it same

# define our clear function 
def clear(): 
    # for windows 
	if name == 'nt': 
		_ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
	else: 
		_ = system('clear') 

# define our new Visitor Function
def newVisitor():
    hname = str(input("Host's Name: "))
    print("Validating.....")
    print()
    try:
        #Checking for Multiple Host with Same Name
        allHost = db.child("Host").order_by_child("Name").equal_to(hname).get()
        allHost = dict(allHost.val())
        print("{0} Match Found".format(len(allHost)))
        for host in allHost.items():
            print(host)
        #Enter Reference Number of Particular Host
        href = input("Host Refrence Number: ")
        Vname = input("Enter Visitor's Name: ")
        Vmail = input("Enter Visitor's Email: ")
        Vphone = int(input("Enter Vistor's Phone: "))
        #Getting Check-In Time
        now = datetime.now()
        now = now.strftime(time_format)
        Vdata = {"Name": Vname, "Email": Vmail, "Phone" : Vphone , \
            "In-time": now, "Status": True, "H-Ref": href}
        #Generating 9 Digit Alpha Numberic Reference Number
        Vref = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(9))
        #Pushing to Real-Time DataBase
        db.child("Visitor").child(Vref).set(Vdata)
        print()
        print("Entry Successful")
        print("Visitor Reference Number: {0}".format(Vref))
        print()
        print("Intimating Host....")
        print()
        #Email Intimation Protocol
        # 'notifications@visitora.com' is a fictious mail, can't accept reply
        # Made from Notifications + Project name
        # Simple HTML Mail Preperation
        message = Mail(
        from_email='notifications@visitora.com',
        to_emails= allHost[href]['Email'], 
        subject='A Person is Just Checked-In to Visit You',
        html_content='<strong>Details of the Person :</strong>\
            <ul><li> Refernce Number: {0}</li>\
            <li>Name: {1} </li>\
            <li>Email: {2} </li>\
            <li>Phone: {3} </li></ul>'.format(Vref, Vname,Vmail,Vphone))
        response = sg.send(message)
        if response.status_code == 202:
            #202 : Successfully Send
            print("Host Intimated")
        else:
            #Other than 202: One or more Error Occured
            print("Host Intimation Protocol Failed")
    except IndexError:
        #Wrong Host Name
        print("No Person Found! ")

#function while Visitor is Leaving
def exitVisitor():
    #Reference Number,  Given to Visitor at the Time of Entry
    Vref = input("Visitor's Reference Number: ")
    if Vref:
        print("Validating.......")
        print()
        try:
            Vdetails = db.child("Visitor").child(Vref).get()
            Vdetails = dict(Vdetails.val())
            #Checking either visitor in building or already left
            if Vdetails['Status']:
                print(Vdetails)
                #Confirmation before exit
                conf = input("Confirm the Exit [Y/N]: ")
                conf = conf.upper()
                if conf == 'Y':
                    #Noting Down Check-Out Time
                    exit = datetime.now()
                    exit = exit.strftime(time_format)
                    #Pushing Update & Changing Flag to False
                    db.child("Visitor").child(Vref).update({"Out-time": exit, "Status": False})
                    print()
                    print("Exited Successfully")
                    print()
                    #Visitor Initimation Protocol
                    print("Intimating Visitor......")
                    #Retrieving Data about Host to the Visitor
                    Hdetails = db.child("Host").child(Vdetails['H-Ref']).get()
                    Hdetails = dict(Hdetails.val())
                    #Definig Mail
                    message = Mail(
                    from_email='notifications@visitora.com',
                    to_emails= Vdetails['Email'],
                    subject='Summary of Your Visit',
                    html_content='<strong>Details of the Visit :</strong>\
                    <ul><li> Refernce Number: {0}</li>\
                    <li>Name: {1} </li>\
                    <li>Phone: {2} </li>\
                    <li>Check-in Time: {3}</li>\
                    <li>Check-Out Time: {4}</li>\
                    <li>Host: {5}</li>\
                    <li>Address Visited: {6}</li></ul>\
                    <p>Thanks for Visiting</p>'\
                        .format(Vref,Vdetails['Name'],Vdetails['Phone'], \
                                Vdetails['In-time'], exit, Hdetails['Name'], Hdetails['Address'] ))
                    response = sg.send(message)
                    #Checking Success
                    if response.status_code == 202:
                        print()
                        print("Visitor Intimated")
                    else:
                        print()
                        print("Visitor Intimation Protocol Failed")
                #Pressed N while Exiting
                elif conf == 'N':
                    print("Exit Suspended")
                #Pressed anything other tahn Y/N
                else:
                    print("Exit Terminated due to Wrong Choice")
            #If Status is already false, means Visitor Already left
            #Telling the time when Visitor Left for convenience 
            else:
                print("Visitor already LEFT at {0}".format(Vdetails['Out-time']))
        #Non-Existen Visitor
        except TypeError:
            print('Wrong Details')
    #No Reference Number Entered
    else:
        print("You forgot to enter Refernce Number.")

#Checking for All existing Visitor in Building at Real time
def checkVisitor():
    #Filter All Visitor by Status Flag: True
    Vall = db.child("Visitor").order_by_child("Status").equal_to(True).get()
    Vall = Vall.each()
    i = 0
    #Iterate all results
    if len(Vall)>0:
        print("Visitors inside Building: ")
        for Vone in Vall:
            i+=1
            print()
            print("{0}. {1}".format(i,Vone.val()))
    #No Visitor with Status flag true
    else:
        print("No Visitor is inside Premises")

#defining main
if __name__ == "__main__":
    #welcome greet
    print("Welcome to VISITORA!! ")
    print()
    #Running until user terminates the program
    while(True):
        #Starting Menu
        print()
        print("1. New Visitor Entry")
        print("2. Exit Visitor")
        print("3. All Visitor")
        print("4. Quit")
        try:
            choice = int(input("Enter your Choice: "))
            print()
            if choice == 1:
                newVisitor()
                input("Press Enter to Continue") #To Hold Output, Sleep can also be used
                clear() #Just to Clear Console 
            elif choice == 2:
                exitVisitor()
                input("Press Enter to Continue") #To Hold Output, Sleep can also be used
                clear() #Just to Clear Console
            elif choice == 3:
                checkVisitor()
                input("Press Enter to Continue") #To Hold Output, Sleep can also be used
                clear() #Just to Clear Console
            elif choice == 4:
                print("Bye!") 
                break #terminating While Loop
            #Pressed other than choices
            else:
                print("Wrong Choice")
        #Pressed Enter or any Alphabet
        except ValueError:
            print("Number Only!!")