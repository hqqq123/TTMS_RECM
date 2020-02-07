from django.urls import path
from play.views import list, add, edit, delete, get_data, like, like_cancel, init_data, up, search

urlpatterns = [
    path('list/', list, name='play_list'),
    path('add/', add, name='play_add'),
    path('edit/<int:id>/', edit, name='play_edit'),
    path('delete/<int:id>/', delete, name='play_delete'),
    path('like/<int:id>/', like, name='play_like'),
    path('like_cancel/<int:id>/', like_cancel, name='play_like_cancel'),
    path('get_data/', get_data, name='get_data'),
    path('up/<int:id>/', up, name='play_up'),
    path('init_data/', init_data, name='init_data'),
    path('search/', search, name='play_search'),

]