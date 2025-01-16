from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import AntiSala, SalaCofre, SalaEnergia, SalaTelecom, RegistroGeral

# Lista com todas as subclasses de SalaBase
SALA_MODELS = [AntiSala, SalaCofre, SalaEnergia, SalaTelecom]

@receiver(post_delete)
def delete_registro_geral(sender, instance, **kwargs):
    """
    Deleta o registro correspondente em RegistroGeral quando qualquer sala é deletada.
    """

    try:
        # Identificar o tipo de sala e deletar o registro relacionado
        content_object = instance.sala  # O campo `GenericForeignKey` no RegistroGeral
        if content_object:
            content_object.delete()
    except Exception as e:
        print(f"Erro ao deletar o registro de sala associado: {e}")

    if sender in SALA_MODELS:
        # Exclui o RegistroGeral correspondente ao registro deletado
        RegistroGeral.objects.filter(sala_id=instance.id).delete()