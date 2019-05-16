from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile

# 회원정보수정
class CustomUserChangeForm(UserChangeForm):
    class Meta():
        model = get_user_model()
        fields = ['first_name', 'last_name']

# 회원가입
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
        
# 프로필
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'introduction',]

