from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
##from django.contrib.auth.models import User                           ## because we imported our own User from models


class Myusercreationform(UserCreationForm):
    class Meta:
        model=User
        fields=['name', 'username', 'email', 'password1', 'password2']              ##By default password1 means password field and password2 means reenter the password field

class Roomform(ModelForm):
    class Meta:
        model=Room
        fields= '__all__'          #we can keep it as '__all__' to get all the fields that are there in the room. or we can create a list of
                            #field that we want to specify in the form for our room creation.
        exclude=['host', 'participants']            ## we can even exclude some fields here.\
        
class Userform(ModelForm):
    class Meta:
        model=User
        fields=['name', 'avatar', 'username', 'email', 'bio']

