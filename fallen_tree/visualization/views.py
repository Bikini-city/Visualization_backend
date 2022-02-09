from http import HTTPStatus
from http.client import BAD_REQUEST
from msilib.schema import Error
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .serializers import DataSetSerializer
from .forms import FileUploadForm
from .models import DataSet, FileUpload
from .response_schema import *

from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser,MultiPartParser
from rest_framework.decorators import parser_classes

def fileUpload(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        img = request.FILES["imgfile"]
        fileupload = FileUpload(
            title=title,
            content=content,
            imgfile=img,
        )
        fileupload.save()
        return redirect('fileupload')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

src = openapi.Parameter('src', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True)
lat = openapi.Parameter('lat', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, required=True)
lng = openapi.Parameter('lng', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, required=True)
dat = openapi.Parameter('date', openapi.IN_FORM, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=True)

#POST /datas
@swagger_auto_schema(method="post",responses=channelList_response_dict,manual_parameters=[src,lat,lng,dat])
@api_view(['POST'])
@parser_classes([MultiPartParser])
def post(request):
    
    error_data = {}
    if request.method == 'POST':
        lat = request.POST['lat']
        lng = request.POST['lng']
        src = request.FILES.get("src", None)
        date = request.POST['date']
        dataSet = DataSet(
            lat=lat,
            lng=lng,
            src=src,
            date=date,
        )
        dataSet.save()
        dataSet_data = DataSetSerializer(dataSet).data
        return JsonResponse(dataSet_data, safe=False, status=status.HTTP_201_CREATED)
    else:
        error_data["error"] = "POST /datas에서 오류가 발생함"
        return JsonResponse(error_data, safe=False, status=HTTPStatus/BAD_REQUEST)
        
