from django.urls import path
from media_separator.views import *

urlpatterns = [
    path('mainPage/', mainPage_page, name='mainPage'),
    path('get_face/', get_face_page, name='get_face'),
    path('classify_face/', classify_face_page, name='classify_face'),
    path('neural_trans/', neural_trans_page, name='neural_trans'),
    path('download/<filename>', download, name='download'),
    path('delete/<filename>', delete, name='delete'),
]