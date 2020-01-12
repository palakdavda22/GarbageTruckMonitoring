from __future__ import division
from __future__ import print_function
from django.shortcuts import render
from django.contrib import auth
import requests
import json
import urllib.request
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

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
    id = int(request.POST.get('binId'))
    lat = (request.POST.get('lat'))
    lon =(request.POST.get('lon'))

    print(id)
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
    # name = database.child('users').child(id).child('details').child('name').get().val()
    bins = database.child('Bin').get().val()
    print(bins)
    name = "vinal"
    return render(request,'welcome.html', {'e':name})


def create_vehicle(request):
    return render(request, 'CreateVehicle.html')


def post_create_vehicle(request):
    vehicle_no = request.POST.get('vehicleNo')
    capacity = int(request.POST.get('capacity'))
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    data = {
        'capacity': capacity
    }
    database.child('Vehicle').child(vehicle_no).set(data)
    print(database.child('Vehicle').get().val())
    name = "vinal"
    return render(request, 'welcome.html', {'e': name})


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

def check_queries(request):
    citizendetails = database.child('Citizen').get().val()
    citizen_details=[]
    for i in citizendetails:

        citizen_details.append(i)

    citizen_details.sort(reverse=True)
    
    address = []
    image = []
    name = []
    query = []
    
    for i in citizen_details:

        addr=database.child('Citizen').child(i).child('address').get().val()
        address.append(addr)
        img=database.child('Citizen').child(i).child('image').get().val()
        image.append(img)
        que=database.child('Citizen').child(i).child('query').get().val()
        query.append(que)
        n=database.child('Citizen').child(i).child('name').get().val()
        name.append(n)

    
    comb_lis_query = zip(name,address,query,image)

   
    return render(request,'checkQueries.html',{'comb_lis_query':comb_lis_query,'e':"Palak"})

def create_distance_matrix(data):
    addresses = data["addresses"]
    API_key = data["API_key"]
    # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
    max_elements = 100
    num_addresses = len(addresses) # 16 in this example.
    # Maximum number of rows that can be computed per request (6 in this example).
    max_rows = max_elements // num_addresses
    # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
    q, r = divmod(num_addresses, max_rows)
    dest_addresses = addresses
    distance_matrix = []
    # Send q requests, returning max_rows rows per request.
    for i in range(q):
        origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    # Get the remaining remaining r rows, if necessary.
    if r > 0:
        origin_addresses = addresses[q * max_rows: q * max_rows + r]
        response = send_request(origin_addresses, dest_addresses, API_key)
        distance_matrix += build_distance_matrix(response)
    return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
    def build_address_str(addresses):
    # Build a pipe-separated string of addresses
        address_str = ''
        for i in range(len(addresses) - 1):
            address_str += addresses[i] + '|'
        address_str += addresses[-1]
        return address_str

    request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    origin_address_str = build_address_str(origin_addresses)
    dest_address_str = build_address_str(dest_addresses)
    request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)
    return response

def build_distance_matrix(response):
    distance_matrix = []
    for row in response['rows']:
        row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
        distance_matrix.append(row_list)
    return distance_matrix

def get_routes(manager, routing, solution, num_routes):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(num_routes):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
#     print(routes)
    return routes

def get_vehicle_capacities():
    vehicles = database.child('Vehicle').get().val()
    print(vehicles)
    vehicle_cap = []
    vehicle_key = []
    for i in vehicles:
        vehicle_cap.append(vehicles[i]['capacity'])
        vehicle_key.append(i)
    return vehicle_cap,vehicle_key

def get_bin_cap():
    bins = database.child('Bin').get().val()
    print(bins)
    bin_cap = []
    vehicle_key = []
    for i in bins:
        bin_cap.append(bins[i]['capacity'])
    print(bin_cap)
    return bin_cap

def get_bin_address():
    bin_addr = []
    bins = database.child('Bin').get().val()
    print(bins)
    for i in bins:
        s = ""
        s = str(bins[i]['latitude'])+","+str(bins[i]['longitude'])
        bin_addr.append(s)
    print(bin_addr)
    return bin_addr

def generate_routes(request):
    data = {}
    data['API_key'] = 'AIzaSyA3W-x4zqHwfCJ2xgzLvuO1MVPlWwp_XJI'
    # data['addresses'] = ['19.312251,72.8513579',  # depot
    #                      '19.3844215,72.8221597',
    #                      '19.3084312,72.8489729',
    #                      '19.3834291,72.8280696',
    #                      '19.3834291,72.8280696',
    #                      '19.2813741,72.8559049',
    #                      '19.2813741,72.8559049',
    #                      '19.2813741,72.8559049',
    #                      '19.2864772,72.8486726',
    #                      '19.2794676,72.8775643',
    #                      '19.3726195,72.8255362',
    #                      '19.3726195,72.8255362',
    #                      '19.3726195,72.8255362',
    #                      '19.3720507,72.8268628',
    #                      '19.3720507,72.8268628',
    #                      '19.3720419,72.8268988',
    #                      ]
    data['addresses'] = get_bin_address()
    """Solve the CVRP problem."""

    """Stores the data for the problem."""
    datap = {}
    # datap['distance_matrix'] = create_distance_matrix(data)
    datap['distance_matrix'] = [
        [0, 31895, 878, 31603, 31603, 5342, 5342, 5342, 3010, 5834, 33590, 33590, 33590, 33821, 33821, 33821],
        [32453, 0, 32024, 999, 999, 29059, 29059, 29059, 31272, 26481, 2985, 2985, 2985, 3217, 3217, 3217],
        [878, 32094, 0, 31803, 31803, 4913, 4913, 4913, 2581, 6033, 33789, 33789, 33789, 34020, 34020, 34020],
        [32453, 1359, 32023, 0, 0, 29058, 29058, 29058, 31271, 26480, 1986, 1986, 1986, 2218, 2218, 2218],
        [32453, 1359, 32023, 0, 0, 29058, 29058, 29058, 31271, 26480, 1986, 1986, 1986, 2218, 2218, 2218],
        [5258, 29590, 4828, 29298, 29298, 0, 0, 0, 4076, 3026, 31285, 31285, 31285, 31516, 31516, 31516],
        [5258, 29590, 4828, 29298, 29298, 0, 0, 0, 4076, 3026, 31285, 31285, 31285, 31516, 31516, 31516],
        [5258, 29590, 4828, 29298, 29298, 0, 0, 0, 4076, 3026, 31285, 31285, 31285, 31516, 31516, 31516],
        [3481, 31233, 3052, 30942, 30942, 4052, 4052, 4052, 0, 5172, 32928, 32928, 32928, 33160, 33160, 33160],
        [5972, 26678, 5543, 26387, 26387, 2577, 2577, 2577, 4791, 0, 28373, 28373, 28373, 28605, 28605, 28605],
        [34313, 2611, 33883, 2294, 2294, 30918, 30918, 30918, 33131, 28340, 0, 0, 0, 511, 511, 511],
        [34313, 2611, 33883, 2294, 2294, 30918, 30918, 30918, 33131, 28340, 0, 0, 0, 511, 511, 511],
        [34313, 2611, 33883, 2294, 2294, 30918, 30918, 30918, 33131, 28340, 0, 0, 0, 511, 511, 511],
        [34219, 2517, 33789, 2200, 2200, 30824, 30824, 30824, 33037, 28247, 511, 511, 511, 0, 0, 0],
        [34219, 2517, 33789, 2200, 2200, 30824, 30824, 30824, 33037, 28247, 511, 511, 511, 0, 0, 0],
        [34219, 2517, 33789, 2200, 2200, 30824, 30824, 30824, 33037, 28247, 511, 511, 511, 0, 0, 0],
    ]
    # datap['demands'] = [0, 1, 1, 4, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    datap['demands'] = get_bin_cap()
    datap['vehicle_capacities'],datap['vehicle_key'] = get_vehicle_capacities()
    datap['num_vehicles'] = len(datap['vehicle_capacities'])
    datap['depot'] = 0


    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(datap['distance_matrix']),
                                           datap['num_vehicles'], datap['depot'])

    print(datap['distance_matrix'][1][1])
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    #     print(routing)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return datap['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return datap['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        datap['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    #     solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        #         print_solution(data, manager, routing, assignment)
        routes = get_routes(manager, routing, assignment, datap['num_vehicles'])
        # Display the routes.
        Routes = []
        for i, route in enumerate(routes):
            # print('Route', i, route)
            Route = []
            for j in range(len(route)):
                Route.append(data['addresses'][route[j]].split(","))
            Routes.append(Route)
        print(Routes)

    vehicle_route = dict()
    j = 0
    for i in datap['vehicle_key']:
        vehicle_route[i] = Routes[j]
        d =  dict()
        for k in range(len(Routes[j])):
            lat= Routes[j][k][0]
            long = Routes[j][k][1]
            d[k] = {
                "latitude": lat,
                "longitude": long
            }
        print(d)
        database.child('Route').child(i).set(d)
        j = j+1
    print(vehicle_route)

    return render(request,'generatedRoutes.html')