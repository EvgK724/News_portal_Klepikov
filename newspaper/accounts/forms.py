from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.core.exceptions import PermissionDenied
from portal.models import Author


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name="authors")
        user.groups.add(authors)
        Author.objects.create(author_user=User.objects.get(pk=user.id))
        return user


# class OwnerPermissionRequiredMixin(PermissionRequiredMixin):
#     def has_permission(self):
#         perms = self.get_permission_required()
#         if not self.get_object().author.author_user == self.request.user:
#             raise PermissionDenied()
#         return self.request.user.has_perms(perms)