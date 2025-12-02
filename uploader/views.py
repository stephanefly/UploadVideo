from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UploadedVideoForm
from .models import UploadedVideo
from .services.pcloud import upload_to_pcloud
from .services.trello import create_trello_card


def upload_view(request):
    # --- GET : afficher formulaire + tableau ---
    if request.method == "GET":
        form = UploadedVideoForm()
        videos = UploadedVideo.objects.order_by('-created_at')
        return render(request, "upload.html", {
            "form": form,
            "videos": videos
        })

    # --- POST : traiter l'upload ---
    form = UploadedVideoForm(request.POST, request.FILES)

    if not form.is_valid():
        videos = UploadedVideo.objects.order_by('-created_at')
        return render(request, "upload.html", {
            "form": form,
            "videos": videos
        })

    title = form.cleaned_data['title']
    uploader = form.cleaned_data['uploader']
    video = request.FILES["video"]

    # Nouveau nom : titre_uploader_YYYYMMDD.mp4
    ts = timezone.now().strftime("%Y%m%d")
    new_filename = f"{title}_{uploader}_{ts}.mp4"

    # Upload pCloud
    fileid = upload_to_pcloud(video, new_filename)

    # Carte Trello
    desc = f"Uploader : {uploader}\nFichier : {new_filename}\n"
    trello_url = create_trello_card(title, desc, uploader)

    # Sauvegarde en base
    UploadedVideo.objects.create(
        title=title,
        uploader=uploader,
        filename=new_filename,
        pcloud_fileid=str(fileid),
        trello_url=trello_url,
    )

    # Redirection vers GET (simple et propre)
    return redirect(request.path)
