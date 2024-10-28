from rest_framework.serializers import ModelSerializer

from .models import Contact


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        exclude = ["created_at"]
