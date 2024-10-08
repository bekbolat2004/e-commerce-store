from django.urls import path

from baskets import views

app_name = 'baskets'

# urlpatterns = [
#     path('basket_add/<int:basket_id>/', views.basket_add, name='basket_add'),
#     path('basket_change/<int:basket_id>/', views.basket_change, name='basket_change'),
#     path('basket_remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
# ]

urlpatterns = [
    path('basket_add/<slug:product_slug>/', views.basket_add, name='basket_add'),
    path('basket_change/<slug:product_slug>/', views.basket_change, name='basket_change'),
    path('basket_remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]



