from django.forms import ModelForm
from .models import*
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django .contrib.auth.models import User

class updateForm(ModelForm):
    class Meta:
        model = SiteName
        fields = ('primry_name',)

class updateFormImage(ModelForm):
    class Meta:
        model = SiteImage
        fields = ('logoImage',)

choices = Category.objects.all().values_list('name','name')
#status_choice =(('Draft','Draft'), ('Published','Published'),)
choice_list = []

for item in choices:
    choice_list.append(item)

class addProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'price', 'strike_out_price', 'image', 'description','quantity', 'status',)

        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control form-input','placeholder':'Product name'}),
            'category' : forms.Select(choices=choice_list, attrs={'class':'form-control form-input','placeholder':'Category'}),
            'status' : forms.RadioSelect(attrs={'class':'radio-button'}),
            'quantity' : forms.TextInput(attrs={'class':'form-control form-input','placeholder':'Quantity'}),
            'strike_out_price' : forms.TextInput(attrs={'class':'form-control form-input','placeholder':'Marked Price'}),
            'price' : forms.TextInput(attrs={'class':'form-control form-input','placeholder':'Product price'}),
            'image':forms.ClearableFileInput(attrs={'class':'image-btn '}),
            'description' : forms.Textarea(attrs={'class':'form-control form-input','placeholder':'Product description'}),
        }

class addCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields =('name',)

        widgets= {
            'name' : forms.TextInput(attrs={'class':'form-control'}),

        }