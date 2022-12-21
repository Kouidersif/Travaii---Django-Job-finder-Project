
from django.shortcuts import redirect





def notApplicant(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_applicant:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_page')
    return wrapper_func 

