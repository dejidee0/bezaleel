from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def verified_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_verified:
                # Redirect to a "verification required" page or return a 403 error
                return redirect('/')  # Define this URL in your app
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')  # Redirect to login if not authenticated
    return wrapper
