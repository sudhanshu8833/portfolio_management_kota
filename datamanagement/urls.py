from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    # path('data_calculation_kdsjfzlwaoruoiewwqncsaoiaevsjka/', views.data_calculation, name='index'),
    path('position/', views.position, name='position'),
    path('start_strategy/', views.start_strategy, name='start_strategy'),
    path('handleLogin/', views.handleLogin, name='/handleLogin'),
    path('order/', views.closed_positions, name='start_strategy'),
    path('session_id/', views.get_session_id, name='session_id'),

]