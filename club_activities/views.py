from django.shortcuts import render, HttpResponse, redirect 
from club_activities.models import *
from django.contrib.auth import authenticate, login ,logout


def home(request):
	print(request.user)
	if not request.user.is_authenticated:
		return render(request, 'home.html')
	else :
		return redirect(f"/clubs/")

def show_clubs(request):
	

	
	if request.method =="POST":

		if request.POST.get('btn') =="clubs" :
			return redirect(f"/signin/")
		if request.POST.get('btn') =="profile" :
			return redirect(f"/profile/")
		if request.POST.get('btn') =="logout" :
			logout(request)
			return HttpResponse("Successfully LoggedOut")


		if request.POST.get('btn') =="Want To Create A Club?" :
			return render(request, "create_form.html")
		if request.POST.get('btn') == "Club Admin Login":
			return render(request,"admin_login.html",{'clubs':clubs})
		if request.Post.get('sub_button') == "submit":
			pass

	clubs = Club.objects.all()
	print(clubs)
	return render(request, "showclubs.html", {'clubs': clubs}) 



def club_page(request, club_name):
	
	clubs = Club.objects.get(cname = club_name)
	events = Event.objects.filter(club_name = clubs)
	if request.method=="POST":

		if request.POST.get('btn')=='Home':
			return render(request, "club_page.html", {'clubs':clubs})

		if request.POST.get('btn')=='About':
			return render(request, "about.html", {'clubs':clubs})

		if request.POST.get('btn')=='Events':
			return render(request, "events.html", {'events':events})

		if request.POST.get('btn')=='Gallery':
			gallery = {}
			for e in events:
				g = Gallery.objects.filter(ename = e)
				gallery[e.ename] = g
				print(gallery)

			return render(request, "gallery.html", {'events':events , 'gallery':gallery})

		if request.POST.get('btn')=='Join Club':
			pass
	return render(request, "club_page.html", {'clubs':clubs })



def admin_login(request):
	if request.method == 'POST':
		if request.POST.get('btn') == 'Add Members':
			return render(request, "add_members.html")

		if request.POST.get('btn') == 'Add Events':
			clubs = Club.objects.all()
			return render(request, "add_events.html", {'clubs':clubs})

		if request.POST.get('btn') == 'Requests':
			return render(request, "see_requests.html")

		if request.POST.get('btn') == 'Participants Registered':
			return render(request, "registered_participants.html")

		if request.POST.get('btn') == 'Add Images':
			club_name = request.POST.get('cname')
			club = Club.objects.get(cname = club_name)
			events = Event.objects.filter(club_name = club)
			return render(request, "add_photos.html",{'events':events})
	clubs = Club.objects.all()
	return render(request, "admin_page.html",{'clubs' : clubs})



def see_response(request):
	if request.method == 'POST':
		if request.POST.get('sub_button') == 'Save' or  request.POST.get('sub_button') == 'Save and Add Another':
			name = request.POST.get('name')
			usn = request.POST.get('usn')
			phone = request.POST.get('phone')
			branch = request.POST.get('branch')
			sem = request.POST.get('sem')
			members = Club_members(name = name, usn = usn, phone = phone , branch = branch, sem = sem)
			members.save()
			if request.POST.get('sub_button') == 'Save':
				return render(request, 'admin_page.html')

			if request.POST.get('sub_button') == 'Save and Add Another':
				return render(request, 'add_members.html')

		if request.POST.get('sub_button') == 'Add':
			name = request.POST.get('event_name')
			desc = request.POST.get('desc')
			date = request.POST.get('date')
			fees = request.POST.get('fees')
			image = request.FILES.get('image')
			cname = request.POST.get('cname')
			print(cname)
			club = Club.objects.get(cname = cname)
			print(club)

			event = Event(ename = name, desc = desc, image = image, fees = fees, date = date, club_name =club)
			event.save()
			return render(request, 'admin_page.html')

		if request.POST.get('btn') == 'Save and Add Another' or request.POST.get('btn') == 'Save':
			image = request.FILES.get('image')
			event = Event.objects.get(ename = request.POST.get('ename'))
			gallery = Gallery(ename = event, images = image)
			gallery.save()
			if request.POST.get('btn') == 'Save and Add Another':
				event = Event.objects.get(ename = request.POST.get('ename')) 
				events = Event.objects.filter(club_name = event.club_name)

				return render(request, 'add_photos.html', {'events':events} )

			if request.POST.get('btn') == 'Save':
				clubs = Club.objects.all()
				return render(request, 'admin_page.html', {'clubs' : clubs})

def signin(request):
	if request.method == 'POST':
		user = request.POST.get('user')
		password = request.POST.get('password')
		
		user = authenticate(request, username=user, password=password)
		if user is not None:
			login(request, user)
			clubs = Club.objects.all()
			return render(request, 'showclubs.html', {'clubs':clubs})

	return render(request, 'signin.html')

def signup(request):
	if request.method == 'POST':
		username = request.POST.get('username',None)
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		if User.objects.filter(username=username).exists():
			return HttpResponse('User already exists')
		else:
			user = User.objects.create_user(username, email, password)
			user.save()
			login(request, user)
			clubs = Club.objects.all()
			return render(request, 'showclubs.html', {'clubs' : clubs})
		
	return render(request, "signup.html")

def profile(request):
	if request.method == "POST":
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		phone = request.POST.get('phone')
		usn = request.POST.get('usn')
		college = request.POST.get('college')
		branch = request.POST.get('branch')
		sem = request.POST.get('sem')
		user = User.objects.get(username = request.user)
		print(fname)
		print(user)
		profile = Profile(user = user, fname = fname, lname = lname, phone = phone, usn = usn, college = college, branch =branch, sem = sem)
		profile.save()
		return HttpResponse("Success")



	return render(request, "profile.html")

	
