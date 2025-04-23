# core/middleware.py

from django.shortcuts import redirect

class TempPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            if getattr(user, 'used_temp_password', False) and request.path != '/change-password/':
                return redirect('change_password')
        return self.get_response(request)
