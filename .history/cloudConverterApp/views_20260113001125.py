from django.shortcuts import render, redirect
from django.http import Http404
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

            # store in session
            request.session["uploaded_file_name"] = uploaded_file.name
            request.session["source_ext"] = source_ext
            request.session["targets"] = targets

            # redirect to SEO-friendly dynamic URL
            return redirect(f"/{source_ext}-to-{targets[0]}/")

    return render(request, "home.html", {"form": form})


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
        form = ConvertForm(request.POST)
        form.fields["target_format"].choices = [(t, t.upper()) for t in targets]

        if form.is_valid():
            uploaded_file = request.FILES.get("file")
            selected_target = form.cleaned_data["target_format"]

            if not uploaded_file:
                raise Http404("No file uploaded")

            output_file = convert_file(uploaded_file, selected_target)

    return render(request, "convert.html", {
        "form": form,
        "from_ext": from_ext,
        "to_ext": to_ext,
        "output_file": output_file,
    })
