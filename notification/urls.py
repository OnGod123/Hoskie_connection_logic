from django.urls import path
from .views import profile_list_view, send_connection_request

urlpatterns = [
    path('profiles/', profile_list_view, name='profile_list'),
    path('send-connection-request/', send_connection_request, name='send_connection_request'),
    # other URL patterns
]
