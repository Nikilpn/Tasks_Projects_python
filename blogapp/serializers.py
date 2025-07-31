from rest_framework import serializers
from blogapp.models import User,Blog,BlogReport,BlacklistedUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68,write_only=True,min_length=3)
    confirm_password=serializers.CharField(max_length=68,write_only=True,min_length=3)
    
    class Meta:
        model=User
        fields=['email','password','confirm_password']
        

        
    def validate(self,attrs):
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if password!=confirm_password:
            raise serializers.ValidationError('password do not match')
        validate_password(password)
        return attrs
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, write_only=True)  
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate(self, attrs):
        user_email = attrs.get('email', '')
        user_password = attrs.get('password', '')
        
        # print(f"my email is    ===={user_email}")
        # print(f"my password is ===={[user_password]}")
        
        if user_email and user_password:
            user=authenticate(email=user_email,password=user_password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials, try again')
            if not user.is_active:
                raise serializers.ValidationError('suspeneded user')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')
     

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        # fields = ['title', 'description', 'image', 'video']
        fields='__all__'
        # exclude = ['owner']
        extra_kwargs={
            'owner':{'read_only':True}
        }

class BlogReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlogReport
        fields=['id','blog','reported_by','reason','description','created_at']
        extra_kwargs={
            'reported_by':{'read_only':True}
        }
# class BlacklistUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlacklistedUser
#         fields = ['id', 'user', 'reason', 'blacklisted_at']
#         extra_kwargs = {
#             'blacklisted_by': {'read_only': True}
#         }
        
    

                  
   