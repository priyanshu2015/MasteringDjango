from django.core.exceptions import PermissionDenied
class CheckPremiumGroupMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name = "premium").exists():
            #return True
            return super().dispatch(request, *args, **kwargs)

        else:
            raise PermissionDenied