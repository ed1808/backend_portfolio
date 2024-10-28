from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from .models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        # Crear una instancia de Contact para usar en las pruebas
        self.contact = Contact.objects.create(
            name="Juan Pérez",
            email="juan.perez@example.com",
            message="Este es un mensaje de contacto.",
        )

    def test_create_contact(self):
        # Verificar que se puede crear y almacenar correctamente una instancia de Contact
        contact = Contact.objects.create(
            name="Maria López",
            email="maria.lopez@example.com",
            message="Este es otro mensaje de contacto.",
        )
        self.assertIsInstance(contact, Contact)
        self.assertEqual(contact.name, "Maria López")

    def test_name_field_required(self):
        # Verificar que el campo `name` es obligatorio
        contact = Contact(
            name="", email="contact@example.com", message="Mensaje de contacto"
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_email_field_required(self):
        # Verificar que el campo `email` es obligatorio
        contact = Contact(name="Carlos Gómez", email="", message="Mensaje de contacto")
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_message_field_required(self):
        # Verificar que el campo `message` es obligatorio
        contact = Contact(
            name="Carlos Gómez", email="carlos.gomez@example.com", message=""
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_email_field_format(self):
        # Verificar que el campo `email` requiere un formato válido
        contact = Contact(
            name="Pedro Rodríguez", email="invalid-email", message="Mensaje de contacto"
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_name_max_length(self):
        # Verificar que el campo `name` tiene una longitud máxima de 255 caracteres
        long_name = "A" * 256
        contact = Contact(
            name=long_name, email="test@example.com", message="Mensaje de contacto"
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_created_at_field_auto_now_add(self):
        # Verificar que el campo `created_at` se establece automáticamente al crear la instancia
        creation_time = timezone.now()
        contact = Contact.objects.create(
            name="Laura Martinez",
            email="laura.martinez@example.com",
            message="Mensaje de contacto",
        )
        self.assertAlmostEqual(
            contact.created_at, creation_time, delta=timedelta(seconds=1)
        )

    def test_str_method(self):
        # Verificar que el método __str__ devuelve el valor correcto
        self.assertEqual(str(self.contact), "Juan Pérez")

    def test_meta_verbose_name(self):
        # Verificar verbose_name
        self.assertEqual(Contact._meta.verbose_name, "Contacto")

    def test_meta_verbose_name_plural(self):
        # Verificar verbose_name_plural
        self.assertEqual(Contact._meta.verbose_name_plural, "Contactos")


class ContactCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            "contact"
        )  # Asegurarse de que este nombre esté registrado en urls.py
        self.valid_payload = {
            "name": "Juan Pérez",
            "email": "juan.perez@example.com",
            "message": "Este es un mensaje de prueba.",
        }
        self.invalid_email_payload = {
            "name": "Juan Pérez",
            "email": "juan.perez@invalid",  # Email incorrecto
            "message": "Este es un mensaje de prueba.",
        }
        self.missing_name_payload = {
            "email": "juan.perez@example.com",
            "message": "Este es un mensaje de prueba.",
        }

    def test_create_contact_success(self):
        # Prueba de creación exitosa de contacto (código 201)
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "success")

        # Verificar que el contacto fue creado en la base de datos
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, self.valid_payload["name"])
        self.assertEqual(contact.email, self.valid_payload["email"])
        self.assertEqual(contact.message, self.valid_payload["message"])

    def test_create_contact_invalid_email(self):
        # Prueba de validación de formato de correo electrónico
        response = self.client.post(
            self.url, data=self.invalid_email_payload, format="json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn(
            "email", response.data
        )  # Verificar que el error esté en el campo `email`

    def test_create_contact_missing_name(self):
        # Prueba de campo obligatorio faltante (name)
        response = self.client.post(
            self.url, data=self.missing_name_payload, format="json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn(
            "name", response.data
        )  # Verificar que el error esté en el campo `name`

    def test_create_contact_missing_email(self):
        # Prueba de campo obligatorio faltante (email)
        missing_email_payload = {
            "name": "Juan Pérez",
            "message": "Este es un mensaje de prueba.",
        }
        response = self.client.post(self.url, data=missing_email_payload, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_contact_missing_message(self):
        # Prueba de campo obligatorio faltante (message)
        missing_message_payload = {
            "name": "Juan Pérez",
            "email": "juan.perez@example.com",
        }
        response = self.client.post(
            self.url, data=missing_message_payload, format="json"
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_permission_allow_any(self):
        # Prueba de permisos para asegurar que el endpoint esté accesible para todos
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(
            response.status_code, HTTP_201_CREATED
        )  # El acceso es permitido para cualquier usuario
