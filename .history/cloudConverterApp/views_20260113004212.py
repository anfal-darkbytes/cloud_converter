import base64
import os
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .forms import UploadForm, ConvertForm
from .services import handle_upload, convert_file


def home(request):
    """
    Home screen:
    - Upload file
    - Auto-detect extension
    - Redirect to dynamic URL: /from-to-to
    """
    form = UploadForm()

    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data["file"]

            # detect source extension and valid targets
            source_ext, targets = handle_upload(uploaded_file)

            if not targets:
                raise Http404("Unsupported file format")

            # store file content in session using base64
            file_content_b64 = base64.b64encode(uploaded_file.read()).decode("ascii")

            request.session["uploaded_file_name"] = uploaded_file.name
            request.session["uploaded_file_content"] = file_content_b64
            request.session["source_ext"] = source_ext
            request.session["targets"] = targets

            # redirect to SEO-friendly dynamic URL
            return redirect(f"/{source_ext}-to-{targets[0]}/")

    return render(request, "home/home.html", {"form": form})


def convert(request, from_ext, to_ext):
    """
    Converter screen:
    - URL-driven (from_ext → to_ext)
    - Allows re-upload
    - Allows selecting another target format
    - Returns downloadable converted file
    """
    session_source = request.session.get("source_ext")
    targets = request.session.get("targets", [])

    # security & validation
    if session_source != from_ext or to_ext not in targets:
        raise Http404("Invalid conversion")

    form = ConvertForm()
    form.fields["target_format"].choices = [(t, t.upper()) for t in targets]
    form.fields["target_format"].initial = to_ext

    if request.method == "POST":
        form = ConvertForm(request.POST)
        form.fields["target_format"].choices = [(t, t.upper()) for t in targets]

        if form.is_valid():
            selected_target = form.cleaned_data["target_format"]

            # retrieve file content from session
            file_content_b64 = request.session.get("uploaded_file_content")
            if not file_content_b64:
                raise Http404("Uploaded file not found in session")

            file_content = base64.b64decode(file_content_b64.encode("ascii"))

            # convert file
            converted_file = convert_file(file_content, request.session.get("uploaded_file_name"), selected_target)

            # return as downloadable response
            response = HttpResponse(converted_file, content_type=f"application/octet-stream")
            # set correct file name
            base_name, _ = os.path.splitext(request.session.get("uploaded_file_name"))
            response['Content-Disposition'] = f'attachment; filename="{base_name}.{selected_target}"'
            return response

    return render(request, "converter/convert.html", {
        "form": form,
        "from_ext": from_ext,
        "to_ext": to_ext,
    })
