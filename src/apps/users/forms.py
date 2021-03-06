# Django Imports
from django import forms

# Local Imports
from .models import User, ResidentProfile, WatchmanProfile


class SignUpForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=50,
        label='Nombre de Usuario'
    )
    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(),
        label='Correo Electrónico'
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(),
        label='Contraseña'
    )
    password_confirmation = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(),
        label='Confirme su Contraseña'
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        label='Nombre(s)'
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        label='Apellido(s)'
    )
    RESIDENT = 1
    WATCHMAN = 2
    ROLE_CHOICES = (
        (RESIDENT, 'Residente'),
        (WATCHMAN, 'Vigilante'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='¿Cúal es tú rol?'
    )
    phone_number = forms.CharField(
        min_length=7,
        max_length=50,
        required=False,
        label='Teléfono'
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return data

    def save(self):
        """Create base_user and its profile-role"""
        data = self.cleaned_data
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        role_chosen = int(data['role'])

        if role_chosen == self.RESIDENT:
            res_prof = ResidentProfile(user=user)
            res_prof.save()
        else:
            wat_prof = WatchmanProfile(user=user)
            wat_prof.save()


class ResidentProfileUpdateForm(forms.ModelForm):
    """ Docstring """
    OWNER = 1
    TENANT = 2
    RELATION_W_PROPERTY = (
        (OWNER, 'PROPIETARIO'),
        (TENANT, 'ARRENDATARIO'),
    )
    property_relation = forms.ChoiceField(
        choices=RELATION_W_PROPERTY,
        label='Relación con el immueble.'
    )
    class Meta:
        model = ResidentProfile
        exclude = ['user']


class WatchmanProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = WatchmanProfile
        exclude = ['user']
