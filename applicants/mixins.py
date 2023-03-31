from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect



class CompanyAndLogin(AccessMixin):
    """Verify that the current user is authenticated and is a company"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_company:
            return redirect('error_page')
        return super().dispatch(request, *args, **kwargs)



class MustbeUnauthenticated(AccessMixin):
    """Verify that the current user is NOT authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('error_page')
        return super().dispatch(request, *args, **kwargs)
    



class ApplicantsAccess(AccessMixin):
    """Verify that the current user is authenticated and is an applicant"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_applicant:
            return redirect('error_page')
        return super().dispatch(request, *args, **kwargs)