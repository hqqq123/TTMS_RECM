from django.urls import path

from ticket.views import sale, seat, buy, make_data, detail

urlpatterns = [
    path('sale/', sale, name='ticket_sale'),
    path('sale/<int:id>/', sale, name='ticket_sale'),
    path('detail/<int:id>/', detail, name='play_detail_sale'),
    path('seat/', seat, name='ticket_seat'),
    path('seat/<int:id>/', seat, name='ticket_seat'),
    path('seat/buy/<int:id>/', buy, name='seat_buy'),

    path('make_recm_data/', make_data, name='make_recm_data'),

    # path('edit/<int:id>/', edit, name='studio_edit'),
    # path('delete/<int:id>/', delete, name='studio_delete'),

]