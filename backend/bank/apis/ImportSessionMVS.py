from OpenSoftCoreV41.utils.model_view_set.__all__ import AllMVS
from bank.models.ImportSession import ImportSession
from bank.serializers.ImportSession import ImportSessionSerializer

class ImportSessionMVS(AllMVS):
    queryset = ImportSession.objects.all()
    serializer_class = ImportSessionSerializer

