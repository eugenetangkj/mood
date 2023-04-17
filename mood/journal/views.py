from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Entry

import pyperclip

# Login/register
def index(request):
 
    return render(request, "journal/index.html")


# Login page
def login_view(request):
    # User visits via POST. Means user enter login details already
    if (request.method == "POST"):
        # Attempt to sign the user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home", kwargs={"criteria": "all"}))
        # Authentication is not successful
        else:
            return render(request, "journal/login.html", {
                "message": "Invalid username and/or password."
            })

    # User visits via GET request. Means user wants to enter login details
    else:
        return render(request, "journal/login.html")
        
# Logout page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



# Register page
def register(request):
    # User visits via POST. Means user enter registration details already
    if (request.method == "POST"):
        # Get user details
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        # Password does not match, return error message
        if password != confirmation:
            return render(request, "journal/register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "journal/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home", kwargs={"criteria": "all"}))
    
    # User visits via GET. Means user wants to enter registration details
    else:
        return render(request, "journal/register.html")



# Home page, displays relevant entries
def home(request, criteria):
    # User is authenticated
    if request.user.is_authenticated:
        # Case 1: View all posts
        if criteria == "all":
            entries_list = Entry.objects.filter(owner=request.user).order_by("-date") 
        # Case 2: View today's posts       
        elif criteria == "today":
            entries_list = Entry.objects.filter(owner=request.user).filter(date__gte=timezone.now() - timedelta(days=1), date__lte=timezone.now()).order_by("-date")
        # Case 3: View all posts within the week
        elif criteria == "week":
            entries_list = Entry.objects.filter(owner=request.user).filter(date__gte=timezone.now() - timedelta(weeks=1), date__lte=timezone.now()).order_by("-date")
        # Case 4: View all posts within the month
        else:
            entries_list = Entry.objects.filter(owner=request.user).filter(date__gte=timezone.now() - relativedelta(months=+1), date__lte=timezone.now()).order_by("-date")



        paginator = Paginator(entries_list, 5) # Shows 5 entries per page
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, "journal/home.html", {
            'page_object': page_object,
            'filtertype': criteria
        })
    
    # User is not authenticated
    else:
        return HttpResponseRedirect(reverse("index"))


# Create page, creates a new entry
def create(request):
    # User is authenticated
    if request.user.is_authenticated:
        # Came to this page via a POST request
        if (request.method == "POST"):
            # Take in the data that the user submitted
            title = request.POST["entry_title"]
            body = request.POST["entry_body"]
            emotion = request.POST["emotion"]
            uploaded_image = request.FILES['img']
            file_system_storage = FileSystemStorage()
            file = file_system_storage.save(uploaded_image.name, uploaded_image)
            file_url = file_system_storage.url(file)

            # Create a new entry based on user's input
            new_entry = Entry(owner=request.user, entry_title=title, entry_body=body, emotion=emotion, image=file_url)
            new_entry.save()
            return HttpResponseRedirect(reverse("view", kwargs={"entry_number": new_entry.id}))
        # Came to this page via a GET request
        else:
            return render(request, "journal/create.html")
    
    # User is not authenticated.
    else:
        return HttpResponseRedirect(reverse("index"))
    
# View entry
def view(request, entry_number):
    # User is authenticated
    if request.user.is_authenticated:
        # Attempt to get relevant entry
        try:
            selected_entry = Entry.objects.get(id=entry_number)
        except Entry.DoesNotExist:
            return HttpResponseRedirect(reverse("home", kwargs={"criteria": "all"}))

        # Relevant entry exist. Check if entry belongs to the user
        if selected_entry.owner != request.user:
            return HttpResponseRedirect(reverse("home", kwargs={"criteria": "all"}))

    
        # Relevant entry exist and entry belongs to the user. Can go ahead with viewing.
        return render(request, "journal/view.html", {
            "selected_entry": selected_entry
        })
          
        
    
    # User is not authenticated    
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt
# Copy entry to clipboard
def copy(request, entry_number):
    # User is authenticated
    if request.user.is_authenticated:
        # Attempt to get relevant entry
        try:
            selected_entry = Entry.objects.get(id=entry_number)
        except Entry.DoesNotExist:
            return HttpResponseRedirect(reverse("home", kwargs={"criteria": "all"}))

        # Relevant entry exist. Check if entry belongs to the user
        if selected_entry.owner != request.user:
            return HttpResponseRedirect(reverse("home", kwargs={"criteria": "all"}))

        date_string = selected_entry.date.strftime("%m/%d/%Y %H:%M:%S")




        journalEntry = "Title:\n" + selected_entry.entry_title + "\n" + "Date:\n" + date_string + "\n" + "Body:\n" + selected_entry.entry_body
        pyperclip.copy(journalEntry)
        return HttpResponse(status=204) 
    
    # User is not authenticated    
    else:
        return HttpResponseRedirect(reverse("index"))

# Updates content of an entry
def update_entry(request, entry_number):
    # User is authenticated
    if request.user.is_authenticated:
        # Came to this page via a POST request
        if (request.method == "POST"):
            current_entry = Entry.objects.all().filter(id=entry_number)[0]

            # Update title, body and emotion
            title = request.POST["entry_title"]
            body = request.POST["entry_body"]
            emotion = request.POST["emotion"]
            current_entry.entry_title = title
            current_entry.entry_body = body
            current_entry.emotion = emotion

            # Check whether got new image that has been uploaded
            if 'img' in request.FILES:
                uploaded_image = request.FILES['img']
                file_system_storage = FileSystemStorage()
                file = file_system_storage.save(uploaded_image.name, uploaded_image)
                file_url = file_system_storage.url(file)
                current_entry.image = file_url

            # Save entry
            current_entry.save()
            return HttpResponseRedirect(reverse("view", kwargs={"entry_number": entry_number}))
        # Came to this page via a GET request
        else:
            return HttpResponseRedirect(reverse("view", kwargs={"entry_number": entry_number}))
    
    # User is not authenticated.
    else:
        return HttpResponseRedirect(reverse("index"))
    
@csrf_exempt
# Deletes an entry
def delete_entry(request, entry_number):
    # User is authenticated
    if request.user.is_authenticated:
        # Came to this page via a POST request
        if (request.method == "POST"):
            # Delete the selected entry
            current_entry = Entry.objects.all().filter(id=entry_number)[0]
            current_entry.delete()
            return HttpResponse(status=204)
        # Came to this page via a GET request
        else:
            return HttpResponseRedirect(reverse("view", kwargs={"entry_number": entry_number}))
    
    # User is not authenticated.
    else:
        return HttpResponseRedirect(reverse("index"))

@csrf_exempt 
# Provides the meditate interface
def meditate(request):
    # User is authenticated
    if request.user.is_authenticated:
        # Update the meditation count
        if request.method == "PUT":
            new_meditation_count = request.user.number_of_meditations + 1
            request.user.number_of_meditations = new_meditation_count
            request.user.save()
            return JsonResponse(request.user.serialize())
        # GET request. Simply return default view of meditation page
        else:
            return render(request, "journal/meditate.html")
        
    
    # User is not authenticated
    else:
        return HttpResponseRedirect(reverse("index"))
    

# Provides the profile page
def profile(request):
    # User is authenticated
    if request.user.is_authenticated:
        return render(request, "journal/profile.html")
        
    
    # User is not authenticated
    else:
        return HttpResponseRedirect(reverse("index"))
    
# Gets the emotions count
def emotions(request):
    # User is authenticated
    if request.user.is_authenticated:
        happiness_count = len(Entry.objects.filter(owner=request.user).filter(emotion="happy"))
        surprised_count = len(Entry.objects.filter(owner=request.user).filter(emotion="surprised"))
        sad_count = len(Entry.objects.filter(owner=request.user).filter(emotion="sad"))
        angry_count = len(Entry.objects.filter(owner=request.user).filter(emotion="angry"))

        return JsonResponse({
            "happiness_count": happiness_count,
            "surprised_count": surprised_count,
            "sad_count":sad_count,
            "angry_count": angry_count
        })
        
    
    # User is not authenticated
    else:
        return HttpResponseRedirect(reverse("index"))
    
