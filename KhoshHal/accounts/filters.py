import django_filters
from .models import Counselor


class UserFilter(django_filters.FilterSet):
    o = django_filters.OrderingFilter(
        fields=(
            ('user__username', 'username'),
            ('user__first_name', 'first_name'),
            ('user__last_name', 'last_name'),
        ),

        field_labels={
            'username': 'User account',
        }
    )

    class Meta:
        model = Counselor
        fields = {
            'user__username': ['iexact', 'icontains'],
            'user__first_name': ['iexact', ],
            'user__last_name': ['iexact', ],
            'specialty': ['iexact', 'icontains'],
        }
