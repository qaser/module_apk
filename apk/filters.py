import django_filters as df
from django_filters.filters import DateRangeFilter

from .models import Department, Fault, Location


class FaultFilter(df.FilterSet):
    department = df.ModelChoiceFilter(
        field_name='location__department',
        label='Служба филиала',
        queryset=Department.objects.all()
    )
    fault_date = DateRangeFilter(field_name='fault_date')

    class Meta:
        model = Fault
        fields = [
            'fault_date',
            'location',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FaultFilter, self).__init__(*args, **kwargs)
        self.form.fields['location'].queryset = Location.objects.filter(
            department=user.profile.department
        )
