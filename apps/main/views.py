from django.shortcuts import render, redirect
from django.views import View
import requests

URL = 'https://nuranov04.pythonanywhere.com/api/'


class GetForm(View):
    def get(self, request):
        form = requests.request('get', URL + 'form/')
        lst_forms = form.json()
        return render(request, 'include/all_forms.html', locals())


class FormDetail(View):
    def get(self, request, form_uid, id):
        form = requests.request('get', URL + 'form/{}/'.format(id))
        data = form.json()
        questions = data['question']
        selects = []  # лист для списка ответов
        for question in questions:
            for select in question['select']:
                for select_answer in question['question_select_answers']:
                    if select_answer['select'] == select['id']:
                        selects.append(select['select'])
        return render(request, 'include/detail.html', locals())


def fill_in(request, id, form_uid):
    form = requests.request('get', URL + 'form/{}/'.format(id))
    data = form.json()
    questions = data['question']
    if request.method == "POST":
        for question in questions:
            text = request.POST.get('{}'.format(question['id']))
            dict = {
                'input': text,
                'question': question['id']
            }
            create_answer = requests.post(URL + 'answer/', dict)
            if question['type'] == 'select':
                select = request.POST.get('select')
                select_dict = {
                    'select': select,
                    'question': question['id']
                }
                create_select_answer = requests.post(URL + 'select_answer/', select_dict)
        return redirect('index')
    return render(request, 'include/form_fillin.html', locals())
