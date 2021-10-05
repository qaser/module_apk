from django.forms import ModelForm
from django.forms.widgets import ClearableFileInput, NumberInput, Textarea
import datetime as dt

from apk.models import Fault, Fix


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


class FixForm(ModelForm):
    class Meta:
        actual_time = dt.datetime.now().strftime('%Y-%m-%d')
        model = Fix
        fields = (
            'fix_action',
            'fixer',
            'fix_deadline',
            'fixed',
            # 'fix_date',
            'reason',
            'correct_action',
            'resources',
            'corrector',
            'correct_deadline',
            'corrected',
            # 'correct_date',
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
