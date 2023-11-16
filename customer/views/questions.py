from django.shortcuts import redirect, render
from insurance import forms as CFORM
from insurance import models as CMODEL

from .. import forms, models

def ask_question_view(request):
    """Ask question view"""
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm = CFORM.QuestionForm()

    if request.method == "POST":
        questionForm = CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = customer
            question.save()
            return redirect("question-history")
    return render(
        request,
        "customer/ask_question.html",
        {"questionForm": questionForm, "customer": customer},
    )


def question_history_view(request):
    """Get question view"""
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(
        request,
        "customer/question_history.html",
        {"questions": questions, "customer": customer},
    )
