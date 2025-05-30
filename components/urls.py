from django.urls import path
from . import views
from .views.cpus import CPUInferenceView
from .views.ram import RAMInferenceView


urlpatterns = [
 
    path('cpu/infer/', CPUInferenceView.as_view(), name='cpu-infer'),
    path('ram/infer/', RAMInferenceView.as_view(), name='ram-infer'),
    
]
