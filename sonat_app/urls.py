from django.urls import path
from .views import api_login, api_register, api_data_user, api_edit_profile, api_logout, search_track, api_add_library, \
    api_get_library, api_filter_library

urlpatterns = [
    path('login/',api_login, name='api_login'),
    path('logout/', api_logout, name='api_logout'),
    path('register/', api_register, name='api_register'),
    path('profile/', api_data_user, name='api_data_user'),
    path('profile/edit/', api_edit_profile, name='api_edit_profile'),
    path('search/', search_track, name='api_search'),
    path('add_library/', api_add_library, name='api_add_library'),
    path("library/", api_get_library, name="api_get_library"),
    path("filter/", api_filter_library, name="api_filter_library")
]