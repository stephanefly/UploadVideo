from .models import UploadedVideo

from django import forms

class UploadedVideoForm(forms.Form):
    title = forms.CharField(label="Titre de la vidéo", max_length=255)
    uploader = forms.CharField(label="Votre nom", max_length=100)
    video = forms.FileField(label="Vidéo (.mp4)")
