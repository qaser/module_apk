from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import CheckboxSelectMultiple, ClearableFileInput, ModelForm
from django.forms.widgets import DateInput, FileInput, NumberInput, Textarea

from apk.models import Act, Fault, Fix
from django.forms.widgets import ClearableFileInput


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
            'fix_deadline': NumberInput(attrs={'type': 'date'}),
            'correct_deadline': NumberInput(attrs={'type': 'date'}),
            'reason': Textarea(attrs={'rows': 3}),
            'resources': Textarea(attrs={'rows': 3}),
        }