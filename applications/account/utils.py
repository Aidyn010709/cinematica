from django.core.mail import send_mail


def send_activation_code(email, code):

    send_mail(
        'Py29',
        f'Привет перейди по этой ссылке что бы активировать аккаунт'
        f': \n\n http://localhost:8000/api/account/activate/{code}',
        'sassassas107@gmail.com',
        [email]
    )


def send_activate(email, code):

    send_mail(
        'Сообщение о том что вы сменили пароль',
        'Вы успешно сменили пароль',
        'sassassas107@gmail.com',
        [email],
        fail_silently=False,
    )


