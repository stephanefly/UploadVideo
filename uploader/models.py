from django.db import models

class UploadedVideo(models.Model):
    title = models.CharField(max_length=255)
    uploader = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    pcloud_fileid = models.CharField(max_length=100)
    trello_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
