from utils.core.read_only_api_view import  ReadOnlyApiView
from d_services.models.MetaDataTable import MetaDataTable
from d_services.serializers.MetaDataTable import MetaDataTableSerializer

class MetaDataTableMVS(ReadOnlyApiView):
    queryset = MetaDataTable.objects.prefetch_related()
    serializer_class = MetaDataTableSerializer
