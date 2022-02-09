from drf_yasg import openapi
from .serializers import *

channelList_response_dict = {
    "200" : openapi.Response(
        description="Success",
        schema=DataSetSerializer,
        examples={
            "application/json": {
                "user": {
                    "id": 1,
                    "name": "moon",
                    "info": {
                        "age": 23,
                        "gender": "female",
                        "부서": "개발팀"
                    },
                    "profile_photo": "/upload_files/toy.jpg"
            },
                "channels": [
                {
                    "id": 1,
                    "name": "뭉가네",
                    "lock": 0,
                    "background": "/upload_files/toy.jpg"
                },
                {
                    "id": 2,
                    "name": "마루네",
                    "lock": 0,
                    "background": "/upload_files/%EB%A9%94%EB%A5%98.jpg"
                }
            ]
                    }
            }
    ),
    "401" : openapi.Response(
        description="헤더에 authorazation이 없거나, 사용자가 존재하지 않을때",
        examples={
            "application/json":{
            "error": "Authorization Error"
        }
        }
    ),
    "401" : openapi.Response(
        description="헤더에 authorazation이 존재하나 decoding에 실패할 경우",
        examples={
            "application/json":{
             "error" : "Decoding Token fail"
        }
        }
    ),
    "403" : openapi.Response(
        description="토큰 인증 만료",
        examples={
            "application/json":{
             "error": "Expired token. Please log in again."
        }
        }
    ),
}
