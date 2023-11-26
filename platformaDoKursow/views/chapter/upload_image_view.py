from ckeditor_uploader import views as ckeditor_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required  # Or your custom permission decorator
@require_http_methods(["POST"])
def custom_ckeditor_upload(request):
    # Add any custom permission checks here
    # If everything is okay, call the original CKEditor upload view
    return ckeditor_views.upload(request)
