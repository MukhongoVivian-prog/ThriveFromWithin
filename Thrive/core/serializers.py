# core/serializers.py

from rest_framework import serializers
from .models import Affirmation, Material, Scene, Sound, User, Company
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'company_name']


class RegisterSerializer(serializers.ModelSerializer):
    # Fields for company creation (for admin)
    company_name = serializers.CharField(required=False)
    company_bio = serializers.CharField(required=False)
    company_country = serializers.CharField(required=False)
    company_email = serializers.EmailField(required=False)
    company_work_environment = serializers.JSONField(required=False)
    company_challenges = serializers.JSONField(required=False)
    company_num_of_employees = serializers.IntegerField(required=False)
    company_code = serializers.CharField(required=False)
    # Field for regular user registration
    company_code_input = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'role', 'first_name', 'last_name', 'username','mood',
            'company_name', 'company_bio', 'company_country', 'company_email',
            'company_work_environment', 'company_challenges', 'company_num_of_employees', 'company_code',
            'company_code_input'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True},
        }

    def validate(self, attrs):
        # Skip validation if this is an update operation
        if self.instance is not None:
            return attrs
            
        role = attrs.get('role', 'employee')
        if role == 'admin':
            # Company admin must provide all company fields
            required_fields = ['company_name', 'company_country', 'company_email', 'company_code',"company_work_environment","company_challenges"]
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field} is required for company admin registration.")
        else:
            # Regular users must provide company_code_input
            if not attrs.get('company_code_input'):
                raise serializers.ValidationError("company_code_input is required for regular user registration.")
        return attrs

    def create(self, validated_data):
        role = validated_data.get('role', 'employee')
        if role == 'admin':
            # Extract company fields
            company_data = {
                'name': validated_data.pop('company_name'),
                'bio': validated_data.pop('company_bio',""),
                'country': validated_data.pop('company_country'),
                'email': validated_data.pop('company_email'),
                'work_environment': validated_data.pop('company_work_environment', []),
                'challenges': validated_data.pop('company_challenges', []),
                'code': validated_data.pop('company_code'),
                'num_of_employees': validated_data.pop('company_num_of_employees', 1),
            }
            company = Company.objects.create(**company_data)
            validated_data['company'] = company
        else:
            # Regular user: link to existing company by code
            company_code = validated_data.pop('company_code_input')
            try:
                company = Company.objects.get(code=company_code)
            except Company.DoesNotExist:
                raise serializers.ValidationError({"company_code_input": "Invalid company code."})
            validated_data['company'] = company
        validated_data['username'] = validated_data['email']
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Update user fields
        # Add company_code_input if not present
        if 'company_code_input' not in validated_data:
            validated_data['company_code_input'] = instance.company.code if instance.company else None

        # Update username if email changes
        if 'email' in validated_data:
            validated_data['username'] = validated_data['email']
        # Update password if provided
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        # If admin and company fields are present, update company
        if instance.role == 'admin' and instance.company:
            company_fields = [
                'company_name', 'company_bio', 'company_country', 'company_email',
                'company_work_environment', 'company_challenges', 'company_num_of_employees', 'company_code'
            ]
            company = instance.company
            updated = False
            for field in company_fields:
                if field in validated_data:
                    model_field = field.replace('company_', '')
                    setattr(company, model_field, validated_data.pop(field))
                    updated = True
            if updated:
                company.save()

        return super().update(instance, validated_data)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
        })
        return data


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ["title","option","id"]

class SoundSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()
    class Meta:
        model = Sound
        fields = ["title","picture","tag","audio","id"]

        def get_picture(self,obj):
            try:
                return obj.picture.url
            except:
                return None
            
class SceneSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    class Meta:
        model = Scene
        fields = ["title","description","id","file"]
    
    def get_file(self,obj):
        try:
            return obj.file.url
        except:
            return None
        

class AffirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affirmation
        fields =["quote","by","id"]

class TherapistSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["first_name","last_name","image","rating","title","bio","id"]

    def get_image(self,obj):
        try:
            return obj.image.url
        except:
            return None