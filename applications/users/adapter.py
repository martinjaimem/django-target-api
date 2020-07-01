from allauth.account.adapter import DefaultAccountAdapter


class UserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.name = data.get('name')
        user.gender = data.get('gender')

        super().save_user(request, user, form, commit)
