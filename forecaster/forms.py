from django import forms
from django.db import connections


def sql_branch(identifier):
    query = "select id, description from %s where parent_id is null;"
    query = query % identifier
    # query.format('products')
    print(query)
    return query


def load_branch(identifier):
    with connections['colplan'].cursor() as cursor:
        query = sql_branch(identifier)
        cursor.execute(query)

        branch_items = cursor.fetchall()

    # return HttpResponse(template.render(context, request))
    return branch_items


class BranchForm(forms.Form):
    # branch_item = forms.ChoiceField(choices = [(1,'oi'), (2,'ola'), (3,'maravilha')])

    # branch_item_level_1 = forms.ChoiceField(choices = [(1,'------')]+choices)
    # branch_item_level_1 = forms.ChoiceField(choices = [])
    # branch_item_level_2 = forms.ChoiceField(choices=[])
    # branch_item_level_3 = forms.ChoiceField(choices=[])
    # branch_item_level_4 = forms.ChoiceField(choices=[])
    identifier = ''

    def __init__(self, identifier='products', level=4, *args, **kwargs):
        self.identifier = identifier
        self.branch_items = load_branch(self.identifier)
        print('que legal %s' % level)
        super().__init__(*args, **kwargs)
        self.fields[self.identifier+'_branch_item_level_1'] = forms.ChoiceField(choices=[])
        self.fields[self.identifier+'_branch_item_level_1'].choices = [("",'------')] + self.branch_items
        for i in range(2, level+1):
            level_name = '_branch_item_level_%s' % i
            self.fields[self.identifier + level_name] = forms.ChoiceField(choices=[])
        # self.fields[self.identifier + '_branch_item_level_2'] = forms.ChoiceField(choices=[])
        # self.fields[self.identifier + '_branch_item_level_3'] = forms.ChoiceField(choices=[])
        # self.fields[self.identifier + '_branch_item_level_4'] = forms.ChoiceField(choices=[])


