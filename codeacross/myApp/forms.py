from django import forms
from myApp.models import Category, Page

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # An inline class to provide additional information on the form.
    class Meta:
        # provide an association between the ModelForm and a model
        model = Category

class PageForm(forms.ModelForm):
    # category = models.ForeignKey(Category)
    title = forms.CharField(max_length=128, help_text="Please enter the page name.")
    url = forms.URLField(max_length=300, help_text="Please enter the URL.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # An inline calss to provide additional information on the form.
    class Meta:
        # provide an association between the ModelForm and a model
        model = Page

        # What fields do we sant to include in our form?
        # This way we don't need every field in the model prosent.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('rul')  

        # if url is not empty and doesn't arart with 'http://', prepend 'http://'. 
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data             