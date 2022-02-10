
from django.db import router
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('stream',views.SteamPlatformVS,basename="streaml")
urlpatterns=[
# path('Steamlist',views.SteamPlatformAV.as_view(),name='Stramelist'),
# path('Steamlist/<int:pk>',views.SteamPlatformDetailsAV.as_view(),name='Streamdetails'),
path('',include(router.urls)),
path('watchlist',views.WatchlistAv.as_view(),name="watchlist"),
path('watchlistsearch',views.watchlistSearch.as_view(),name="watchlistsearch"),
path('watchlist/<int:pk>',views.WatchDeatilsAv.as_view(),name="watchdetails"),
path("stream/review",views.ReviewList.as_view(),name="revlist"),
path("stream/<int:pk>/review-create",views.ReviewCreate.as_view(),name="revcreate"),
path("stream/review/<int:pk>",views.ReviewDetails.as_view(),name="revdetails"),
# filter 
# path('review/<str:username>',views.ReviewUser.as_view(),name='reviewfilter'),
# filter by queryparams
path('review/',views.ReviewUser.as_view(),name='reviewfilter')

]