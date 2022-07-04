import time
from datetime import datetime
import os
import pyrebase
import glob

firebaseConfig = {
    'apiKey': "AIzaSyBsvD0QlQjxViR8ERg1kE5TueN2SWmZVkQ",

    'authDomain': "myprojects-31e70.firebaseapp.com",

    'databaseURL': "https://myprojects-31e70-default-rtdb.firebaseio.com",

    'projectId': "myprojects-31e70",

    'storageBucket': "myprojects-31e70.appspot.com",

    'messagingSenderId': "763673836121",

    'appId': "1:763673836121:web:8ce58a2d740b610124cf48",

    'measurementId': "G-13G91J2KBD"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
''''

def Details():
    email = input('Enter email: ')
    passcode = input('Enter passcode: ')
    confirm_pass = input('Confirm passcode')
    create_user(email,passcode,confirm_pass)





def create_user(emai,passc,confirm_passc):
    if passc == confirm_passc:
        auth.create_user_with_email_and_password(emai, passc)
        print('Created Successfully')
    else:
        print('Passcode Mismatch Try Again')
        Details()

Details()



filename = "plot.png"
filename_new = filename[0:4]
CloudFileName = "Face/WithoutMask/{}".format(filename)

storage.child(CloudFileName).put(filename)
print('uploaded successfully')

url = storage.child(CloudFileName).get_url(None)
print(str(url))

from datetime import datetime

TimeStamp = datetime.now().strftime('%d%m%Y%H%M')
data = {'address': url, 'time': TimeStamp}
db.child("data").child("{}".format(filename_new)).push(data)
print('created successfully')
'''
wild = glob.glob(r"C:\Users\Julius Anumbia\Desktop\CovidEnforcement\MaskCheck\MaskCheck\Pictures/*")
num = -1
for number in wild:
    num = num + 1

    filename = wild[num]
    stringified = str(filename)
    filename_new = stringified[78:92]
    # Adding to storage
    CloudFileName = "Face/WithoutMask/{}".format(filename_new)
    print("file {} started uploading".format(wild[num]))
    storage.child(CloudFileName).put(filename)
    time.sleep(2)
    print("Done Uploading file {}".format(wild[num]))
    # Adding details to the database
    url = storage.child(CloudFileName).get_url(None)
    TimeStamp = datetime.now().strftime('%d%m%Y%H%M')
    data = {'address': url, 'time': TimeStamp}
    db.child("data").child("{}".format(filename_new)).push(data)
    print("{} created successfully".format(num))
    # Delecting the unwanted pic file after they have being uplloaded
    if os.path.exists(stringified):
        os.remove(stringified)
        print('File Deleted')
    else:
        print("The file does not exist")
    time.sleep(2)

print("Uploaded all successfully")
