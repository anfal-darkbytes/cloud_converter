
import os
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _



BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-z9ka++w(23biig%h-p)75bs8*%cgm+fj4y7)$p%9p!xb+3%f80'

DEBUG = True

ALLOWED_HOSTS = []

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudConverterApp',
    'django_celery_beat',
    'blog',
    'tinymce',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cloudConverterProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cloudConverterProject.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CELERY_BEAT_SCHEDULE = {
    'run-function-every-5-minutes': {
        'task': 'cloudConverterApp.utils.del_old_conversions',
        'schedule': 300.0,
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
# Source - https://stackoverflow.com/a/74781169
# Posted by Calpurnio Pisone, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-30, License - CC BY-SA 4.0

TINYMCE_DEFAULT_CONFIG = {
    "entity_encoding": "raw",
    "menubar": "file edit view insert format tools table help",
    "plugins": 'print preview paste importcss searchreplace autolink autosave save code visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists wordcount imagetools textpattern noneditable help charmap emoticons quickbars',
    "toolbar": "fullscreen preview | undo redo | bold italic forecolor backcolor | formatselect | image link | "
    "alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | fontsizeselect "
    "emoticons | ",
    'paste_text_sticky': True,
    'paste_text_sticky_default': True,
    'valid_styles': 'font-weight,font-style,text-decoration',
    'fontsize_formats': "8pt 10pt 11pt 12pt 13pt 14pt 16pt 18pt 20pt 24pt 36pt",
    'font_formats': "Andale Mono=andale mono,times;" +
    "Arial=arial,helvetica,sans-serif;" +
    "Arial Black=arial black,avant garde;" +
    "Book Antiqua=book antiqua,palatino;" +
    "Comic Sans MS=comic sans ms,sans-serif;" +
    "Courier New=courier new,courier;" +
    "Georgia=georgia,palatino;" +
    "Helvetica=helvetica;" +
    "Impact=impact,chicago;" +
    "Symbol=symbol;" +
    "Tahoma=tahoma,arial,helvetica,sans-serif;" +
    "Terminal=terminal,monaco;" +
    "Times New Roman=times new roman,times;" +
    "Trebuchet MS=trebuchet ms,geneva;" +
    "Verdana=verdana,geneva;" +
    "Webdings=webdings;" +
    "Wingdings=wingdings,zapf dingbats",
    "custom_undo_redo_levels": 50,
    "quickbars_insert_toolbar": False,
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
    "content_style": "body { font-family:Roboto,Helvetica,Arial,sans-serif; font-size:14px }",
}

DATA_UPLOAD_MAX_MEMORY_SIZE= 26214400

