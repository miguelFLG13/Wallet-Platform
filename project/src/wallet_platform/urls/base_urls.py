from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path('user/', include('users.urls')),
    path('wallet/', include('wallets.urls'))
]
