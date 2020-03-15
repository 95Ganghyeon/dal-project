from allauth.account.views import PasswordChangeView

class CustomPasswordChangeView(PasswordChangeView):
    success_url = '/user/profile/edit' # <- password_change redirect url