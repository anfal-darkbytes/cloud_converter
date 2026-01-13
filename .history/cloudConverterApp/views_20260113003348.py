import os
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.files.storage import default_storage
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

            # save file temporarily in MEDIA_ROOT/temp/
            temp_folder = "temp"
            if not os.path.exists(os.path.join(default_storage.location, temp_folder)):
                os.makedirs(os.path.join(default_storage.location, temp_folder))

            temp_path = default_storage.save(f"{temp_folder}/{uploaded_file.name}", uploaded_file)

            # store path in session instead of raw bytes
            request.session["uploaded_file_path"] = temp_path
            request.session["source_ext"] = source_ext
            request.session["targets"] = targets

            # redirect to dynamic URL
            return redirect(f"/{source_ext}-to-{targets[0]}/")

    return render(request, "home/home.html", {"form": form})


def convert(request, from_ext, to_ext):
    """
    Converter screen:
    - URL-driven (from_ext → to_ext)
    - Allows re-upload
    - Allows selecting another target format
    """
    session_source = request.session.get("source_ext")
    targets = request.session.get("targets", [])

    # security & validation
    if session_source != from_ext or to_ext not in targets:
        raise Http404("Invalid conversion")

    form = ConvertForm()
    form.fields["target_format"].choices = [(t, t.upper()) for t in targets]
    form.fields["target_format"].initial = to_ext

    output_file = None

    if request.method == "POST":
        form = ConvertForm(request.POST, request.FILES)
        form.fields["target_format"].choices = [(t, t.upper()) for t in targets]

        if form.is_valid():
            selected_target = form.cleaned_data["target_format"]

            # get uploaded file path from session
            file_path = request.session.get("uploaded_file_path")
            if not file_path or not default_storage.exists(file_path):
                raise Http404("Uploaded file not found")

            with default_storage.open(file_path, "rb") as f:
                file_content = f.read()

            # call your conversion function
            output_file = convert_file(file_content, os.path.basename(file_path), selected_target)

    return render(request, "converter/convert.html", {
        "form": form,
        "from_ext": from_ext,
        "to_ext": to_ext,
        "output_file": output_file,
    })
