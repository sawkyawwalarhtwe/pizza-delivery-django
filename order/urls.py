from django.urls import path
from . import views

urlpatterns = [
    path('',views.OrderCreateListView.as_view(),name='order'),
    path('<int:order_id>/',views.OrderDetailsView.as_view(),name='order_details'),
    path('update-status/<int:order_id>/',views.UpdateOrderStatus.as_view(),name='order_update_status'),
    path('user/<int:user_id>/',views.UserOrderView.as_view(),name='user_order'),
    path('<int:order_id>/user/<int:user_id>/',views.UserOrderDetail.as_view(),name='user_order_specific'),
]