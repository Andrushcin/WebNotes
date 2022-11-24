from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user
from django.contrib import messages

# Обновляем объект Note данными полезной нагрузки
def add_data_from_payload(note, payload):
    if 'name' in payload.keys():
        note.name = payload['name']

    if 'text' in payload.keys():   
        note.text = payload['text']

    if 'favourites' in payload.keys():
        note.favourites = bool(payload['favourites'])
    
    if 'date_missing' in payload.keys():
        if payload['date_missing'] != "":
            note.date_to_trash = payload['date_missing']
    
    note.save()
    return note

# Получаем объект User, если это авторизованный пользователь
# Либо получаем Session, если пользователь не авторизован
def get_instance(request):
    if isinstance(get_user(request), AnonymousUser):
        if request.session.session_key == None:
            request.session.cycle_key()
        
        return Session.objects.get(session_key = request.session.session_key)
    else:
        return get_user(request)

# Получаем все объекты Note для зарегистрированного пользователя
# или текущей сессии, если пользователь не авторизован
def get_notes_for_user(instance, sort_params):
    order_by_param = sort_params["order_by"]
    if not sort_params["reverse"]:
        order_by_param = "-" + sort_params["order_by"]

    return instance.note_set.all().order_by(order_by_param)

def get_sort_param(request, available_sort_params):
    params = request.GET
    reverse = False
    order_by = 'date_update'

    if 'sort' in params.keys():
        if params['sort'] in available_sort_params:
            order_by = params['sort']

    if 'reverse' in params.keys():
        if params['reverse'] == "true":
            reverse = True
    
    return {"order_by": order_by,
            "reverse": reverse}

# Функция необходима для отображения способа сортировки на странице
def get_select_param(sort_param, available_sort_params):
    select_param = {}
    for var in available_sort_params:
        if var == sort_param["order_by"]:
            select_param[var] = "selected"
        else:
            select_param[var] = ""
    return select_param

# Декоратор для уведомления неавторизованных пользователей
def message_for_anonymous(func_get):
    def get(self, request, *args, **kwargs):
        if isinstance(get_user(request), AnonymousUser):
            message = "Внимание! Вы не авторизованы в системе, поэтому при завершении сеанса вы потеряете доступ к своим заметкам."
            messages.warning(request, message)
        return func_get(self, request, *args, **kwargs)
    return get
