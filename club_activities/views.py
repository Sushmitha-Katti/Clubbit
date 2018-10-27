from django.shortcuts import render, HttpResponse, redirect, render_to_response 
from club_activities.models import *
from django.contrib.auth import authenticate, login ,logout
from datetime import date

def home(request):
	 if not request.user.is_authenticated:
	 	return render(request, "Home.html")
	 else:
	 	return redirect("/clubs/")

def signout(request):
	logout(request)
	return redirect("/")

def show_clubs(request):
	print(request.user)
	
	mem = 0
	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		if member.type_of_user == 'A':
			mem = 1
		elif member.type_of_user == 'CA':
			mem = 2
	except:
		pass

	if request.method =="POST":

		if request.POST.get('btn') =="Want To Create A Club?" :
			return render(request, "create_form.html")
		if request.POST.get('btn') == "Club Admin Login":
			return render(request,"admin_login.html",{'clubs':clubs})
		if request.POST.get('sub_button') == "submit":
			pass

	clubs = Club.objects.all()
	if clubs.count()>0:
		club = {}
		a = []
		for i, j in enumerate(clubs):
			print(i)
			if((i)%3 != 0 or i ==0):
				a.append (j) 
				print(j)

			else:
				
				print(j)
				club[i]=a
				a = []
				a.append(j)
		club[i]=a
	else:
		club = Club.objects.all()


	



	return render(request, "showclubs.html", {'clubs': clubs,  'mem' : mem, 'club':club}) 



def club_page(request, club_name):
	
	clubs = Club.objects.get(cname = club_name)
	events = Event.objects.filter(club_name = clubs )
	if request.method=="POST":

		if request.POST.get('btn')=='Home':
			return redirect("/clubs/")

		if request.POST.get('btn')=='Club':
			return render(request, "club_page.html", {'clubs':clubs})

		if request.POST.get('btn')=='About':
			return render(request, "about.html", {'clubs':clubs})

		if request.POST.get('btn')=='Events':
			return render(request, "events.html", {'events':events, 'today': date.today()})

		if request.POST.get('btn')=='Gallery':
			gallery = {}
			for e in events:
				g = Gallery.objects.filter(ename = e)
				print(g)
				if g.exists():
					gallery[e.ename] = g

			return render(request, "gallery.html", {'events':events , 'gallery':gallery})

		if request.POST.get('btn')=='joinclub':
			profile = Profile.objects.get(user=request.user)
			request = Request(member=profile, club = clubs)
			request.save()

			return HttpResponse("Requested to join the club")
		for event in events:
			register = 'Register for ' + event.ename
			print(register)
			if request.POST.get('sub_btn') == register:
				profile = Profile.objects.get(user=request.user)
				event = Event.objects.get(ename = event.ename)
				registered = Registered_members(ename = event, details = profile)
				registered.save()
				return HttpResponse("Successfully registerd to event")

	
	clubs = Club.objects.get(cname = club_name)
	events = Event.objects.filter(club_name = clubs )
	return render(request, "club_page.html", {'clubs':clubs, 'events' : events})



def admin_login(request):

	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		
		
	except : 
			return HttpResponse(" Sorry Only college admin can login")

	if member.type_of_user != 'A' or not request.user.is_authenticated :
			return HttpResponse("Only admin can login")


	
	events = Event.objects.filter(club_name = member.club)
	req = Request.objects.filter(club = member.club)
	profile = Profile.objects.get(user = request.user)
	member = Member.objects.get(profile = profile)
	req = Request.objects.filter(club = member.club)
	club = member.club

	return render(request, "admin_page.html",{'events' : events ,'today': date.today(), 'club': club})



def see_response(request):
	if request.method == 'POST':
		print(f'Hello{request.POST.get("sub_button")}')

		


		if request.POST.get('sub_button') == 'Save' or  request.POST.get('sub_button') == 'Save and Add Another':
			name = request.POST.get('name')
			usn = request.POST.get('usn')
			phone = request.POST.get('phone')
			branch = request.POST.get('branch')
			sem = request.POST.get('sem')
			members = Club_members(name = name, usn = usn, phone = phone , branch = branch, sem = sem)
			members.save()
			if request.POST.get('sub_button') == 'Save':
				return redirect('/adminlogin/')

			if request.POST.get('sub_button') == 'Save and Add Another':
				return render(request, 'add_members.html')

		

		

def signin(request):
	correct = 1
	if request.method == 'POST':
		user = request.POST.get('user')
		password = request.POST.get('password')
		
		user = authenticate(request, username=user, password=password)
		if user is not None:
			print(user)
			login(request, user)
			return redirect("/clubs/")
		else:
			correct = 0
			return render(request, 'signin.html', {'correct' : correct})

	return render(request, 'signin.html', {'correct' : correct})

def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username',None)
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		usn = request.POST.get('usn',None)
		if User.objects.filter(username=username).exists():
			return HttpResponse('User already exists')
		else:
			user = User.objects.create_user(username, email, password)
			user.save()
			profile = Profile(user = user, usn = usn)
			profile.save()
			login(request, user)
			return redirect("/clubs/")
			
		
	return render(request, "signup.html")

def profile(request):

	profile = Profile.objects.get(user = request.user)

	if request.method == "POST":
		profile.fname = request.POST.get('fname')
		profile.lname = request.POST.get('lname')
		profile.phone = request.POST.get('phone')
		profile.usn = request.POST.get('usn')
		profile.college = request.POST.get('college')
		profile.branch = request.POST.get('branch')
		profile.sem = request.POST.get('sem')
		profile.user = User.objects.get(username = request.user)
		profile.save()
		return HttpResponse("Success")



	return render(request, "profile.html", {'profile' : profile})

	
def cadmin(request):
	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		
		
	except : 
			return HttpResponse(" Sorry Only college admin can login")

	if member.type_of_user != 'CA' or not request.user.is_authenticated :
			return HttpResponse("Only college admin can login")


	club_request = Club_request.objects.all()
	if request.method == 'POST':
		for i in club_request:
			print(f"hello{i.profile.usn}")
			print(f"m{request.POST.get('reject')}")
			print(f"m{request.POST.get('reject')}")
			if request.POST.get('add') == i.profile.usn:
				print("yes")
				club = Club.objects.create(cname = i.club_name,mission = i.mission, vision = i.vision, about = i.desc)
				print("Hello")
				try :
					mem = Member.objects.get( profile = Profile.objects.get(usn =i.profile.usn))
					mem.type_of_user = 'A'
				except : 
					mem = Member.objects.create(profile = Profile.objects.get(usn =i.profile.usn), type_of_user = 'A', club = Club.objects.get(cname= i.club_name)  )
				Club_request.objects.get(profile=Profile.objects.get(usn = i.profile.usn)).delete()
				return redirect("/collegeadmin/")

			if request.POST.get('reject') == i.profile.usn:
				print("Yes")
				Club_request.objects.get(profile=Profile.objects.get(usn = i.profile.usn)).delete()
				return redirect("/collegeadmin/")
	club_request = Club_request.objects.all()
	if club_request.count() > 0:
		re = 1;
	else :
		re = 0;
	return render(request, 'cadmin.html', {'cr':club_request, 're':re})

def add_events(request,club_name):
	club = Club.objects.get(cname = club_name)
	if request.POST.get('sub_button') == 'Add':
			name = request.POST.get('event_name')
			desc = request.POST.get('desc')
			date = request.POST.get('date')
			fees = request.POST.get('fees')
			image = request.FILES.get('image')
			print(request.user)
			profile = Profile.objects.get(user = request.user)
			member = Member.objects.get(profile = profile)
			event = Event(ename = name, desc = desc, image = image, fees = fees, date = date, club_name =club)
			event.save()
			return redirect('/adminlogin/')

	return render(request, "add_events.html" )

def edit_club(request,club_name):
	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		if member.type_of_user != 'A' or not request.user.is_authenticated:
			return HttpResponse("Sorry Only club  admin can access this page ")
	except : 
		if not request.user.is_authenticated:
			return HttpResponse(" Sorry Only club  admin can access this page ")

	club = Club.objects.get(cname = member.club)
	if request.POST.get('sub_button') == 'Update':
			profile = Profile.objects.get(user = request.user)
			member = Member.objects.get(profile = profile)
			club = Club.objects.get(cname = member.club)
			club.cname = request.POST.get('cname')
			club.motto = request.POST.get('motto')
			image = request.FILES.get('image')
			if not image is None:
				club.image = image
			club.about = request.POST.get('about')
			club.mission = request.POST.get('mission')
			club.vission = request.POST.get('vision')
			club.shortdesc = request.POST.get('short')
			club.phone = request.POST.get('phone')
			club.mail = request.POST.get('mail')
			club.save()
			return HttpResponse("Successfully upated")

	return render(request, "cdetail.html", {'club' : club})

def addimg(request, club_name):
	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		if member.type_of_user != 'A' or not request.user.is_authenticated:
			return HttpResponse("Sorry Only club  admin can access this page ")
	except : 
		if not request.user.is_authenticated:
			return HttpResponse(" Sorry Only club  admin can access this page ")
	profile = Profile.objects.get(user = request.user)
	member = Member.objects.get(profile = profile)
	events = Event.objects.filter(club_name = member.club)

	if request.POST.get('btn') == 'Save and Add Another' or request.POST.get('btn') == 'Save':
			image = request.FILES.get('image')
			event = Event.objects.get(ename = request.POST.get('ename'))
			gallery = Gallery(ename = event, images = image)
			gallery.save()

			if request.POST.get('btn') == 'Save and Add Another':
				event = Event.objects.get(ename = request.POST.get('ename')) 
				events = Event.objects.filter(club_name = event.club_name)

				return render(request, 'add_photos.html', {'events':events})

			if request.POST.get('btn') == 'Save':
				return redirect('/adminlogin/')
	return render(request, "add_photos.html",{'events':events})

def joinr(request, club_name):
	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		if member.type_of_user != 'A' or not request.user.is_authenticated:
			return HttpResponse("Sorry Only club  admin can access this page ")
	except : 
		if not request.user.is_authenticated:
			return HttpResponse(" Sorry Only club  admin can access this page ")

	profile = Profile.objects.get(user = request.user)
	member = Member.objects.get(profile = profile)
	req = Request.objects.filter(club = member.club)
	if request.method == 'POST':
		for i in req:
			print(f"hello{i.member.usn}")
			print(f"m{request.POST.get('reject')}")
			if request.POST.get('add') == i.member.usn:
				print("yes")
				mem = Member(profile = i.member, club = i.club)
				mem = mem.save()
				Request.objects.get(member=Profile.objects.get(usn = i.member.usn)).delete()
				return redirect("/adminlogin/")

			if request.POST.get('reject') == i.member.usn:
				print("Yes")
				Request.objects.get(member= Profile.objects.get(usn = i.member.usn)).delete()
				return redirect("/adminlogin/")
	if req.count()>0:
		re = 1
	else :
		re = 0
	return render(request, "see_requests.html", {'req':req, 're':re})
	
def regmem(request, club_name):

	try:
		profile = Profile.objects.get(user = request.user)
		member = Member.objects.get(profile = profile)
		if member.type_of_user != 'A' or not request.user.is_authenticated:
			return HttpResponse("Sorry Only club  admin can access this page ")
	except : 
		if not request.user.is_authenticated:
			return HttpResponse(" Sorry Only club  admin can access this page ")


	profile = Profile.objects.get(user = request.user)
	member = Member.objects.get(profile = profile)
	events = Event.objects.filter(club_name = member.club)


	
	ereg = {}
	for e in events:
		if e.date>=date.today():
			g = Registered_members.objects.filter(ename=e)
			if g.exists():
				ereg[e.ename] = g




	return render(request, "registered_participants.html", {'reg':ereg})

def sel(request, club_name):
	return render(request, "sel.html")


def add_admin(request, club_name):
	club = Club.objects.get(cname = club_name)
	member = Member.objects.filter(club = club)
	if request.method == 'POST':
		usn = request.POST.get('usn')
		mem = Member.objects.get(profile = Profile.objects.get(usn = usn))
		mem.club = Club.objects.get(cname = club_name)
		mem.type_of_user = 'A'
		mem.save()
		return redirect("/adminlogin/")

	
	return render(request, "add_admin.html", {'member':member})

def cform(request):
	if request.method == "POST":
		cname = request.POST.get('cname')
		mission = request.POST.get('mission')
		vision = request.POST.get('vision')
		about = request.POST.get('about')
		usn = request.POST.get('usn')

		try :
			club = Club.objects.get(cname = cname) 
			if club.count > 0:
				return HttpResponse("Sorry club already exists, try another name!!!")
		except : 
			pass
		cr = Club_request(club_name=cname, mission = mission, vision = vision, desc = about, profile = Profile.objects.get(usn = usn))
		cr.save()
		return HttpResponse("Request sent")



	return render(request, "create_form.html")