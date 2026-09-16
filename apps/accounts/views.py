from rest_framework.generics import ListAPIView

from apps.accounts.serializers import AccountSerializer
from apps.accounts.models import CustomerProfile

class AccountListView(ListAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return CustomerProfile.objects.all()
     