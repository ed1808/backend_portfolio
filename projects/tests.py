from datetime import timedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from .models import Project, Technology
from .serializers import ProjectSerializer


class TechnologyModelTest(TestCase):
    def setUp(self):
        # Creación de una instancia de Technology para usar en pruebas
        self.tech = Technology.objects.create(name="Python")

    def test_create_technology(self):
        # Verificar que se puede crear y almacenar correctamente una instancia
        technology = Technology.objects.create(name="Django")
        self.assertIsInstance(technology, Technology)
        self.assertEqual(technology.name, "Django")

    def test_name_field_required(self):
        # Verificar que el campo `name` es obligatorio
        technology = Technology(name="")
        with self.assertRaises(ValidationError):
            technology.full_clean()  # Lanza un ValidationError si hay errores de validación

    def test_name_max_length(self):
        # Verificar que el campo `name` tiene una longitud máxima de 255 caracteres
        long_name = "A" * 256
        technology = Technology(name=long_name)
        with self.assertRaises(ValidationError):
            technology.full_clean()

    def test_created_at_field_auto_now_add(self):
        # Verificar que el campo `created_at` se establece automáticamente al crear la instancia
        creation_time = timezone.now()
        technology = Technology.objects.create(name="JavaScript")
        # Rango de tiempo pequeño para verificar que el campo se establece al momento de la creación
        self.assertAlmostEqual(
            technology.created_at, creation_time, delta=timedelta(seconds=1)
        )

    def test_str_method(self):
        # Verificar que el método __str__ devuelve el valor correcto
        self.assertEqual(str(self.tech), "Python")

    def test_meta_verbose_name(self):
        # Verificar verbose_name
        self.assertEqual(Technology._meta.verbose_name, "Tecnología")

    def test_meta_verbose_name_plural(self):
        # Verificar verbose_name_plural
        self.assertEqual(Technology._meta.verbose_name_plural, "Tecnologías")


class ProjectModelTest(TestCase):
    def setUp(self):
        # Crear instancias de Technology y Project para usar en pruebas
        self.tech_python = Technology.objects.create(name="Python")
        self.tech_django = Technology.objects.create(name="Django")
        self.project = Project.objects.create(
            name="Mi Proyecto",
            description="Descripción del proyecto.",
            url="https://example.com",
            project_status="available",
        )
        # Asociar tecnologías al proyecto
        self.project.technologies.set([self.tech_python, self.tech_django])

    def test_create_project(self):
        # Verificar que se puede crear y almacenar correctamente una instancia de Project
        project = Project.objects.create(
            name="Nuevo Proyecto",
            description="Otra descripción.",
            url="https://newexample.com",
            project_status="available",
        )
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, "Nuevo Proyecto")

    def test_name_field_required(self):
        # Verificar que el campo `name` es obligatorio
        project = Project(
            name="",
            description="Descripción del proyecto.",
            url="https://example.com",
            project_status="available",
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_description_field_required(self):
        # Verificar que el campo `description` es obligatorio
        project = Project(
            name="Proyecto sin descripción",
            description="",
            url="https://example.com",
            project_status="available",
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_url_field_required(self):
        # Verificar que el campo `url` es obligatorio
        project = Project(
            name="Proyecto sin URL",
            description="Descripción del proyecto.",
            url="",
            project_status="available",
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_project_status_choices(self):
        # Verificar que el campo `project_status` solo acepta valores válidos
        project = Project(
            name="Proyecto con estado inválido",
            description="Descripción del proyecto.",
            url="https://example.com",
            project_status="invalid_status",
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_name_max_length(self):
        # Verificar que el campo `name` tiene una longitud máxima de 255 caracteres
        long_name = "A" * 256
        project = Project(
            name=long_name,
            description="Descripción del proyecto.",
            url="https://example.com",
            project_status="available",
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_technologies_field(self):
        # Verificar que se pueden asociar tecnologías a un proyecto
        self.assertIn(self.tech_python, self.project.technologies.all())
        self.assertIn(self.tech_django, self.project.technologies.all())

    def test_created_at_field_auto_now_add(self):
        # Verificar que el campo `created_at` se establece automáticamente al crear la instancia
        creation_time = timezone.now()
        project = Project.objects.create(
            name="Proyecto con fecha",
            description="Descripción del proyecto.",
            url="https://example.com",
            project_status="available",
        )
        self.assertAlmostEqual(
            project.created_at, creation_time, delta=timedelta(seconds=1)
        )

    def test_str_method(self):
        # Verificar que el método __str__ devuelve el valor correcto
        self.assertEqual(str(self.project), "Mi Proyecto")

    def test_meta_verbose_name(self):
        # Verificar verbose_name
        self.assertEqual(Project._meta.verbose_name, "Proyecto")

    def test_meta_verbose_name_plural(self):
        # Verificar verbose_name_plural
        self.assertEqual(Project._meta.verbose_name_plural, "Proyectos")


class ProjectsListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear proyectos para probar la lista y el orden
        self.project1 = Project.objects.create(
            name="Proyecto Antiguo",
            description="Este es el proyecto antiguo.",
            url="https://oldexample.com",
            project_status="available",
            created_at=timezone.now() - timedelta(days=10),
        )
        self.project2 = Project.objects.create(
            name="Proyecto Nuevo",
            description="Este es el proyecto más nuevo.",
            url="https://newexample.com",
            project_status="available",
            created_at=timezone.now(),
        )

        # URL para el endpoint de listado de proyectos
        self.url = reverse("projects")

    def test_get_projects_list_success(self):
        # Prueba de respuesta exitosa con código 200
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_projects_order(self):
        # Prueba de que los proyectos se devuelven en orden descendente por `created_at`
        response = self.client.get(self.url)
        projects = response.data

        # Asegurarse de que el primer proyecto sea el más reciente
        self.assertEqual(projects[0]["name"], self.project2.name)
        self.assertEqual(projects[1]["name"], self.project1.name)

    def test_pagination(self):
        # Verificar que la paginación limita el número de resultados
        # Se creará un proyecto adicional para verificar el límite de paginación
        Project.objects.create(
            name="Proyecto Extra",
            description="Este es un proyecto adicional.",
            url="https://extraexample.com",
            project_status="available",
            created_at=timezone.now() - timedelta(days=5),
        )

        # Solicitar la lista de proyectos con límite de paginación de 2
        response = self.client.get(f"{self.url}?limit=2")
        self.assertEqual(response.status_code, HTTP_200_OK)

        # Verificar que se devuelven solo 2 proyectos en la página actual
        self.assertEqual(len(response.data["results"]), 2)

    def test_response_structure(self):
        # Comprobar que la respuesta tiene la estructura y los datos esperados
        response = self.client.get(self.url)
        projects = Project.objects.all().order_by("-created_at")
        serializer = ProjectSerializer(
            projects[:2], many=True
        )  # Solo verificamos los primeros 2 proyectos

        # Validar que los datos serializados coinciden con los datos de la respuesta
        self.assertEqual(response.data, serializer.data)


class ProjectDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Crear un proyecto para usar en la prueba de detalle
        self.project = Project.objects.create(
            name="Proyecto Detalle",
            description="Este es un proyecto de prueba para el detalle.",
            url="https://example.com",
            project_status="available",
            created_at=timezone.now(),
        )

        # URL para el endpoint de detalle del proyecto con el ID del proyecto creado
        self.url = reverse("project", kwargs={"pk": self.project.id})

    def test_get_project_detail_success(self):
        # Prueba de respuesta exitosa con código 200 al obtener un proyecto existente
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_project_detail_data(self):
        # Prueba de que la estructura y los datos de la respuesta son correctos
        response = self.client.get(self.url)

        # Serializar el proyecto directamente desde la base de datos
        serializer = ProjectSerializer(self.project)

        # Comprobar que los datos de la respuesta coinciden con los datos serializados
        self.assertEqual(response.data, serializer.data)

    def test_project_not_found(self):
        # Prueba de que se obtiene un código 404 si el proyecto no existe
        url = reverse("project", kwargs={"pk": 999})  # ID no existente
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
