import pyrebase #REST-API Client for firebase
import details #Confidential file Containing API Keys & Secret

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
db = firebase.database()

#Defining FUnction for feedback
def FeedBack(name, rating, review, suggestions):
    data = {'Name': name, 'Rating': rating, 'Review': review, 'Suggestion': suggestions}
    db.child("Feedback").push(data)
    return("Successfully Posted ")

if __name__ == "__main__":
    #greet
    print("Welcome to Feedback Wizard")
    try:
        #Name for Feedback
        Fname = input("Name :")
        #Protection from false Rating
        while(True):
            Rating = int(input("Rate Between 0 and 5: "))
            #Protecting from Rating greater than 5
            if Rating > 5:
                print("Number is Above 5")
                Rating = int(input("Please, Rate Between 0 and 5: "))
            #Protection from Negative Rating
            elif Rating < 0:
                print("Number is Below 0")
                Rating = int(input("Please, Rate Between 0 and 5: "))
            #Processing On Right Rating
            else:
                break
        Review = input("A short Review: ")
        Suggestions = input("Any Suggestion: ")
        print(FeedBack(Fname, Rating, Review, Suggestions))
    except ValueError:
        print("Number Only")