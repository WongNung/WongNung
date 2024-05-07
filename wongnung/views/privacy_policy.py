from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from wongnung.models.privacy_policy import PrivacyPolicy

@login_required
def privacy_policy_confirm(request):
    user = request.user
    if request.method == 'POST':
        agree = request.POST.get('agree')
        if agree:
            PrivacyPolicy.objects.update_or_create(user=user, defaults={'agreed': True})
            return redirect("wongnung:feed") # Redirect to home page after agreement
        else:
            # Handle case where user did not agree
            return render(request, 'wongnung/privacy_policy_confirm.html', {'error': 'Please agree to the privacy policy'})

    return render(request, 'wongnung/privacy_policy_confirm.html')
