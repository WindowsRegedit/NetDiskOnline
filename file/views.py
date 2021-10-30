from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse
from django.core.files import File
import os

SAVED_FILES_DIR = r'files/'
def render_home_template(request):
    files = os.listdir(SAVED_FILES_DIR)
    return render(request, 'home.html', {'files': files})
@require_GET
def home(request):
    if not os.path.exists(SAVED_FILES_DIR):
        os.makedirs(SAVED_FILES_DIR)

    return render_home_template(request)
@require_GET
def download(request, filename):
    file_pathname = os.path.join(SAVED_FILES_DIR, filename)

    with open(file_pathname, 'rb') as f:
        file = File(f)

        response = HttpResponse(file.chunks(),
                                content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)

    return response
@require_POST
def upload(request):
    file = request.FILES.get("filename", None)
    if not file:
        return render_home_template(request)

    pathname = os.path.join(SAVED_FILES_DIR, file.name)

    with open(pathname, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return render_home_template(request)