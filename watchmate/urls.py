
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user_app.urls')),
    path('movie/',include('watchlist_app.urls'))
]
