from django.urls import path
from . import views
from .views.cpus import CPUInferenceView
from .views.ram import RAMInferenceView
from .views.monitor import MonitorInferenceView
from .views.motherboard import MotherboardInferenceView
from .views.powersupply import PowerSupplyInferenceView

urlpatterns = [
 
    path('cpu/infer/', CPUInferenceView.as_view(), name='cpu-infer'),
    path('ram/infer/', RAMInferenceView.as_view(), name='ram-infer'),
    path('monitor/infer/', MonitorInferenceView.as_view(), name='monitor-infer'),
    path('motherboard/infer/', MotherboardInferenceView.as_view(), name='motherboard-infer'),
    path('powersupply/infer/', PowerSupplyInferenceView.as_view(), name='powersupply-infer'),
]
