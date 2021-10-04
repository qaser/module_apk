# from apk.forms import FaultFilterForm
import django_filters as df
from .models import Department, Fault, Location


class FaultFilter(df.FilterSet):
    department = df.ModelChoiceFilter(field_name='Служба филиала', queryset=Department.objects.all())
    # location = df.ModelChoiceFilter(field_name='Место обнаружения', queryset=Location.objects.filter(department=department))

    class Meta:
        model = Fault
        fields = [
            'fault_date',
            'location',
            # 'inspector' 
        ]
        # form = FaultFilterForm
