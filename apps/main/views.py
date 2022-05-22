from django.shortcuts import render, redirect
from django.views import View
import requests

URL = 'https://nuranov04.pythonanywhere.com/api/'


class GetForm(View):
    def get(self, request):
        # кидаем GET запрос на апи и получаем все формы
        form = requests.request('get', URL + 'form/')
        # получаем словарь из ответа для работы
        lst_forms = form.json()
        return render(request, 'include/all_forms.html', locals())


#  Класс для вывода информации для каждой формы
class FormDetail(View):
    def get(self, request, form_uid, id):
        #  отпправляем Get запрос на апи и получаем данные каждой формы
        form = requests.request('get', URL + 'form/{}/'.format(id))
        # для работы нам нужно получить dict
        data = form.json()
        print(type(data))
        questions = data['question']
        selects = []  # лист для списка ответов
        for question in questions:
            #  итерритуемся по селекту вопроса
            for select in question['select']:
                # итеррируемся по селекту которые выбирали пользователи
                for select_answer in question['question_select_answers']:
                    # сравниваем 'id' селекта и 'id' селекта который выбирал пользователь
                    if select_answer['select'] == select['id']:
                        # добавляем в лист по которму в дальнейшем будем иттерироваться 
                        selects.append(select['select'])
        return render(request, 'include/detail.html', locals())


def fill_in(request, id, form_uid):
    # берем форму по "id"
    form = requests.request('get', URL + 'form/{}/'.format(id))
    # получаем lst со всеми данными формы
    data = form.json()
    #  берем все вопросы определенной формы
    questions = data['question']
    if request.method == "POST":
        # итерируемся по всем вопросам
        for question in questions:
            #  получаем данные из шаблона с помощью jonja тегов
            text = request.POST.get('{}'.format(question['id']))
            dict = {
                'input': text,
                'question': question['id']
            }
            # отправляем POST запрос на нашу апи
            create_answer = requests.post(URL + 'answer/', dict)
            # нам нужно взять селект отдельно. Из-за того что у нас не multiselect
            # я сделал name='select'статичным. Нам нужно только одно значение
            if question['type'] == 'select':
                select = request.POST.get('select')
                select_dict = {
                    'select': select,
                    'question': question['id']
                }
                # отправляем POST запрос на нашу апи
                create_select_answer = requests.post(URL + 'select_answer/', select_dict)
        return redirect('index')
    return render(request, 'include/form_fillin.html', locals())
