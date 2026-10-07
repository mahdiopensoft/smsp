from rest_framework import serializers
from bank.models.AuditLog import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = '__all__'

    def get_user_name(self, obj):
        if obj.user:
            first = getattr(obj.user, 'first_name', '') or ''
            last = getattr(obj.user, 'last_name', '') or ''
            full = f"{first} {last}".strip()
            return full or getattr(obj.user, 'username', '') or str(obj.user)
        return "النظام"

