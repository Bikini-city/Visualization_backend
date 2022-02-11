import os
import time

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

from .serializers import DetectionsSerializer
from .models import Detections
from .setups import DEMO_PATH,EXP_FILE,MODEL_PATH
from .YOLOX.tools.demo import main,make_parser,get_exp
from .codewriter import json_reader,addUiElements
from rest_framework import viewsets

from visualization.detect_fallen import *

test = True

#form-data for posting dataset's image or video
src = openapi.Parameter('src', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True)
lat = openapi.Parameter('lat', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, required=True)
lng = openapi.Parameter('lng', openapi.IN_FORM, type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, required=True)
dat = openapi.Parameter('date', openapi.IN_FORM, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=True)

#GET datas/
@swagger_auto_schema(method="get",responses=GetDataSet_response_dict)
@api_view(['GET'])
def getDataSets(request):        
    response = []

    dataSets = DataSet.objects.all()
    for dataSet in dataSets:
        dataSet_json = DataSetSerializer(dataSet).data   
        dataSet_id = dataSet_json["id"]
        result = get_object_or_404(Result,dataSet_id=dataSet_id)
        result_json = ResultSerializer(result).data

        dataSet_json["broken"] = result_json["broken"]
        dataSet_json["fallen"] = result_json["fallen"]
        
        response.append(dataSet_json)

    return JsonResponse(response, safe=False)

#POST /datas/uploads
@swagger_auto_schema(method="post",manual_parameters=[src,lat,lng,dat],responses=PostDataSet_response_dict)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def postDataSet(request,**args):
    
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

        down, broken = detect(src)
        
        #### For Test START ####
        if test:
            result = Result(
                broken = broken,
                fallen = down,
                dataSet_id = dataSet
            )
            result.save()
        #### For Test END ####

        result_json = ResultSerializer(result).data
        dataSet_data["broken"] = result_json["broken"]
        dataSet_data["fallen"] = result_json["fallen"]

        return JsonResponse(dataSet_data, safe=False, status=status.HTTP_201_CREATED)
    else:
        error_data["error"] = "POST /datas에서 오류가 발생함"
        return JsonResponse(error_data, safe=False, status=HTTPStatus/BAD_REQUEST)


class DataSetWithID(APIView):
    
    #GET datas/{id}
    @swagger_auto_schema(responses=GetDataSetDetail_response_dict)
    def get(self, request, *args, **kwargs): 
        # model 가져오기
        id = kwargs.get("id")
        dataSet = get_object_or_404(DataSet, id=id)
        result = get_object_or_404(Result, dataSet_id = id)
        dataSet_json = DataSetSerializer(dataSet).data
        result_json = ResultSerializer(result).data

        #응답부분에 result의 broken, fallen 정보 넣기
        dataSet_json["broken"] = result_json["broken"]
        dataSet_json["fallen"] = result_json["fallen"]
        
        return JsonResponse(dataSet_json, safe=False)

    #DELETE datas/{id}
    @swagger_auto_schema(responses=DeleteDataSetDetail_response_dict)
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dataSet = DataSet.objects.filter(id=id)
        result = Result.objects.filter(dataSet_id=id)

        response = DataSetSerializer(dataSet).data

        dataSet.delete()
        result.delete()

        return JsonResponse(response, safe=False, status=status.HTTP_204_NO_CONTENT)
    
"""class DetectionsViewSet(viewsets.ModelViewSet):
    queryset = Detections.objects.filter(id=1)
    serializer_class = DetectionsSerializer


    def create(self, request, *args, **kwargs):

        # Perform Transaction
        confidence = float(request.data['confidence'])
        image_to_detect = request.data['image_to_detect']

        detections = Detections.objects.create(image_to_detect=image_to_detect,confidence=confidence)
        VAL_IMG_PATH = f'media/{detections.image_to_detect}'

        # YOLOX PARAMETERS
        conf = confidence
        args = make_parser().parse_args()
        args.demo = "image"
        args.exp_file = EXP_FILE
        args.ckpt = MODEL_PATH
        args.path = VAL_IMG_PATH
        args.conf = conf
        args.nms = 0.45
        args.tsize = 640
        args.save_result = True
        exp = get_exp(args.exp_file, args.name)

        # YOLOX DETECTOR
        jfile = main(exp,args)
        # img,jfile = path_converter(img),path_converter(jfile)

        # PYQT CODE GENERATOR
        data = json_reader(jfile)
"""
        

      

       

