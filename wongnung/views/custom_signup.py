from allauth.account.views import SignupView
from django.shortcuts import redirect

class CustomSignupView(SignupView):
    def form_valid(self, form):
        # Call the parent form_valid method
        super().form_valid(form)
        # Redirect to the privacy policy confirmation page
        return redirect("wongnung:privacy-policy")
