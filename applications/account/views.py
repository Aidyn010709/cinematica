from applications.account.serializers import RegisterSerializer
from applications.account.utils import send_activate
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model, update_session_auth_hash


User = get_user_model()


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегистрировались. Вам отправлено письмо на почту код с активацией', status=201)


class ActivationAPIView(APIView):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
        except:
            return Response('Нет такого кода!:', status=400)
        user.is_active = True
        user.activation_code = ''
        user.save(update_fields=['is_active', 'activation_code'])
        return Response('Успешно', status=200)


class ChangePasswordAPIView(APIView):

    def post(self, request):

        email = request.data.get('email', '')
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('Пользователь с такой почтой не найден', status=404)
        if not user.check_password(current_password):
            return Response('Неверный текущий пароль', status=400)
        if len(new_password) < 6:
            return Response('Новый пароль должен содержать не менее 6 символов', status=400)

        user.set_password(new_password)
        user.save()
        send_activate(user.email, user.activation_code)
        update_session_auth_hash(request, user)
        return Response('Пароль успешно изменен', status=200)



