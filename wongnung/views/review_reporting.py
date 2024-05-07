import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..globals import htmx_endpoint_with_auth
from ..insights import UserReportsReview

from . import user_insights
from ..models.report import Report
from ..models.review import Review

logging = logging.getLogger(__name__)

@htmx_endpoint_with_auth
@login_required
def report(request, pk):
    """An endpoint for saving a new report."""
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        if "cancel" in request.POST:
            return set_report_modal_state(request, pk=pk, cancel=True)
        content = request.POST["report-content"].strip()
        if not content:
            logger.warning(f"Failed to submit report for review {pk} by user {request.user.username}: Empty report content.")
            return set_report_modal_state(request, pk=pk)
        report = Report.objects.create(
            review=review, user=request.user, content=content
        )
        report.save()
        logger.info(f"Report submitted for review {pk} by user {request.user.username}.")

    user_insights.push(request.user, UserReportsReview(review.film, review))
    return set_report_modal_state(request, pk=pk, cancel=True)


@htmx_endpoint_with_auth
@login_required
def set_report_modal_state(request, pk, cancel: bool = False):
    """An endpoint for frontend to show/hide report modal."""
    review = get_object_or_404(Review, pk=pk)
    context = {"review": review}
    if cancel:
        context["cancel"] = True
    return render(request, "wongnung/report_modal_component.html", context)
