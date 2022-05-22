from django.urls import path
from apps.main.views import GetForm, FormDetail, fill_in

urlpatterns = [
    path('', GetForm.as_view(), name='index'),
    path('fill_in/<int:id>.<str:form_uid>/', fill_in, name='fill_in'),
    path('detail/<int:id>.<str:form_uid>/', FormDetail.as_view(), name='detail'),
]
