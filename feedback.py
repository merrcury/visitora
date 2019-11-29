import pyrebase
import details

config = {
  "apiKey": details.apiKey,
  "authDomain": details.authDomain,
  "databaseURL": details.databaseURL,
  "storageBucket": details.storageBucket,
  "serviceAccount": "visitor-a-firebase-adminsdk.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def FeedBack(name, rating, review, suggestions):
    data = {'Name': name, 'Rating': rating, 'Review': review, 'Suggestion': suggestions}
    db.child("Feedback").push(data)
    return("Successfully Posted ")

if __name__ == "__main__":
    print("Welcome to Feedback Wizard")
    try:
        Fname = input("Name :")
        while(True):
            Rating = int(input("Rate Between 0 and 5: "))
            if Rating > 5:
                print("Number is Above 5")
                Rating = int(input("Please, Rate Between 0 and 5: "))
            elif Rating < 0:
                print("Number is Below 0")
                Rating = int(input("Please, Rate Between 0 and 5: "))
            else:
                break
        Review = input("A short Review: ")
        Suggestions = input("Any Suggestion: ")
        print(FeedBack(Fname, Rating, Review, Suggestions))
    except ValueError:
        print("Number Only")