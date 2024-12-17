from django_filters import rest_framework as filters
from .models import Equipment

class EquipmentFilter(filters.FilterSet):
    manufacturer = filters.CharFilter(field_name='manufacturer', lookup_expr='icontains')
    made_in = filters.CharFilter(field_name='made_in', lookup_expr='icontains')
    serial_no = filters.CharFilter(field_name='serial_no', lookup_expr='icontains')
    type = filters.CharFilter(field_name='type__type', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    model = filters.CharFilter(field_name='model', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status__status', lookup_expr='icontains')
    received_from = filters.CharFilter(field_name='received_from', lookup_expr='icontains')
    date_of_installation = filters.DateFilter(field_name='date_of_installation', lookup_expr='exact')
    place_of_installation = filters.CharFilter(field_name='place_of_installation__place', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Equipment
        fields = ['manufacturer', 'made_in', 'serial_no', 'type', 'title', 'model', 'status', 'received_from', 'date_of_installation', 'place_of_installation', 'description']