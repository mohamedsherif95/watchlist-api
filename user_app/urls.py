from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from  user_app.api.api import LogOutApi, RegesterationApi
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


urlpatterns = [
    path('login/', obtain_auth_token,name='login'),
    path('Regester/',RegesterationApi.as_view() ,name='regester'),
    path('logout/',LogOutApi.as_view() ,name='logout'),
    
    # jwt Auth#
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    
]
