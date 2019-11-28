import pyrebase
import details
from datetime import datetime
import secrets 
import string 
from collections import OrderedDict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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

def newVisitor():
    hname = str(input("Host's Name: "))
    print("Validating.....")
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
        now = now.strftime("%d/%m/%Y, %H:%M:%S")
        Vdata = {"Name": Vname, "Email": Vmail, "Phone" : Vphone , \
            "In-time": now, "Status": False, "Host": allHost[href]['Name'], "H-Ref": href}
        Vref = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(9))
        db.child("Visitor").child(Vref).set(Vdata)
        print("Entry Successful")
        message = Mail(
        from_email='notifications@visitora.com',
        to_emails= allHost[href]['Email'],
        subject='A Person is Just Checked-In to Visit You',
        html_content='<strong>Details of the Person :</strong><ul><li>Name: {0} </li>\
            <li>Email: {1} </li><li>Phone: {2} </li></ul>'.format(Vname,Vmail,Vphone))
        response = sg.send(message)
        if response.status_code == 202:
            print("Host Intimated")
        else:
            print("Host Intimation Protocol Failed")
    except IndexError:
        print("No Person Found! ")
    