##from django.http import JsonResponse                              ## this is for json format
from rest_framework.decorators import api_view                      ## for a better view than json view
from rest_framework.response import Response
from base.models import Room
from base import api                        ## for a better view than json view
from .serializers import Roomserializer

@api_view(['GET'])                                                                    ## bracket inside are those that are the allowed requests which we can allow
def getRoutes(request):
    routes=[
        'GET api/',                                                 ## means when you are going for GET then you are going to get this homepage
        'GET api/room',                                             ## these are the data we are allowing the other users to scrap from our website whenebver they want to.
        'GET api/room/:id',
    ]
    return Response(routes)
    ##return JsonResponse(routes, safe=False)                         ## safe=false allows the routes data to get converted into json data 

@api_view(['GET'])
def getrooms(request):
    rooms=Room.objects.all()
    serializer=Roomserializer(rooms, many=True)                        ##many=true because it says that we can serialize many objects here.
    return Response(serializer.data)                                   ##.data because we don't want to return back the object we want to return back it s dta          ## so it will give output only when we use serializers because rooms are the python data. and not like json because objects cannot be converted automatically so we need to use serialiser

## nnow here we want to give data of one particular room so many=true no need because we are giving then one object.
@api_view(['GET'])
def getroom(request, pk):
    room=Room.objects.get(id=pk)
    serializer=Roomserializer(room)                        
    return Response(serializer.data)                                   ##.data because we don't want to return back the object we want to return back it s dta          ## so it will give output only when we use serializers because rooms are the python data. and not like json because objects cannot be converted automatically so we need to use serialiser