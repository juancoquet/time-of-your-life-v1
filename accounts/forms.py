from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ValidationError, DateInput, widgets
from django.utils import timezone
from datetime import date

from countdown.forms import FUTURE_DOB_ERROR, PAST_DOB_ERROR, FUTURE_DOB_ERROR, get_today_minus_90_years


EVENT_OUT_OF_RANGE_ERROR = "Your new date of birth would cause some of your life events" \
    "to be out of range."


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'dob',)
        widgets = {'dob': DateInput(attrs={"class": "datepicker"})}

    def clean_dob(self, *args, **kwargs):
        dob_given = self.cleaned_data['dob']
        if dob_given >= timezone.now().date():
            raise ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years().date():
            raise ValidationError(PAST_DOB_ERROR)
        else:
            return dob_given


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'dob',)
        widgets = {'dob': DateInput(attrs={"class": "datepicker"})}

    def clean_dob(self, *args, **kwargs):
        dob_given = self.cleaned_data['dob']
        if dob_given >= timezone.now().date():
            raise ValidationError(FUTURE_DOB_ERROR)
        if dob_given < get_today_minus_90_years().date():
            raise ValidationError(PAST_DOB_ERROR)
        else:
            return dob_given

    def show_event_out_of_range_error(self):
        self.errors['dob'] = EVENT_OUT_OF_RANGE_ERROR
