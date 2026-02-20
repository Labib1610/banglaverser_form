from django.urls import path
from . import views

app_name = 'evaluation'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/get-dialect-data/', views.get_dialect_data, name='get_dialect_data'),
    path('api/get-plausibility-data/', views.get_plausibility_data, name='get_plausibility_data'),
    path('api/submit-evaluation/', views.submit_evaluation, name='submit_evaluation'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('export/', views.export_data, name='export'),
]
