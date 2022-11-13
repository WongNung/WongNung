from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from wongnung.globals import htmx_endpoint_with_auth
from wongnung.insights import UserUpvotesReview

from ..models.review import Review
from . import user_insights


@htmx_endpoint_with_auth
@login_required
def vote(request, pk):
    """An endpoint to set user's vote on a specific review."""
    review = get_object_or_404(Review, pk=pk)
    user = request.user

    if request.POST.get("up"):  # When user upvotes
        if review.upvotes.filter(id=user.id).exists():
            review.remove_upvotes(request.user)
        else:
            review.add_upvotes(request.user)
            review.remove_downvotes(request.user)
        user_insights.push(user, UserUpvotesReview(review.film, review))

    if request.POST.get("down"):  # When user downvotes
        if review.downvotes.filter(id=user.id).exists():
            review.remove_downvotes(request.user)
        else:
            review.add_downvotes(request.user)
            review.remove_upvotes(request.user)

    review.save()
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,))
    )
