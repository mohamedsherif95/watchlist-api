from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from user_app.api.serializer import RegesterSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken




class LogOutApi(APIView):

    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RegesterationApi(APIView):

    @csrf_exempt
    def post(self,request):
        serializer=RegesterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']="Regestrition Success"
            data['username']=account.username
            data['email']=account.email

            token=Token.objects.get(user=account).key
            data['token']=token

            # jwt genertate token
            # refresh = RefreshToken.for_user(account)
            # data['token']={
            #                  'refresh': str(refresh),
            #                  'access': str(refresh.access_token),

            #                 }

        else:
            data=serializer.errors
        return Response(data)



# api_view(["post"])
# def Regerster_View(request):
#     if request.method=='POST':
#         serializer=RegesterSerializer(data=request.body)
#         data={}
#         if serializer.is_valid():
#             account=serializer.save()
#             data['response']="Regestrition Success"
#             data['username']=account.username
#             data['email']=account.email

#             token=Token.objects.get(user=account).key
#             data['token']=token
#         else:
#             data=serializer.errors
#         return Response(data)

