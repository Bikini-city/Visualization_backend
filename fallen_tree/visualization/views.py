from http import HTTPStatus
from http.client import BAD_REQUEST
from msilib.schema import Error
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

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
from rest_framework.views import APIView

test = True

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

#POST /datas/uploads
@swagger_auto_schema(method="post",responses=channelList_response_dict,manual_parameters=[src,lat,lng,dat])
@api_view(['POST'])
@parser_classes([MultiPartParser])
def postDataSet(request):
    
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

        #### For Test START ####
        if test:
            result = Result(
                broken = 4,
                fallen = 3,
                dataset_id = dataSet
            )
            result.save()
        #### For Test END ####

        return JsonResponse(dataSet_data, safe=False, status=status.HTTP_201_CREATED)
    else:
        error_data["error"] = "POST /datas에서 오류가 발생함"
        return JsonResponse(error_data, safe=False, status=HTTPStatus/BAD_REQUEST)

#GET datas/
@swagger_auto_schema(method="get",responses=channelList_response_dict)
@api_view(['GET'])
def getDataSets(request):        
    dataSets = DataSet.objects.all()
        
    response = []

    for dataSet in dataSets:
        dataSet_json = DataSetSerializer(dataSet).data   
        dataSet_id = dataSet_json["id"]
        result = get_object_or_404(Result,dataSet_id=dataSet_id)
        result_json = ResultSerializer(result).data
        print(result_json)
        dataSet_json["broken"] = result_json["broken"]
        dataSet_json["fallen"] = result_json["fallen"]
        response.append(dataSet_json)

    return JsonResponse(response, safe=False)


class DataSetWithID(APIView):
    
    #GET datas/{id}
    @swagger_auto_schema(responses=channelList_response_dict)
    def get(self, request, *args, **kwargs):   
        id = kwargs.get("id")
        dataSet = get_object_or_404(DataSet, id=id)
        result = get_object_or_404(Result, dataSet_id = id)
        dataSet_json = DataSetSerializer(dataSet).data
        result_json = ResultSerializer(result).data
        dataSet_json["broken"] = result_json["broken"]
        dataSet_json["fallen"] = result_json["fallen"]
        
        return JsonResponse(dataSet_json, safe=False)

    #DELETE datas/{id}
    @swagger_auto_schema(responses=channelList_response_dict)
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dataSet = DataSet.objects.filter(id=id)
        result = Result.objects.filter(dataset_id=id)

        response = DataSetSerializer(dataSet).data

        dataSet.delete()
        result.delete()

        return JsonResponse(response, safe=False, status=status.HTTP_204_NO_CONTENT)
