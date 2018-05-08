from django import forms
from django.db import connections


def sql_branch():
    query = "select id, description from products where parent_id is null;"
    # query.format('products')
    print(query)
    return query


def load_branch():
    with connections['colplan'].cursor() as cursor:
        query = sql_branch()
        cursor.execute(query)

        branch_items = cursor.fetchall()

    # return HttpResponse(template.render(context, request))
    return branch_items


class BranchForm(forms.Form):
    # branch_item = forms.ChoiceField(choices = [(1,'oi'), (2,'ola'), (3,'maravilha')])
    choices = load_branch()
    branch_item_level_1 = forms.ChoiceField(choices = choices)
    branch_item_level_2 = forms.ChoiceField(choices=[])
    branch_item_level_3 = forms.ChoiceField(choices=[])
    branch_item_level_4 = forms.ChoiceField(choices=[])
    identifier = 'products'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.identifier)
        self.branch_items = load_branch()

