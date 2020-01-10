from django.shortcuts import render
from django.contrib import auth



import pyrebase


config = {
	'apiKey': "AIzaSyB6s7DSe9M6MZk7g77cMTuoqIO6d-ebKwI",
    'authDomain' : "garbage-truck-monitoring.firebaseapp.com",
    'databaseURL' : "https://garbage-truck-monitoring.firebaseio.com",
    'projectId' : "garbage-truck-monitoring",
    'storageBucket' : "garbage-truck-monitoring.appspot.com",
    'messagingSenderId' : "549306067582",
    'appId' : "1:549306067582:web:bbaeac9ec829045099c62f",
    'measurementId' : "G-X9JCRW3TR0"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

def signIn(request):
	return render(request, "sign.html")
def postsign(request):
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	try:
		user = authe.sign_in_with_email_and_password(email,passw)
	except:
		message="invalid credentials"
		return render(request,"sign.html",{"messg":message})
	print(user['idToken'])
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'sign.html')



def create_bin(request):

    return render(request,'CreateBin.html')

def post_create_bin(request):

    
    lat = request.POST.get('lat')
    lon =request.POST.get('lon')
    id = str(lat) + str(lon)
    print(type(lat))
    capacity = request.POST.get('capacity')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

   
    data = {
        "latitude":lat,
        'longitude':lon,
		'capcity':capacity
    }
    database.child('Bin').child(id).set(data)
    name = database.child('users').child(id).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})


def create_driver(request):
	return render(request, 'CreateDriver.html')

def post_create_driver(request):
	name = request.POST.get('name')
	age =request.POST.get('age')
	address =request.POST.get('address')
	gender =request.POST.get('gender')
	date =request.POST.get('joiningdate')
	aadhar = str(name) + str(date)
	
	idtoken= request.session['uid']
	a = authe.get_account_info(idtoken)
	a = a['users']
	a = a[0]
	a = a['localId']

   
	data = {
        "name":name,
        'age':age,
		'gender': gender,
		'address':address,
		'joining date': date
    }
	database.child('Driver').child(aadhar).set(data)
	name = database.child('users').child(id).child('details').child('name').get().val()
	return render(request,'welcome.html', {'e':name})


def check(request):
   
# --------------------------Driver
    timestamps = database.child('Driver').get().val()
    lis_time=[]
    for i in timestamps:

        lis_time.append(i)

    lis_time.sort(reverse=True)
    print("hello")
    print(lis_time)
    address = []
    age = []
    gender = []
    date = []
    name = []
    for i in lis_time:

        n=database.child('Driver').child(i).child('name').get().val()
        name.append(n)
        ag=database.child('Driver').child(i).child('age').get().val()
        age.append(ag)
        addr=database.child('Driver').child(i).child('address').get().val()
        address.append(addr)
        gen=database.child('Driver').child(i).child('gender').get().val()
        gender.append(gen)
        da=database.child('Driver').child(i).child('joining date').get().val()
        date.append(da)

    print(name)
    print(address)
    print(age)
    print(gender)
    print(date)
    

    comb_lis = zip(name,address,age,gender,date)

	# -------------------------Bin
    bindetails = database.child('Bin').get().val()
    bin_details=[]
    for i in bindetails:

        bin_details.append(i)

    bin_details.sort(reverse=True)
    
    latitude = []
    longitude = []
    capacity = []
    
    for i in bin_details:

        lat=database.child('Bin').child(i).child('latitude').get().val()
        latitude.append(lat)
        lon=database.child('Bin').child(i).child('longitude').get().val()
        longitude.append(lon)
        
        cap=database.child('Bin').child(i).child('capacity').get().val()
        capacity.append(cap)

    
    comb_lis_bin = zip(latitude,longitude,capacity)

   
    return render(request,'check.html',{'comb_lis':comb_lis,'comb_lis_bin':comb_lis_bin,'e':"Palak"})
