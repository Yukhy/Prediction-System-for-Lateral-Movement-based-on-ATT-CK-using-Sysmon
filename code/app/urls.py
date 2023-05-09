from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.index, name='index'),
    path("result/technique/", views.result_technique, name="result_technique"),
    path("result/similarity/", views.result_similarity, name="result_similarity"),
    path("content/matrix", views.get_matrix_data, name="matrix_data")
]