from rest_framework import serializers


class AddUserSerializer(serializers.Serializer):
    name = serializers.CharField(help_text='Введите имя пользователя.')
    email = serializers.EmailField(help_text='Введите почту пользователя.')


class UserIdSerializer(serializers.Serializer):
    user_id = serializers.CharField(help_text='Введите id пользователя.')


class UpdateUserSerializer(UserIdSerializer):
    name = serializers.CharField(help_text='Введите имя пользователя.',
                                 required=False)
    email = serializers.EmailField(help_text='Введите почту пользователя.',
                                   required=False)
