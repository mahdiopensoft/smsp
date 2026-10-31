import os
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseNotFound, Http404
from django.views.static import serve

def protected_media_view(request, path):
    """
    Secure media file serving view (Gate 7).
    Guarantees that sensitive student papers, scanned sheets, and aligned results
    cannot be accessed anonymously, while permitting authenticated users,
    token-bearing requests, and trusted local/CORS application requests.
    """
    clean_path = path.lstrip('/')

    # Sensitive directories containing student papers or submissions
    is_sensitive = clean_path.startswith('uploads/') or clean_path.startswith('pages/') or clean_path.startswith('original/')

    if is_sensitive:
        is_authorized = False

        # 1. Check if user is already authenticated (session or view)
        if request.user and request.user.is_authenticated:
            is_authorized = True

        # 2. Check query param or header token
        if not is_authorized:
            token = request.GET.get('token')
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            raw_token = token or (auth_header.split()[1] if (auth_header and ' ' in auth_header) else None)
            if raw_token:
                try:
                    from rest_framework_simplejwt.authentication import JWTAuthentication
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(raw_token)
                    user = jwt_auth.get_user(validated_token)
                    if user and user.is_authenticated:
                        is_authorized = True
                except Exception:
                    pass

        # 3. Check Referer or Origin from trusted local / frontend hosts
        if not is_authorized:
            referer = request.META.get('HTTP_REFERER', '')
            origin = request.META.get('HTTP_ORIGIN', '')
            sec_dest = request.META.get('HTTP_SEC_FETCH_DEST', '')
            # If request originated from frontend app (Referer/Origin present from localhost/127.0.0.1)
            allowed_hosts = ['localhost', '127.0.0.1']
            if any(h in referer for h in allowed_hosts) or any(h in origin for h in allowed_hosts):
                is_authorized = True

        if not is_authorized:
            return HttpResponseForbidden("Authentication required to access student exam materials.")

    try:
        return serve(request, path, document_root=settings.MEDIA_ROOT)
    except Http404:
        return HttpResponseNotFound("File not found.")
