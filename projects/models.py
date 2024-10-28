from django.db import models


class Technology(models.Model):
    name: models.CharField = models.CharField(
        max_length=255, verbose_name="Nombre de la tecnología o lenguaje"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tecnología"
        verbose_name_plural = "Tecnologías"

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
    )

    name: models.CharField = models.CharField(
        max_length=255, verbose_name="Nombre del proyecto"
    )
    description: models.TextField = models.TextField(
        verbose_name="Descripción del proyecto"
    )
    url: models.URLField = models.URLField(verbose_name="URL del proyecto")
    technologies: models.ManyToManyField = models.ManyToManyField(
        Technology, verbose_name="Tecnologías", related_name="technologies"
    )
    project_status: models.CharField = models.CharField(
        max_length=15, choices=STATUS, verbose_name="Estado del proyecto"
    )
    project_image: models.ImageField = models.ImageField(
        verbose_name="Imagen del proyecto", blank=True, null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.name
