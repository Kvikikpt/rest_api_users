from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .json_data_actions import create_user,\
    get_users,\
    get_user_by_id,\
    update_user,\
    delete_user

from .serializers import AddUserSerializer, UpdateUserSerializer, UserIdSerializer

from user_api.exeptions import NoUserIdFound


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'Add user': reverse('add-user', request=request, format=format),
        'Get users': reverse('get-users', request=request, format=format),
        'Get user by id': reverse('get-user-by-id', request=request,
                                  format=format),
        'Update user by id': reverse('update-user-by-id',
                                     request=request, format=format),
        'Delete user by id': reverse('delete-user-by-id',
                                     request=request, format=format),
    })


class AddUserView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AddUserSerializer

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK,
                            data={'data': 'Posted data is invalid'})
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return response

        request_data = serializer.validated_data
        user_name = request_data['name']
        email = request_data['email']

        try:
            create_user(user_name, email)
            return Response(status=status.HTTP_200_OK,
                            data={'status': f'User \'{user_name}\' was created'})
        except Exception as e:
            print(f'Error occurred while adding user. Error: {e}')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'An error occurred'})


class UserListView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_400_BAD_REQUEST, )
        try:
            users_list = get_users()
            return Response(status=status.HTTP_200_OK,
                            data={'users': users_list})
        except Exception as e:
            print(f'Error occurred while getting users list. Error: {e}')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'An error occurred'})


class UserIdView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserIdSerializer

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK,
                            data={'data': 'Posted data is invalid'})
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return response

        request_data = serializer.validated_data
        user_id = request_data['user_id']
        try:
            user = get_user_by_id(user_id)
            return Response(status=status.HTTP_200_OK,
                            data={user_id: user})
        except NoUserIdFound:
            print(f'Not found user id')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'Id not found'})
        except Exception as e:
            print(f'Error occurred while getting user by id. Error: {e}')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'An error occurred'})


class UserIdUpdateView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UpdateUserSerializer

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK,
                            data={'data': 'Posted data is invalid'})
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return response

        request_data = serializer.validated_data
        user_id = request_data['user_id']

        try:
            user = update_user(user_id, request_data)
            return Response(status=status.HTTP_200_OK,
                            data={user_id: user})
        except NoUserIdFound:
            print(f'Not found user id')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'Id not found'})
        except Exception as e:
            print(f'Error occurred while getting update user. Error: {e}')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'An error occurred'})


class UserDeleteView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = UserIdSerializer

    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_200_OK,
                            data={'data': 'Posted data is invalid'})
        serializer = self.serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return response

        request_data = serializer.validated_data
        user_id = request_data['user_id']
        try:
            delete_user(user_id)
            return Response(status=status.HTTP_200_OK,
                            data={'Status': f'Ok, user {user_id} '
                                            f'was deleted'})
        except NoUserIdFound:
            print(f'Not found user id')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'Id not found'})
        except Exception as e:
            print(f'Error occurred while deleting user. Error: {e}')
            return Response(status=status.HTTP_200_OK,
                            data={'Error': 'An error occurred'})
