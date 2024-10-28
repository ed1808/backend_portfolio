from django.db import models


class Contact(models.Model):
    name: models.CharField = models.CharField(
        max_length=255, verbose_name="Nombre contacto"
    )
    email: models.EmailField = models.EmailField(verbose_name="Email contacto")
    message: models.TextField = models.TextField(verbose_name="Mensaje contacto")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"

    def __str__(self):
        return self.name
