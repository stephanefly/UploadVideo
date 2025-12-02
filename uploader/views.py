from django.shortcuts import render
from django.utils import timezone

from .forms import UploadedVideoForm
from .models import UploadedVideo
from .services.pcloud import upload_to_pcloud
from .services.trello import create_trello_card

def upload_view(request):
    context = {}

    if request.method == "POST":
        form = UploadedVideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            uploader = form.cleaned_data['uploader']
            video = request.FILES["video"]

            # Renommage : YYYYMMDD-HHMM_UPLOADER.mp4
            ts = timezone.now().strftime("%Y%m%d")
            new_filename = f"{title}_{uploader}_{ts}.mp4"


            # 1) Upload pCloud
            fileid = upload_to_pcloud(video, new_filename)

            desc = (
                f"Uploader : {uploader}\n"
                f"Fichier : {new_filename}\n"
            )

            # -> IMPORTANT : on utilise le titre du formulaire
            trello_url = create_trello_card(title, desc, uploader)

            # 3) Sauvegarder en base
            UploadedVideo.objects.create(
                title=title,  # <-- ajout
                uploader=uploader,
                filename=new_filename,
                pcloud_fileid=str(fileid),
                trello_url=trello_url,
            )

            context.update({
                "success": True,
                "filename": new_filename,
                "trello_url": trello_url,
            })
            form = UploadedVideoForm()  # formulaire vide après succès
    else:
        form = UploadedVideoForm()

    context["form"] = form
    return render(request, "upload.html", context)
