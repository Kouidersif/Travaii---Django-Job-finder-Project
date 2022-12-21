
from django.shortcuts import redirect





def notLogged(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_company:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_page')
    return wrapper_func 


def only_non_authenticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('error_page')
        elif not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
    return wrapper_func