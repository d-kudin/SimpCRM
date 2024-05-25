from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imie'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Nazwa użytkownika'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Wymagany. 150 znaków lub mniej. Tylko litery, cyfry i @/./+/-/_.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Hasło'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Twoje hasło nie może być zbyt podobne do innych Twoich danych osobowych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li><li>Twoje hasło nie może być powszechnie używanym hasłem</li><li>Twoje hasło nie może być w całości numeryczne.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Potwierdź hasło'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Wprowadź to samo hasło co poprzednio w celu weryfikacji.</small></span>'	



# Utworzenie formularza dodawania klienta
class AddRecordForm(forms.ModelForm):
	imie = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Imię", "class":"form-control"}), label="")
	nazwisko = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nazwisko", "class":"form-control"}), label="")
	email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
	nr_telefonu = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nr telefonu", "class":"form-control"}), label="")
	adres = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Adres", "class":"form-control"}), label="")
	miasto = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Miejscowość", "class":"form-control"}), label="")
	wojewodztwo = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Województwo", "class":"form-control"}), label="")
	kod_pocztowy = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Kod pocztowy", "class":"form-control"}), label="")

	class Meta:
		model = Record
		exclude = ("user",)