from django.contrib import admin
from .models import RegistroGeral, AntiSala, SalaCofre, SalaTelecom, SalaEnergia
from django.db.models import Count


@admin.register(RegistroGeral)
class RegistroGeralAdmin(admin.ModelAdmin):
    # Exibição na lista de registros
    list_display = ('tipo_sala', 'get_observacao', 'get_temperatura', 'user', 'get_created_at')
    list_filter = ('tipo_sala',)  # Filtro por tipo de sala
    search_fields = ('tipo_sala', 'user__username')  # Pesquisa por tipo de sala e usuário
    list_per_page = 15  # Paginação com 15 registros por página

    # Métodos para acessar campos da sala relacionada
    def get_observacao(self, obj):
        return obj.sala.observation
    get_observacao.short_description = 'Observação'

    def get_temperatura(self, obj):
        return f"{obj.sala.temperature} °C"
    get_temperatura.short_description = 'Temperatura'

    def get_created_at(self, obj):
        if obj.sala and hasattr(obj.sala, 'created_at'):
            return obj.sala.created_at.strftime('%d/%m/%Y %H:%M')
        return "-"
    get_created_at.short_description = 'Data de Criação'


    # Controle de permissões no admin
    def has_add_permission(self, request):
        """
        Impede que registros sejam adicionados diretamente pelo admin.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Impede que registros sejam alterados diretamente pelo admin.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Impede que registros sejam excluídos diretamente pelo admin.
        """
        return False


# Registro das outras salas
@admin.register(AntiSala)
class AntiSalaAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza',)


@admin.register(SalaCofre)
class SalaCofreAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza',)


@admin.register(SalaTelecom)
class SalaTelecomAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza',)


@admin.register(SalaEnergia)
class SalaEnergiaAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza',)
