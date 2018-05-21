from django import forms
import datetime
import re


class FeedbackForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")
    message_text = forms.CharField(widget=forms.Textarea, max_length=500, label="Comment")


class OnboardingForm(forms.Form):

    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    gender = forms.CharField()
    birthdate = forms.DateField(input_formats=['%Y/%m/%d', '%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d'], initial=datetime.date.today)

    tags = forms.ModelMultipleChoiceField(validators=[])

    occupation = forms.CharField()
    city = forms.CharField()
    statement = forms.CharField()
    twitter_username = forms.CharField()

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')

        if tags == 'undefined' or tags == None or tags == '':
            raise forms.ValidationError("You must provide at least one tag.")
        self.data['tags'] = [{'name': x.lower().capitalize()} for x in tags.split(",")]

class ProfileForm(OnboardingForm):

    twitter_username = None
    profile_img = forms.CharField(required=False)

    size = forms.CharField(required=False)

    technical_expertise = forms.CharField(required=False)
    technical_expertise_other = forms.CharField(required=False)

    sector = forms.CharField(required=False)
    sector_other = forms.CharField(required=False)

    role = forms.CharField(required=False)
    role_other = forms.CharField(required=False)

    source_of_inspiration = forms.CharField(required=False)
    types_of_innovation = forms.CharField(required=False)

    place = forms.CharField(required=False)
    organization = forms.CharField(required=False)

    socialLinks = forms.CharField(required=False)

    def clean(self):
        pass
        # super(self.__class__, self).clean()

    # def save(self, validated_data):
    #     print validated_data
    #     return validated_data