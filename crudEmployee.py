import pyrebase
import details
import secrets 
import string
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

clear = lambda: os.system('clear')

def createEmployee():
  try:
    Ename = input("Employee's Name: ")
    Email = input("Employee's Mail Address: ")
    Ephone = int(input("Employee's Phone Number: "))
    Eloaction = input("Employee's location In Office: ")
    Edata = {"Name": Ename, "Email":  Email, "Phone": Ephone, "Address": Eloaction}
    Eref = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(7))
    db.child("Host").child(Eref).set(Edata)
    print()
    print("Creation Successful")
  except ValueError:
    print("Only Numbers Will be Accepted")

def removeEmployee():
  Eref = input("Enter Employee's Refernce Number: ")
  db.child("Host").child(Eref).remove()
  print()
  print("Successfully Removed")

def updateEmployee():
  Eref = input("Enter Employee's Refernce Number: ")
  print()
  print("1. Name Change")
  print("2. Email Chnage")
  print("3. Phone Chnage")
  print("4. Location Chnage")
  try:
    choice = int(input("Enter your Choice: "))
    print()
    if choice == 1:
      Ename = input("Employee's Name: ")
      db.child("Host").child(Eref).update({"Name": Ename})
      print("Name Updated Successfully")
    elif choice == 2:
      Email = input("Employee's Mail Address: ")
      db.child("Host").child(Eref).update({"Email": Email})
      print("E-mail Updated Successfully")
    elif choice == 3:
      Ephone = int(input("Employee's Phone Number: "))
      db.child("Host").child(Eref).update({"Phone": Ephone})
      print("Phone Number Updated Successfully")
    elif choice == 4:
      Eloaction = input("Employee's location In Office: ")
      db.child("Host").child(Eref).update({"Address": Eloaction})
      print("Location Updated Successfully")
    else:
        print("Wrong Choice")
  except ValueError:
    print("Number Only!!")

if __name__ == "__main__":
    print("Welcome to VISITORA!! Employee Portal")
    print()
    while(True):
        print()
        print("1. Create new Employee")
        print("2. Remove Old Employee")
        print("3. Update Details")
        print("4. Quit")
        try:
            choice = int(input("Enter your Choice: "))
            print()
            if choice == 1:
                createEmployee()
                input("Press Enter to Continue")
                clear()
            elif choice == 2:
                removeEmployee()
                input("Press Enter to Continue")
                clear()
            elif choice == 3:
                updateEmployee()
                input("Press Enter to Continue")
                clear()
            elif choice == 4:
                print("Bye!")
                break
            else:
                print("Wrong Choice")
        except ValueError:
            print("Number Only!!")