from django.contrib import admin
from django.urls import path, include
from uploader import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('uploader.urls')),  # page d'accueil = upload
    path("export-videos-excel/", views.export_videos_excel, name="export_videos_excel"),
]
