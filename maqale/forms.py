from django import forms
from .models import Comment
from .models import RegisteredUser
from django.core.exceptions import ValidationError
import re



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'کامنت خود را بنویسید...'}),
        }



class UserRegisterForms(forms.Form):
    user_name = forms.CharField(max_length=50, label='نام کاربری')
    email = forms.EmailField(label='ایمیل')
    password_1 = forms.CharField(max_length=50, label='رمزعبور', widget=forms.PasswordInput)
    password_2 = forms.CharField(max_length=50, label='تکرار رمزعبور', widget=forms.PasswordInput)
   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user_name'].widget.attrs.update({
            'placeholder': 'نام کاربری',
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'ایمیل',
            'class': 'form-control'
        })
        self.fields['password_1'].widget.attrs.update({
            'placeholder': 'رمز عبور',
            'class': 'form-control'
        })
        self.fields['password_2'].widget.attrs.update({
            'placeholder': 'تکرار رمز عبور',
            'class': 'form-control'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if RegisteredUser.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است")
        return email
    

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if RegisteredUser.objects.filter(user_name=user_name).exists():
            raise ValidationError("این نام کاربری قبلاً ثبت شده است")
        return user_name


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password_1")
        password2 = cleaned_data.get("password_2")

        if password1 != password2:
            raise ValidationError("رمزها با هم مطابقت ندارند")