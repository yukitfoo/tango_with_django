from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User



class CategoryForm(forms.ModelForm):
    # to make sure it must have a name and name is unique
    # add required = True and unique = True
    name = forms.CharField(max_length=Category.name_max_length, help_text = "Please enter the category name.", required = True)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    slug = forms.CharField(widget=forms.HiddenInput(), required = False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.title_max_length, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=Page.url_max_length, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # if url is not empty and doesnt start with http://
        # prepend http
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        # must always return this
        return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
