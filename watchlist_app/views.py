from django.forms import ValidationError
from watchlist_app.models import Review, Watchlist,StreamPlatFormn
from watchlist_app.serializer import ReviewSerializer, StreamPlatFormSerializer,Watchlistserializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,mixins
from django.db.models import Avg
from rest_framework import viewsets
from .permissions import ReviewOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.throttling import ReviewCreateThrottling,ReviewListThrottling
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.paginations import WatchlistPagination,WatchlistCursorPagination




class ReviewUser(generics.ListAPIView):
    
    
    serializer_class=ReviewSerializer
    
    def get_queryset(self):
        #   username = self.kwargs['username']
        #   return Review.objects.filter(user_review__username=username)
        username = self.request.query_params.get('username')
        return Review.objects.filter(user_review__username=username)



class ReviewDetails(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[ReviewOrReadOnly,IsAuthenticated]
    # throttle_classes=[UserRateThrottle,AnonRateThrottle]
    # throttle_classes=[ScopedRateThrottle]
    # throttle_scope='review_details'


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class ReviewList(generics.ListAPIView):
    
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    # throttle_classes=[ReviewListThrottling]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_review__username', 'watchlist__title']


class ReviewCreate(generics.CreateAPIView):
    serializer_class=ReviewSerializer
    throttle_classes=[ReviewCreateThrottling]


    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlist=Watchlist.objects.get(pk=pk)

        user=self.request.user
        user_queryset=Review.objects.filter(watchlist=watchlist,user_review=user)
        if user_queryset.exists():
            raise ValidationError("you are rating this movie before")
        serializer.save(watchlist=watchlist,user_review=user)
       



class SteamPlatformVS(viewsets.ModelViewSet):
    queryset=StreamPlatFormn.objects.all()
    serializer_class=StreamPlatFormSerializer

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs) 

# class SteamPlatformAV(APIView):
#     def get(self,request):
#         try:
#             platform=StreamPlatFormn.objects.all()
#         except StreamPlatFormn.DoesNotExist:
#             return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
#         serializer=StreamPlatFormSerializer(platform,many=True,context={'request': request})
#         return Response(serializer.data,status=status.HTTP_200_OK)

#     def post(self,request):
#         serializer=StreamPlatFormSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

# class SteamPlatformDetailsAV(APIView):
#     def get(self,request,pk):
#         try:
#             platform=StreamPlatFormn.objects.get(pk=pk)
#         except StreamPlatFormn.DoesNotExist:
#             return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
#         serializer=StreamPlatFormSerializer(platform,context={'request': request})
#         return Response(serializer.data,status=status.HTTP_200_OK)

#     def put(self,request,pk):
#         try:
#             platform=StreamPlatFormn.objects.get(pk=pk)
#         except StreamPlatFormn.DoesNotExist:
#             return Response({'platform doesnt found'})
#         serializer=StreamPlatFormSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

#     def patch(self,request,pk):
#         try:
#             platform=StreamPlatFormn.objects.get(pk=pk)
#         except StreamPlatFormn.DoesNotExist:
#             return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
#         serializer=Watchlistserializer(platform,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self,request,pk):
#         try:
#             platform=StreamPlatFormn.objects.get(pk=pk)
#         except StreamPlatFormn.DoesNotExist:
#             return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)    

class watchlistSearch(generics.ListAPIView):
    queryset=Watchlist.objects.all()
    serializer_class=Watchlistserializer
    pagination_class=WatchlistPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'stream__name']
    filter_backends = [filters.SearchFilter]
    search_fields  = ['title', 'stream__name']

class WatchlistAv(APIView):
    
    def get(self,request):
        try:
            movie=Watchlist.objects.all()
        except Watchlist.DoesNotExist:
            return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
        serializer=Watchlistserializer(movie,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        serializer=Watchlistserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    


class WatchDeatilsAv(APIView):
    def get(self,request,pk):
        try:
            movie=Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
        serializer=Watchlistserializer(movie)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def put(self,request,pk):
        try:
            movie=Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
        serializer=Watchlistserializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk):
        try:
            movie=Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
        serializer=Watchlistserializer(movie,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            movie=Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'movie:DoesNot found'},status=status.HTTP_204_NO_CONTENT)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    


# @api_view(["GET","POST"])
# def movies(request):
#     movie=Movies.objects.all()
#     if request.method=="POST":
#         serializer=Movieserializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     else:
#         serializer=Movieserializer(movie,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)

# @api_view(["GET","PUT","DELETE","PATCH"])
# def moviess(request,pk):
#     if request.method=="GET":
#        movie=Movies.objects.get(pk=pk)
#        serializer=Movieserializer(movie)
#        return Response(serializer.data,status=status.HTTP_200_OK)
#     elif request.method=="PUT":
#         movie=Movies.objects.get(pk=pk)
#         serializer=Movieserializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#     elif request.method=="PATCH":
#         movie=Movies.objects.get(pk=pk)
#         serializer=Movieserializer(movie,data=request.data,partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors,status==status.HTTP_400_BAD_REQUEST)
#     else:
#         movie=Movies.objects.get(pk=pk)
#         movie.delete()
#         response={
#             "deleted done"
#         }
#         return Response(response,status=status.HTTP_200_OK)

