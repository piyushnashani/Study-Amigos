from http.client import HTTPResponse
from ssl import _create_default_https_context
from wsgiref.util import request_uri
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import Myusercreationform
from django.contrib.auth.decorators import login_required
##from django.contrib.auth.models import User                           ##Because we imported our own user from models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Roomform, Userform
from django.db.models import Q                                          ## basically imported for the search functionality for 'and-&' and 'or-|'

# Create your views here.

##rooms 

rooms=[
    {'id': 1, 'name': 'let\'s learn python'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend developers'},
]

def Loginpage(request):
    page='login'
    if request.user.is_authenticated:                                   ## if user is already logged in then he should not go the login page as he shoud first logout.
        return redirect('home')
    if request.method== 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)                    ##if user doesnot exist
        except:
            messages.error(request, 'User does not exist')              ## for showing it we print all the messages left in our main file and that will run smooth as we want whenever to display messages because each page consist of the main.html file and whenever there are messages left it will show up there
        
        user=authenticate(request, email=email, password=password)  ##makes sure that whatever user unputs we give are correct or not.
        if user is not None:
            login(request, user)
            return redirect('home')                                                                #login method is going to add a session in the database and then inside our browser and that user will be officially logged-in
        else:
            messages.error(request, 'Username or Password does not exist.')
    context={'page':page}
    return render(request, 'base/login_register.html', context)
    ## and now if user has logged in and if we h=go into that inspect thing and we delete the session id then on refreshing on the home page the user automatically logs out.
    ## and whenever user logs in a neew session id is created.

def Registerpage(request):
    page='register'
    form=Myusercreationform()
    if request.method == 'POST':
        form= Myusercreationform(request.POST)
        if form.is_valid():
            user=form.save(commit=False)                                ##saving user data to user from the form
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occuredduring registration')

    context={'page':page, 'form': form}
    return render(request, 'base/login_register.html', context)

def Logoutuser(request):
    logout(request)
    return redirect('home')                                             ## in redirect we don't put request, context dictionary all that stuff we just need to put the url where we need the user to get redirected

def home(request):
    q=request.GET.get('q')  if request.GET.get('q')!=None else ''       ## q is basically our search parameter ## this whole if upto '' this is the value of qbasically this whole statement says if q is not empty then give it the value of 'q' i.e.request.GET.get('q') otherwise keep it empty.
                                                                        ##this is basically for the home pase as no q is there so on home page there will be no rooms if we dont apply the if else statements as we have applied in the above line. 
                                                                        ## this q belongs to the url one's q which is used in urls of browse topics.
    rooms= Room.objects.filter(Q(topic__name__icontains=q) |            #this topic is a variable from models.py file 
            Q(name__icontains=q) |                                      ## and go check all this variables(topic, name, description) carefully in models.py
            Q(description__icontains=q))                                ## verify about the functioning of icontains. as practically it by putting some words of the name in the url it is working without icontains, I think icontains or contains is used for the home page.
                                                                        ## if we keep contains instead of icontains then it will make the search case sensitive
                                                                        ## if we keep topic__name=q then we have to search through the full name.
                                                                        ## for now understand  keeping this icontains or contains is safe.                
    room_count=rooms.count                                              ##.count is faster than len(rooms)
    topics=Topic.objects.all()[0:5]
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))[0:5] ##it will give only those messages in the recent activity that are from that particular topic on which we click on home page and if we click all then it will give all the recent activity irrelative of the topic
    context={'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html',context)                 ## to render a html file

def room(request, pk):
    room= Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')                              ## in message_set message is not the model but we have used lowercase and that works. 
    if request.method=='POST' and request.user.is_authenticated :
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')                              ## body which is inside is the name which we have given while giving the input which we have given
        )                       
        room.participants.add(request.user)
        return redirect('room', pk=room.id)                                       ## inside create function of Message model we have variables which we have to put values of ( that are user, room and body )
    participants=room.participants.all()                              ## but for participants for now we need to go to admin and check participants their in every room. ## As it is a manyot many field so we don't need to give _set                               
    context={'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)                 ## to render a html file

def Userprofile(request, pk):
    user=User.objects.get(id=pk)                                        ##AS their  will be a particular id associated with the user
    rooms=user.room_set.all()                                           ##_set will give us all the objects setted by this particular user
    room_messages=user.message_set.all()                                ##room_messages it will be not room_message because see in activity_component.html we are iterating over room_messages and that is a perfect veriable or tuple whatever you say so we have to give the exact same name otherwise machine will get confused to iterate and you will get an error mentioning on which to iterate           
    topics=Topic.objects.all()
    bio= user.bio
    context={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics, 'bio':bio}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')                                     ##login_required make sures that login should be there if we like to create room.
def Createroom(request):
    form=Roomform()
    topics=Topic.objects.all()                                         ## for all the topics to be shown in the  dropdown of the topic while selecting topic while creating the room
    if request.method == 'POST' :
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
                )
        
        ## Above is the way through which we are getting the values of the form through frontend and saving the topic names for the next time as we create room so we will get those topics in like a drop down menu

        ##form= Roomform(request.POST)
        ##if form.is_valid():
        ##    room=form.save(commit=False)                                ## commit=false will save the instance when the form is saved
        ##    room.host=request.user                                      ##host of the room will be the user.
        ##    room.save()
        return redirect('home')                                               ##print(request.POST will print the filled up data of the form on terminal) and if we do request.POST.get('name') then it will give us the name of the room
    context={'form':form,'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def Updateroom(request, pk):
    room=Room.objects.get(id=pk)
    form=Roomform(instance=room)
    topics=Topic.objects.all()                                         ## for all the topics to be shown in the  dropdown of the topic while selecting topic while creating the room
    if request.user != room.host:                                                             #user should be the room host
        return HttpResponse('You are not allowed to update this room.')

    ## or else we could have done one more thing here that we have removed the option of delete and update for the users who are not the hosts of some rooms so for that rooms.
    ## and the above two lines of code are playing us safe even if we remove that delete and update option.
    if request.method == 'POST' :
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')
        
        ##form=Roomform(request.POST, instance=room)
        ##if form.is_valid():
        ##    form.save()
        ##    return redirect('home')
    context={'form':form,'topics':topics, 'room':room}
    return render(request, 'base/room_form.html',context)


@login_required(login_url='login')
def Deleteroom(request, pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:   
        return HttpResponse('You are not allowed to delete this room.')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def Deletemessage(request, pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:   
        return HttpResponse('You are not allowed to delete this room.')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def Updateuser(request):
    user=request.user
    form=Userform(instance = user)
    if request.method == 'POST':
        form=Userform(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={'form':form}
    return render(request, 'base/update_user.html', context )

def Topicspage(request):
    q=request.GET.get('q')  if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})

def Activitypage(request):
    room_messages= Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})