from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class RegistroGeral(models.Model):
    TIPO_SALA_CHOICES = [
        ('ANTISALA', 'Antisala'),
        ('COFRE', 'SalaCofre'),
        ('TELECOM', 'SalaTelecom'),
        ('ENERGIA', 'SalaEnergia'),
    ]
    tipo_sala = models.CharField(max_length=10, choices=TIPO_SALA_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relacionamento genérico com as salas específicas
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    sala = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.tipo_sala} - {self.user.username if self.user else 'N/A'}"


# Classe Base para salas
class SalaBase(models.Model):
    LIMPEZA_CHOICES = [
        ('L', 'Limpo'),
        ('M', 'Mais ou Menos'),
        ('S', 'Sujo'),
    ]
    observation = models.CharField(max_length=250, null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    limpeza = models.CharField(
        max_length=1,
        choices=LIMPEZA_CHOICES,
        default='L',
    )
    image = models.ImageField(upload_to='uploads/salas/', null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().save(*args, **kwargs)

        # Atualiza ou cria o registro geral correspondente
        RegistroGeral.objects.update_or_create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.id,
            defaults={
                'tipo_sala': self.TIPO_SALA,
                'user': user,
            }
        )



# Modelos específicos para cada sala
class AntiSala(SalaBase):
    TIPO_SALA = 'ANTISALA'

    def __str__(self):
        return "Antisala"


class SalaCofre(SalaBase):
    TIPO_SALA = 'COFRE'

    def __str__(self):
        return "SalaCofre"


class SalaTelecom(SalaBase):
    TIPO_SALA = 'TELECOM'

    def __str__(self):
        return "SalaTelecom"


class SalaEnergia(SalaBase):
    TIPO_SALA = 'ENERGIA'

    def __str__(self):
        return "SalaEnergia"