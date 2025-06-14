from rest_framework import serializers
from account.models import User
from django.contrib.auth.hashers import make_password
from .validators import is_valid_iranian_national_id


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'bio', 'latitude', 'longitude']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)

class TeacherRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'national_id']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'national_id': {'required': True},
        }

    def validate_national_id(self, value):
        if not is_valid_iranian_national_id(value):
            raise serializers.ValidationError("Invalid Iranian national ID.")
        return value
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already registered.")
        return value
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['role'] = 'teacher'
        validated_data['is_active'] = False
        return User.objects.create(**validated_data)

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'national_id', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'national_id': {'required': True},
            'password': {'write_only': True, 'required': True},
        }

    def validate_national_id(self, value):
        if not is_valid_iranian_national_id(value):
            raise serializers.ValidationError("Invalid Iranian national ID.")
        if User.objects.filter(username=value).exists():  # national_id is used as username
            raise serializers.ValidationError("This national ID is already registered.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['role'] = 'student'
        validated_data['username'] = validated_data['national_id']
        validated_data['is_active'] = False
        return User.objects.create(**validated_data)



class AddStudentByTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'national_id', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'national_id': {'required': True},
            'password': {'write_only': True, 'required': True},
        }

    def validate_national_id(self, value):
        if not is_valid_iranian_national_id(value):
            raise serializers.ValidationError("Invalid Iranian national ID.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This national ID is already registered.")
        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['national_id']
        validated_data['role'] = 'student'
        validated_data['is_active'] = True  
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)



class TeacherProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'role', 'bio', 'latitude', 'longitude','national_id']
        read_only_fields = ['username', 'national_id', 'role']
