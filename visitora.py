import pyrebase
import details
from datetime import datetime
import secrets 
import string 
from collections import OrderedDict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

config = {
  "apiKey": details.apiKey,
  "authDomain": details.authDomain,
  "databaseURL": details.databaseURL,
  "storageBucket": details.storageBucket,
  "serviceAccount": "visitor-a-firebase-adminsdk.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

sg = SendGridAPIClient(details.twilioKey)

time_format = "%d/%m/%Y, %H:%M:%S"

clear = lambda: os.system('clear')

def newVisitor():
    hname = str(input("Host's Name: "))
    print("Validating.....")
    print()
    try:
        allHost = db.child("Host").order_by_child("Name").equal_to(hname).get()
        allHost = dict(allHost.val())
        print("{0} Match Found".format(len(allHost)))
        for host in allHost.items():
            print(host)
        href = input("Host Refrence Number: ")
        Vname = input("Enter Visitor's Name: ")
        Vmail = input("Enter Visitor's Email: ")
        Vphone = int(input("Enter Vistor's Phone: "))
        now = datetime.now()
        now = now.strftime(time_format)
        Vdata = {"Name": Vname, "Email": Vmail, "Phone" : Vphone , \
            "In-time": now, "Status": True, "H-Ref": href}
        Vref = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(9))
        db.child("Visitor").child(Vref).set(Vdata)
        print()
        print("Entry Successful")
        print("Visitor Reference Number: {0}".format(Vref))
        print()
        print("Intimating Host....")
        print()
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
            print("Host Intimated")
        else:
            print("Host Intimation Protocol Failed")
    except IndexError:
        print("No Person Found! ")

def exitVisitor():
    Vref = input("Visitor's Reference Number: ")
    if Vref:
        print("Validating.......")
        print()
        try:
            Vdetails = db.child("Visitor").child(Vref).get()
            Vdetails = dict(Vdetails.val())
            if Vdetails['Status']:
                print(Vdetails)
                conf = input("Confirm the Exit [Y/N]: ")
                conf = conf.upper()
                if conf == 'Y':
                    exit = datetime.now()
                    exit = exit.strftime(time_format)
                    db.child("Visitor").child(Vref).update({"Out-time": exit, "Status": False})
                    print()
                    print("Exited Successfully")
                    print()
                    print("Intimating Visitor......")
                    Hdetails = db.child("Host").child(Vdetails['H-Ref']).get()
                    Hdetails = dict(Hdetails.val())

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
                    if response.status_code == 202:
                        print()
                        print("Visitor Intimated")
                    else:
                        print()
                        print("Visitor Intimation Protocol Failed")
                elif conf == 'N':
                    print("Exit Suspended")
                else:
                    print("Exit Terminated due to Wrong Choice")
            else:
                print("Visitor already LEFT at {0}".format(Vdetails['Out-time']))
        except TypeError:
            print('Wrong Details')
    else:
        print("You forgot to enter Refernce Number.")

def checkVisitor():
    Vall = db.child("Visitor").order_by_child("Status").equal_to(True).get()
    Vall = Vall.each()
    i = 0
    if len(Vall)>0:
        print("Visitors inside Building: ")
        for Vone in Vall:
            i+=1
            print()
            print("{0}. {1}".format(i,Vone.val()))
    else:
        print("No Visitor is inside Premises")

if __name__ == "__main__":
    print("Welcome to VISITORA!! ")
    print()
    while(True):
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
                input("Press Enter to Continue")
                clear()
            elif choice == 2:
                exitVisitor()
                input("Press Enter to Continue")
                clear()
            elif choice == 3:
                checkVisitor()
                input("Press Enter to Continue")
                clear()
            elif choice == 4:
                print("Bye!")
                break
            else:
                print("Wrong Choice")
        except ValueError:
            print("Number Only!!")