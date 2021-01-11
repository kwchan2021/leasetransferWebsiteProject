# [Firebase package]
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# [Use storage to store images]
from firebase import storage
from firebase_admin import storage
# [Use storage to store images]

# [Firebase package]
# [Pyrebase package]
import pyrebase
from getpass import getpass #what is this
# [Pyrebase package]
# [Flask API]
from flask import(
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
# [Flask API]
# [Datetime library]
import datetime
# [Datetime library]
# [json]
import json
from jsonpath_ng import jsonpath, parse
# [json]
# [Displaying Search Results]
from flask_table import Table, Col
# [Displaying Search Results]
# [Enable flask to have markup msg -> hyperlink]
from flask import Markup
# [Enable flask to have markup msg -> hyperlink]

# [Timestamp]
from datetime import datetime
# [Timestamp]

# [File Upload]
from werkzeug.utils import secure_filename
import os
import tempfile
# [File Upload]

# [Create Acc auth]
import argparse
from pprint import pprint
# [Create Acc auth]

# [Firebase Key and initialize]
config = {
    'apiKey': "AIzaSyBpkQ9Y6UitaltQIeMkIqI5xcAbxJvF0qM",
    'authDomain': "leasetransfersite.firebaseapp.com",
    'databaseURL': "https://leasetransfersite.firebaseio.com",
    'projectId': "leasetransfersite",
    'storageBucket': "leasetransfersite.appspot.com",
    'messagingSenderId': "74227457009",
    'appId': "1:74227457009:web:c2859ae458b610949b8250",
    'measurementId': "G-GNW0HEQ5RK"
}
firebase = pyrebase.initialize_app(config) # [initialize with pyrebase using firebase key]

# [Authentication]
auth = firebase.auth()
# [Authentication]

# [Bucket]
#bucket = firebase.storage_bucket(name="bucketName", app="bucketApp")
# [Bucket]

# [Firebase Key and initialize]

# [Firestore db]
cred = credentials.Certificate('service_key.json') #credentials
firebase_admin.initialize_app(cred, {
    'apiKey': 'AIzaSyBpkQ9Y6UitaltQIeMkIqI5xcAbxJvF0qM',
    'authDomain': 'leasetransfersite.firebaseapp.com',
    'databaseURL': 'https://leasetransfersite.firebaseio.com',
    'projectId': 'leasetransfersite',
    'storageBucket': 'leasetransfersite.appspot.com',
    'messagingSenderId': '74227457009',
    'appId': '1:74227457009:web:c2859ae458b610949b8250',
    'measurementId': 'G-GNW0HEQ5RK'
})
db = firestore.client()
# [Firestore db]

# [Firebase Storage]
storage = firebase.storage()
# [Firebase Storage]

# [Flask and initialize]
app = Flask(__name__)
app.secret_key = 'tempKey' #dont know what is it for
# [Flask and initialize]



# [Ads obj]
class adsObj:
    def __init__(self, leaseTitle, size, provinces, city, address, contractLength, description, email, tel, availability):
        self.leaseTitle = leaseTitle
        self.size= size
        self.provinces = provinces
        self.city = city
        self.address = address
        self.contractLength = contractLength
        self.description = description
        self.email = email
        self.tel = tel
        self.availability = availability
# [Ads obj]

# [Ads obj alternative]
class adsObjAlt:
    def __init__(self, leaseTitle, size, provinces, city, address, contractLength, description, email, tel, availability, by_who):
        self.leaseTitle = leaseTitle
        self.size= size
        self.provinces = provinces
        self.city = city
        self.address = address
        self.contractLength = contractLength
        self.description = description
        self.email = email
        self.tel = tel
        self.availability = availability
        self.by_who = by_who
# [Ads obj alternative]

# [Ads obj with key]
class adsObjAlt_WithKey:
    def __init__(self, leaseTitle, size, provinces, city, address, contractLength, description, email, tel, availability, by_who, postedAt):
        self.leaseTitle = leaseTitle
        self.size= size
        self.provinces = provinces
        self.city = city
        self.address = address
        self.contractLength = contractLength
        self.description = description
        self.email = email
        self.tel = tel
        self.availability = availability
        self.by_who = by_who
        # key
        self.postedAt = postedAt # pass the key into the argument
        # key
# [Ads obj with key]

# [Global variable]
globalAdsobj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")
globalTitle = "Start globalTitle"
adsSearchResultArray = ["Start adsSearchResultArray"]
# [Global variable]

# ==========[Function to route around]==========
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('home'))

@app.route('/ads', methods=['GET', 'POST'])
def ads():
    global globalTitle
    logo = storage.child("logo.jpg").get_url(None)

    #need to retrieve user data - ads posted by user
    if 'user' in session:

        results = getSpecificUserData(session['user'])
        table = OwnAds(results)
        table.border = True
        table.no_items = "You did not put any ads"

        if request.method == 'POST':
            globalTitle = request.form['apartmentChoice']
            return redirect(url_for('adsDetails'))


        return render_template('ads.html', user=session['user'], table=table, logo=logo)

    return redirect(url_for('login'))

@app.route('/adsDetails', methods=['GET', 'POST'])
def adsDetails():

    global globalTitle
    logo = storage.child("logo.jpg").get_url(None)
    img = ""

    # Redirect to adsSearch.html if there is no input
    if (globalTitle == "Start globalTitle"):
        return redirect(url_for('adsSearch'))
    # Redirect to adsSearch.html if there is no input

    objlist = globalTitle.split(" By ")
    if (len(objlist)>0):
        print(objlist)
    
    anotherObjlist = objlist[1].split(" At ")

    leaseTitle = objlist[0]
    email = "By " + anotherObjlist[0]
    postedAt = "At " + anotherObjlist[1]

    # Search in the database
    searchobjArray = getAllData()

    theSize = ""
    theProvince = ""
    theCity = ""
    theAddress = ""
    theContractLength = ""
    theDescription = ""
    theTel = ""
    theAvailability = ""

    for obj in searchobjArray:
        if obj.leaseTitle == leaseTitle:
            theSize = obj.size
            theProvince = obj.provinces
            theCity = obj.city
            theAddress = obj.address
            theContractLength = obj.contractLength
            theDescription = obj.description
            theTel = obj.tel
            theAvailability = obj.availability

            if obj.size == "1.5":
                img = storage.child("bachlor.png").get_url(None)
            elif obj.size == "2.5":
                img = storage.child("bachlor.png").get_url(None)
            elif obj.size == "3.5":
                img = storage.child("onebedroom.png").get_url(None)
            elif obj.size == "4.5":
                img = storage.child("twobedroom.png").get_url(None)
            elif obj.size == "5.5":
                img = storage.child("house.png").get_url(None)
            elif obj.size == "House":
                img = storage.child("house.png").get_url(None)
            elif obj.size == "Townhouse":
                img = storage.child("house.png").get_url(None)
            elif obj.size == "Others":
                img = storage.child("house.png").get_url(None)

    # Search in the database

    if 'user' in session:   
        msg='Hi, '
        msg1=Markup('(<a href=/logout>Logout</a> / <a href="/ads">Your own ads</a>)')

        return render_template('adsDetails.html', title=leaseTitle, email=email, postedAt=postedAt, size=theSize, province=theProvince, city=theCity, address=theAddress, contractLength=theContractLength, description=theDescription, tel=theTel, availability=theAvailability, msg=msg, user=session['user'], msg1=msg1, logo=logo, img=img)

    else:
        return render_template('adsDetails.html', title=leaseTitle, email=email, postedAt=postedAt, size=theSize, province=theProvince, city=theCity, address=theAddress, contractLength=theContractLength, description=theDescription, tel=theTel, availability=theAvailability, user=Markup('Hi Guest (<a href="/login">Login</a> / <a href="/createAccount">Create Account</a>)'), logo=logo, img=img)

@app.route('/adsSearch', methods=['GET', 'POST'])
def adsSearch():
    logo = storage.child("logo.jpg").get_url(None)
    global adsSearchResultArray
    objArray = []

    refobjArray = getAllData()

    userinput = ""

    if request.method == 'POST':
        provinces = request.form['inputProvinces']
        city = request.form['inputCity']
        size  = request.form['inputSize']
        userinput = provinces + " " + city + " " + size + " "

        for obj in refobjArray:
            if (obj.provinces == provinces):
                if (obj.city == city):
                    objArray.append(obj)

        # [Implement later]
        # facilities search
        # [Implement later]

        adsSearchResultArray = search_adsSearchHTML(provinces, city, size)

        return redirect(url_for('adsSearchResult'))
    
    if 'user' in session:
        msg='Hi, '
        msg1=Markup('(<a href=/logout>Logout</a> / <a href="/ads">Your own ads</a>)')
        return render_template('adsSearch.html',msg=msg, user=session['user'], msg1=msg1, logo=logo)
    else:
        return render_template('adsSearch.html', user=Markup('Hi Guest (<a href="/login">Login</a> / <a href="/createAccount">Create Account</a>)'), logo=logo)

@app.route('/adsSearchResult', methods=['GET', 'POST'])
def adsSearchResult():

    logo = storage.child("logo.jpg").get_url(None)
    global adsSearchResultArray #to print the search result
    global globalTitle#to store it before redirecting to ads.html

    table = OwnAds(adsSearchResultArray)
    table.border = True
    table.no_items = ""

    if request.method == 'POST':
        globalTitle = globalTitle = request.form['apartmentChoice']
        return redirect(url_for('adsDetails'))

    if 'user' in session:
        msg='Hi, '
        msg1=Markup('(<a href=/logout>Logout</a> / <a href="/ads">Your own ads</a>)')
        return render_template('adsSearchResult.html',msg=msg, user=session['user'], msg1=msg1, table=table, logo=logo)
    else:
        return render_template('adsSearchResult.html', user=Markup('Hi Guest (<a href="/login">Login</a> / <a href="/createAccount">Create Account</a>)'), table=table, logo=logo)


@app.route('/adsPosting', methods=['GET', 'POST'])
def adsPosting():
    logo = storage.child("logo.jpg").get_url(None)

    countUserArray = []

    if 'user' in session:
        if request.method == 'POST':
            #get data from the form
            leaseTitle = request.form['inputLeaseTitle']
            size  = request.form['inputSize']
            provinces = request.form['inputProvinces']
            city = request.form['inputCity']
            address = request.form['inputAddress']
            contractLength = request.form['inputContractLength']
            description = request.form['inputDescription']
            email = request.form['inputEmail']
            tel = request.form['inputTel']
            availability = request.form['inputAvailability']
            by_who = session['user']
            #get data from the form

            countUserArray = getSpecificUserData(by_who)
            
            if(len(countUserArray) < 3):
                appendData(leaseTitle, size, provinces, city, address, contractLength, description, tel, email, availability, by_who)
                return redirect(url_for('ads')) #to figure out how to direct to that specific app
            else:
                return redirect(url_for('error'))
        return render_template('adsPosting.html', user=session['user'], logo=logo)
    return redirect(url_for('login'))

@app.route('/error', methods=['GET', 'POST'])
def error():
    if 'user' in session:
        logo = storage.child("logo.jpg").get_url(None)
        return render_template('error.html', logo=logo)
    return redirect(url_for('home'))

# [Email verification]
# [Email verification]

#TODO use the email verification
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    logo = storage.child("logo.jpg").get_url(None)
    pic = storage.child("pic1.svg").get_url(None)
    msg = ""

    if not('user' in session):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            cpassword = request.form['cpassword']

            try:
                if(password == cpassword):
                    #auth.send_email_verification(email, password)
                    auth.create_user_with_email_and_password(email, password) #login
                    return redirect(url_for('home'))
                else:
                    msg = "Password are not the same.\nCannot create account.\nPlease try again."
                    print("password not the same")
                    #return redirect(url_for('createAccount'))

            except:
                print("Fail to create account")
                return redirect(url_for('createAccount'))

        return render_template('createAccount.html', msg=msg, logo=logo, pic=pic)

    return redirect(url_for('home'))

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        email = email = request.form['email']
        return redirect(url_for('home'))
    return render_template('forgotPassword.html')

#can be deleted
@app.route('/guesthome', methods=['GET', 'POST'])
def guesthome():
    logo = storage.child("logo.jpg").get_url(None)

    if not('user' in session):
        objArray = []

        if request.method == 'POST':
            if request.form['apartmentChoice'] == 'StudioApartments':
                objArray = searchSuggestedData("StudioApartments")
            elif request.form['apartmentChoice'] == 'ApartmentsForCouple':
                objArray = searchSuggestedData("ApartmentsForCouple")
            elif request.form['apartmentChoice'] == 'ApartmentsForFamilyWithKids':
                objArray = searchSuggestedData("ApartmentsForFamilyWithKids")
            elif request.form['apartmentChoice'] == 'ApartmentsWithGym':
                objArray = searchSuggestedData("ApartmentsWithGym")
            elif request.form['apartmentChoice'] == 'LuxuryApartmentsPenthouses':
                objArray = searchSuggestedData("LuxuryApartmentsPenthouses")
            elif request.form['apartmentChoice'] == 'Townhouses':
                objArray = searchSuggestedData("Townhouses")
            else:
                objArray = getAllData() # [Get the whole list first]
                #searchData(request.form['apartmentChoice'])
                print(request.form['apartmentChoice'])
        
        table = OwnAds(objArray)
        table.border = True
        table.no_items = ""
        return render_template('guesthome.html', user='guest', table=table, logo=logo)

    return redirect(url_for('home'))

@app.route('/home', methods=['PUT', 'POST', 'GET', 'PATCH'])
def home():
    objArray = []
    global globalTitle

    # Logo
    logo = storage.child("logo.jpg").get_url(None)
    #logo = "https://drive.google.com/file/d/11OWsc5qAV_7rWone-FXVZkNLq4WhIJdZ/view?usp=sharing"
    # Logo

    if request.method == 'POST':
        if request.form['apartmentChoice'] == 'StudioApartments':
            objArray = searchSuggestedData("StudioApartments")
            print(objArray[0].leaseTitle)
        elif request.form['apartmentChoice'] == 'ApartmentsForCouple':
            objArray = searchSuggestedData("ApartmentsForCouple")
            print(objArray[0].leaseTitle)
        elif request.form['apartmentChoice'] == 'ApartmentsForFamilyWithKids':
            objArray = searchSuggestedData("ApartmentsForFamilyWithKids")
            print(objArray[0].leaseTitle)
        elif request.form['apartmentChoice'] == 'ApartmentsWithGym':
            objArray = searchSuggestedData("ApartmentsWithGym")
            print(objArray[0].leaseTitle)
        elif request.form['apartmentChoice'] == 'LuxuryApartmentsPenthouses':
            objArray = searchSuggestedData("LuxuryApartmentsPenthouses")
            print(objArray[0].leaseTitle)
        elif request.form['apartmentChoice'] == 'Townhouses':
            objArray = searchSuggestedData("Townhouses")
            print(objArray[0].leaseTitle)

        #redirect case
        else:
            print(globalTitle)
            globalTitle = request.form['apartmentChoice']
            print(globalTitle)
            return redirect(url_for('adsDetails'))
        #redirect case


    table = OwnAds(objArray)
    table.border = True
    table.no_items = ""

    if 'user' in session:   
        msg='Hi, '
        msg1=Markup('(<a href=/logout>Logout</a> / <a href="/ads">Your own ads</a>)')

        return render_template('home.html',msg=msg, user=session['user'], msg1=msg1, table=table, logo=logo)

    else:
        return render_template('home.html', user=Markup('Hi Guest (<a href="/login">Login</a> / <a href="/createAccount">Create Account</a>)'), table=table, logo=logo)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logo = storage.child("logo.jpg").get_url(None)

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            auth.sign_in_with_email_and_password(email, password) #login
            session['user'] = email #create session
            return redirect(url_for('home'))

        except:
            print("Fail to login")
            return redirect(url_for('login'))

    return render_template('login.html', logo=logo)

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    session.pop('user', None)
    return index()
    #return render_template('guesthome.html')

# ==========[Function to route around]==========


# ==========[Supporting function]==========

#to append data
def appendData(leaseTitle, size, provinces, city, address, contractLength, description, tel, email, availability, user_session_email):
    
    #index of the data
    docs = db.collection(u'contracts').stream()
    count = 1
    for doc in docs:
        count = count+1
    #index of the data

    #time stamp
    now = datetime.now().strftime("%y/%m/%d-%H:%M:%S")
    #time stamp

    data = {
        'leaseTitle':leaseTitle,
        'size':size,
        'provinces':provinces,
        'city':city,
        'address':address,
        'contractLength':contractLength,
        'description':description,
        'tel':tel,
        'email':email,
        'availability':availability,
        'by_who':user_session_email, #added

        #unique id for contract
        #add time stamp
        #add index <- key        
        'index': count, 
        'postedAt': now
    }
    name = "-".join(leaseTitle.split())
    db.collection(u'contracts').document(name).set(data)


def getSpecificUserData(user_email):

####====
    objArray = []
    refobjArray = getAllData()

    refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

    for i in range(len(refobjArray)):
        refObj = refobjArray[i]
        
        #add input form and input
        part1 = Markup('<form method="POST">')
        part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
        part3 = refObj.leaseTitle
        part4 = " By "
        part5 = refObj.email
        part6 = " At "
        part7 = refObj.postedAt
        part8 = Markup('">')
        part9 = Markup('<input type="submit" value="')
        part10 = refObj.leaseTitle
        part11 = " By "
        part12 = refObj.email
        part13 = " At "
        part14 = refObj.postedAt
        part15 = Markup('">')
        part16 = Markup("</form>")
        refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
        #add input form and input

        finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)
        if(finalObj.email == user_email):
         objArray.append(finalObj)

    return objArray


# [Search for adsSearch.html]
def search_adsSearchHTML(provinces, city, size):
    objArray = []
    refobjArray = getAllData()

    refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

    for i in range(len(refobjArray)):
        refObj = refobjArray[i]
        
        #add input form and input
        part1 = Markup('<form method="POST">')
        part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
        part3 = refObj.leaseTitle
        part4 = " By "
        part5 = refObj.email
        part6 = " At "
        part7 = refObj.postedAt
        part8 = Markup('">')
        part9 = Markup('<input type="submit" value="')
        part10 = refObj.leaseTitle
        part11 = " By "
        part12 = refObj.email
        part13 = " At "
        part14 = refObj.postedAt
        part15 = Markup('">')
        part16 = Markup("</form>")
        refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
        #add input form and input

        finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)
        if(finalObj.provinces == provinces):
            if(finalObj.city == city):
                if(finalObj.size == size):
                    objArray.append(finalObj)

    return objArray

# [Search for adsSearch.html]

# [Search suggested data]
def searchSuggestedData(keyword):
    objArray = []
    refobjArray = getAllData()

    if(keyword == "StudioApartments"):
        refObj = adsObjAlt_WithKey("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability", "by_who", "time")

        for i in range(len(refobjArray)):
            refObj = refobjArray[i]
            
            #add input form and input
            part1 = Markup('<form method="POST">')
            part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
            part3 = refObj.leaseTitle
            part4 = " By "
            part5 = refObj.email
            part6 = " At "
            part7 = refObj.postedAt
            part8 = Markup('">')
            part9 = Markup('<input type="submit" value="')
            part10 = refObj.leaseTitle
            part11 = " By "
            part12 = refObj.email
            part13 = " At "
            part14 = refObj.postedAt
            part15 = Markup('">')
            part16 = Markup("</form>")
            refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
            #add input form and input

            finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)

            if(finalObj.size=="1.5"):
                objArray.append(finalObj)
            if(finalObj.size=="2.5"):
                objArray.append(finalObj)
                
    elif(keyword == "ApartmentsForCouple"):
        refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

        for i in range(len(refobjArray)):
            refObj = refobjArray[i]
            
            #add input form and input
            part1 = Markup('<form method="POST">')
            part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
            part3 = refObj.leaseTitle
            part4 = " By "
            part5 = refObj.email
            part6 = " At "
            part7 = refObj.postedAt
            part8 = Markup('">')
            part9 = Markup('<input type="submit" value="')
            part10 = refObj.leaseTitle
            part11 = " By "
            part12 = refObj.email
            part13 = " At "
            part14 = refObj.postedAt
            part15 = Markup('">')
            part16 = Markup("</form>")
            refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
            #add input form and input

            finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)
        
            objArray.append(finalObj)
 
    elif(keyword == "ApartmentsForFamilyWithKids"):
        refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

        for i in range(len(refobjArray)):
            refObj = refobjArray[i]

            #add input form and input
            part1 = Markup('<form method="POST">')
            part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
            part3 = refObj.leaseTitle
            part4 = " By "
            part5 = refObj.email
            part6 = " At "
            part7 = refObj.postedAt
            part8 = Markup('">')
            part9 = Markup('<input type="submit" value="')
            part10 = refObj.leaseTitle
            part11 = " By "
            part12 = refObj.email
            part13 = " At "
            part14 = refObj.postedAt
            part15 = Markup('">')
            part16 = Markup("</form>")
            refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
            #add input form and input

            finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)

            if(finalObj.size=="3.5"):
                objArray.append(finalObj)
            if(finalObj.size=="4.5"):
                objArray.append(finalObj)
            if(finalObj.size=="5.5"):
                objArray.append(finalObj)
            if(finalObj.size=="Others"):
                objArray.append(finalObj)
            if(finalObj.size=="House"):
                objArray.append(finalObj)
            if(finalObj.size=="Townhouse"):
                objArray.append(finalObj)
    
    elif(keyword == "ApartmentsWithGym"):
        refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

        for i in range(len(refobjArray)):
            refObj = refobjArray[i]

            #add input form and input
            part1 = Markup('<form method="POST">')
            part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
            part3 = refObj.leaseTitle
            part4 = " By "
            part5 = refObj.email
            part6 = " At "
            part7 = refObj.postedAt
            part8 = Markup('">')
            part9 = Markup('<input type="submit" value="')
            part10 = refObj.leaseTitle
            part11 = " By "
            part12 = refObj.email
            part13 = " At "
            part14 = refObj.postedAt
            part15 = Markup('">')
            part16 = Markup("</form>")
            refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
            #add input form and input

            finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)

            gym = "gym"
            descrip = finalObj.description.lower()
            if(gym in descrip):
                objArray.append(finalObj)
        
    elif(keyword == "LuxuryApartmentsPenthouses"):
        refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

        for i in range(len(refobjArray)):
            refObj = refobjArray[i]

            #add input form and input
            part1 = Markup('<form method="POST">')
            part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
            part3 = refObj.leaseTitle
            part4 = " By "
            part5 = refObj.email
            part6 = " At "
            part7 = refObj.postedAt
            part8 = Markup('">')
            part9 = Markup('<input type="submit" value="')
            part10 = refObj.leaseTitle
            part11 = " By "
            part12 = refObj.email
            part13 = " At "
            part14 = refObj.postedAt
            part15 = Markup('">')
            part16 = Markup("</form>")
            refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
            #add input form and input
            
            finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)

            if(finalObj.size=="5.5"):
                objArray.append(finalObj)
            if(finalObj.size=="House"):
                objArray.append(finalObj)
            if(finalObj.size=="Townhouse"):
                objArray.append(finalObj)
    
    elif(keyword == "Townhouses"): 
        refObj = adsObj("leaseTitle", "size", "provinces", "city", "address", "contractLength", "description", "email", "tel", "availability")

        for i in range(len(refobjArray)):
            refObj = refobjArray[i]

            #add input form and input
            part1 = Markup('<form method="POST">')
            part2 = Markup('<input type="hidden" name="apartmentChoice" value="')
            part3 = refObj.leaseTitle
            part4 = " By "
            part5 = refObj.email
            part6 = " At "
            part7 = refObj.postedAt
            part8 = Markup('">')
            part9 = Markup('<input type="submit" value="')
            part10 = refObj.leaseTitle
            part11 = " By "
            part12 = refObj.email
            part13 = " At "
            part14 = refObj.postedAt
            part15 = Markup('">')
            part16 = Markup("</form>")
            refTitle = part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8 + part9 + part10 + part11 + part12 + part13 + part14 + part15 + part16
            #add input form and input
            
            finalObj = adsObj(refTitle, refObj.size, refObj.provinces, refObj.city, refObj.address, refObj.contractLength, refObj.description, refObj.email, refObj.tel, refObj.availability)

            if(finalObj.size=="House"):
                objArray.append(finalObj)
            if(finalObj.size=="Townhouse"):
                objArray.append(finalObj)

    return objArray
# [Search suggested data]

# [In-site keyword search]
#TODO later
# [In-site keyword search]

# [Copy all data to an array]
def getAllData():

    objArray = []

    # [Get the collection]
    docs = db.collection(u'contracts').stream()
    # [Get the collection]

    # [Will be O(n^2) time complexity]
    for doc in docs: # [For each loop to go to the contracts one by one]
        # [Convert the data into right format, ' -> "]
        rawData = (f'{doc.to_dict()}')
        #data = json.loads(rawData)
        listData = list(rawData) #list
        for x in range(len(listData)):
            if(listData[x]=="\'"):
                listData[x]="\""

        modiData = "".join(listData) #string

        jsonData = json.loads(modiData) #dict / json
        # [Convert the data into right format, ' -> "]
        
        # [store it into a ref object]
        refObj = adsObjAlt_WithKey(jsonData["leaseTitle"], jsonData["size"], jsonData["provinces"], jsonData["city"], jsonData["address"], jsonData["contractLength"], jsonData["description"], jsonData["email"], jsonData["tel"], jsonData["availability"], jsonData["by_who"], jsonData["postedAt"])
        # [store it into a ref object]

        # [Store them into an array]
        objArray.append(refObj)
        # [Store them into an array]

    # [Will be O(n^2) time complexity]

    return objArray
# [Copy all data to an array]

# [Upload Images]
def uploadPhoto(userIDStr, file):
    #https://www.programcreek.com/python/example/51528/flask.request.files
    path = 'gs://leasetransfersite.appspot.com'+str(secure_filename(file.filename))
    if file: 
        try:
            bucket = firebase.storage_bucket()
            #file is just an object from request.files e.g. file = request.files['myFile']
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file)
        except Exception as e:
            print('error uploading user photo: ' % e)            
# [Upload Images]


# [abstract table for printing]
class OwnAds(Table):
    id = Col('Id', show=False)
    leaseTitle = Col('Title')
    #leaseTitle = Col(Markup('<a href="/adsDetails">Title</a>'))
    size = Col('Size')
    provinces = Col('Province')
    city = Col('City')
    address = Col('Address')
    contractLength = Col('Contract Length')
    description = Col('Description')
    email = Col('Email')
    tel = Col('Tel')
    availability = Col('Availability')
# [abstract table for printing]


# ==========[Supporting function]==========





# ==========[Make it run]==========
if __name__ == '__main__':
    app.run(debug=True)
# ==========[Make it run]==========
