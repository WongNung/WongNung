from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models.review import Review
from ..models.report import Report


@login_required
def report(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect(
                "wongnung:report-modal-cancel",
                pk=pk,
            )
        content = request.POST["report-content"].strip()
        if not content:
            return redirect("wongnung:report-modal", pk=pk)
        report = Report.objects.create(
            review=review, user=request.user, content=content
        )
        report.save()
    return HttpResponseRedirect(
        reverse("wongnung:review-component", args=(review.pk,))
    )


@login_required
def show_report_modal(request, pk, cancel=""):
    review = get_object_or_404(Review, pk=pk)
    context = {"review": review}
    if cancel:
        context["cancel"] = True
    return render(request, "wongnung/report_modal_component.html", context)
