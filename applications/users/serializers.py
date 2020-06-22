from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer

from applications.users.models import User


class UserSerializer(UserDetailsSerializer):
    gender = serializers.ChoiceField(choices=User.Gender.choices, required=True)
    name = serializers.CharField(required=True, max_length=250)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'gender']


class RestAuthLoginSerializer(LoginSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class RestAuthRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    gender = serializers.ChoiceField(choices=User.Gender.choices, required=True)
    name = serializers.CharField(required=True, max_length=250)

    def get_cleaned_data(self):
        super(RestAuthRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            }
