from django.forms import widgets
import django_filters as df
from django_filters.filters import DateFilter, DateFromToRangeFilter, DateRangeFilter
from django_filters.widgets import RangeWidget, DateRangeWidget

from .models import Department, Fault, Location
# from .utils import is_admin, is_manager, is_lead, is_engineer, is_employee


# class MyRangeWidget(RangeWidget):
#     def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
#         super(MyRangeWidget, self).__init__(attrs)

#         if from_attrs:
#             self.widgets[0].attrs.update(from_attrs)
#         if to_attrs:
#             self.widgets[1].attrs.update(to_attrs)


class FaultFilter(df.FilterSet):
    department = df.ModelChoiceFilter(
        field_name='location__department',
        label='Служба филиала',
        queryset=Department.objects.all()
    )
    # fault_date = DateFromToRangeFilter(
    #     field_name='fault_date',
    #     label='Временной интервал',
    #     widget=MyRangeWidget(
    #         attrs={'type': 'date'},
    #         from_attrs={},
    #         to_attrs={},
    #     )
    # )
    fault_date = DateRangeFilter(field_name='fault_date')
    # location = df.ModelChoiceFilter(
    #     field_name = 'location__object',
    #     label = 'Объект проверки',
    #     queryset = Location.objects.all(),
    # )

    class Meta:
        model = Fault
        fields = [
            'fault_date',
        ]

    # @property
    # def qs(self):
    #     qset = super(FaultFilter, self).qs
    #     user = self.request.user
    #     return qset.filter()