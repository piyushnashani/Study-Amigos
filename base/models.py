from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    #pass
    name= models.CharField(max_length=200, null=True)
    email= models.EmailField(unique=True, null=True)
    bio=models.TextField(null=True)

    avatar= models.ImageField(null=True, default="avatar.svg")                  ## this command requires pillow library to install ##but in setttings we also need to set that where will the user uploaded content like picture will be saved/saved and we also need to give some url to this picture

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]

class Topic(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model):
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic= models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)   #We are deleteing then there will be empty topics, because,
                                                                            #we are deleting topics not the rooms so topics can be empty
                                                                            #after deleting it so we have specify null=True and similar 
                                                                            #for thee hosts
    name= models.CharField(max_length=200)
    description= models.TextField(null=True, blank=True)        ##null is for the database, and blank is for the form, basically we
                                                                ##can have this description as empty in the database and we can have
                                                                ## and we can have this empty as we submit the form.
    participants= models.ManyToManyField(                       ##we have already used User before that's why we need to give related name
        User, related_name='participants', blank=True)
    updated= models.DateTimeField(auto_now=True)                #autonow for saving the time at every time instant we save it
    created= models.DateTimeField(auto_now_add=True)            #autonowadd for saving the time at the first timeinstant we created it.

    class Meta:
        ordering= ['-updated','-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    room=models.ForeignKey(Room, on_delete=models.CASCADE)      #cascade will delete the messages if that specific room gets deleted
                                                                #if we do on_delete=models.SET_NULL then the messages gets stored in the database even if the room is deleted
    body=models.TextField()
    updated= models.DateTimeField(auto_now_add=True)
    created= models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering= ['-updated','-created']                        ##Ordering of the messages

    def __str__(self):
        return self.body[0:50]