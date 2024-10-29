from django.core.mail import send_mail
from django.conf import settings
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .models import Contact
from .serializers import ContactSerializer


class ContactCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        send_mail(
            f"New contact from portfolio: {serializer.data['name']}",
            f"{serializer.data["message"]} | Contact email: {serializer.data['email']}",
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_TO_USER],
            fail_silently=True,
        )

        return Response({"message": "success"}, status=HTTP_201_CREATED)
