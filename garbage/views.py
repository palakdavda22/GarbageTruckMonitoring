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
def signIn(request):
	return render(request, "sign.html")
def postsign(request):
	email=request.POST.get('email')
	passw = request.POST.get("pass")
	try:
		user = authe.sign_in_with_email_and_password(email,passw)
	except:
		message="invalid credentials"
		return render(request,"signIn.html",{"messg":message})
	print(user['idToken'])
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request, "welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request,'sign.html')



