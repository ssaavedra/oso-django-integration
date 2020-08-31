import json

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

from django_oso.auth import authorize

from expenses.models import Expense

def get_expense(request, id):
    try:
        expense = Expense.objects.get(pk=id)
    except Expense.DoesNotExist:
        return HttpResponseNotFound()

    authorize(request, expense, actor=request.current_user, action="read")
    return HttpResponse(expense.json())

@require_http_methods(["PUT"])
def submit_expense(request):
    expense_data = json.loads(request.body)

    expense_data.setdefault("user_id", request.current_user.id)

    expense = Expense.from_json(expense_data)
    expense.save()

    return HttpResponse(json.dumps(expense.json()))
