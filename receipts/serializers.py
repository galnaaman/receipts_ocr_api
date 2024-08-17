from rest_framework import serializers
from .models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Receipt
        fields = ['id', 'image', 'uploaded_at', 'processed_data']
        read_only_fields = ['uploaded_at', 'processed_data']
