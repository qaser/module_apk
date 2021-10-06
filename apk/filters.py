# from apk.forms import FaultFilterForm
import django_filters as df
from django_filters.widgets import RangeWidget
from .models import Department, Fault
import datetime as dt


class FaultFilter(df.FilterSet):
    department = df.ModelChoiceFilter(
        field_name='location__department',
        label='Служба филиала',
        queryset=Department.objects.all()
    )
    fault_date = df.DateFromToRangeFilter(
        field_name='fault_date',
        label='Временной интервал',
        widget=RangeWidget(
            attrs={'type': 'date'},
        )
    )

    class Meta:
        model = Fault
        fields = [
            'fault_date',
        ]
