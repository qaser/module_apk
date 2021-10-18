import datetime as dt

from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput, NumberInput, Textarea

from apk.models import Fault, Fix, Location


class ImageWidget(ClearableFileInput):
    template_name = 'apk/apk_ext/form_extend/image_widget.html'


class FaultForm(ModelForm):
    class Meta:
        model = Fault
        fields = (
            'group',
            'location',
            'description',
            'document',
            'danger',
            'intruder',
            'unseeing',
            'section_esupb',
            'image_before',
        )
        widgets = {
            'description': Textarea(attrs={'rows': 5}),
            'image_before': ImageWidget(),
        }


class FaultFormFirstLevel(ModelForm):
    class Meta:
        model = Fault
        fields = (
            'location',
            'description',
            'danger',
            'image_before',
        )
        widgets = {
            'description': Textarea(attrs={'rows': 5}),
            'image_before': ImageWidget(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FaultFormFirstLevel, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(
            department=user.profile.department
        )


class FixForm(ModelForm):
    class Meta:
        actual_time = dt.datetime.now().strftime('%Y-%m-%d')
        model = Fix
        fields = (
            'fix_action',
            'fixer',
            'fix_deadline',
            'fixed',
            'reason',
            'correct_action',
            'resources',
            'corrector',
            'correct_deadline',
            'corrected',
            'image_after',
        )
        widgets = {
            'fix_action': Textarea(attrs={'rows': 5}),
            'correct_action': Textarea(attrs={'rows': 5}),
            'image_after': ImageWidget(),
            'fix_deadline': NumberInput(
                attrs={'type': 'date', 'value': actual_time}
            ),
            'correct_deadline': NumberInput(
                attrs={'type': 'date', 'value': actual_time}
            ),
            'reason': Textarea(attrs={'rows': 3}),
            'resources': Textarea(attrs={'rows': 3}),
        }
