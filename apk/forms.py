from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import CheckboxSelectMultiple, ClearableFileInput, ModelForm

from apk.models import Act, Fault


# class ImageWidget(ClearableFileInput):
#     template_name = 'recipes/extend/form_extend/image_widget.html'


class ActForm(ModelForm):
    class Meta:
        model = Act
        fields = ('control_level', 'act_number', 'closed')


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


class FixForm(ModelForm):
    class Meta:
        model = Fault
        fields = (
            'fix_action',
            'fixer',
            'fix_deadline',
            'fixed',
            'fix_date',
            'reason',
            'correct_action',
            'resources',
            'corrector',
            'correct_deadline',
            'corrected',
            'correct_date',
            'image_after',
        )