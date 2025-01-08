
from django.contrib import admin
from .models import RegistroGeral, AntiSala, SalaCofre, SalaTelecom, SalaEnergia
from django.db.models import Count


@admin.register(RegistroGeral)
class RegistroGeralAdmin(admin.ModelAdmin):
    # Exibição na lista de registros
    list_display = ('tipo_sala', 'data_criacao_formatada', 'temperatura_formatada', 'user', 'observacao')
    list_filter = ('tipo_sala', 'data_criacao')  # Filtros laterais
    search_fields = ('tipo_sala', 'user__username', 'observacao')  # Pesquisa por tipo_sala, usuário e observação
    date_hierarchy = 'data_criacao'  # Navegação por data
    readonly_fields = ('tipo_sala', 'observacao', 'temperatura', 'data_criacao', 'user')  # Campos só para leitura
    list_per_page = 15  # Paginação com 15 registros por página

    # Formatação customizada para exibição
    def data_criacao_formatada(self, obj):
        return obj.data_criacao.strftime('%d/%m/%Y')  # Formata a data no padrão brasileiro
    data_criacao_formatada.short_description = 'Data de Criação'

    def temperatura_formatada(self, obj):
        return f"{obj.temperatura} °C"  # Exibe a temperatura com unidade
    temperatura_formatada.short_description = 'Temperatura'

    # Adiciona contexto extra ao changelist (exemplo: total por tipo de sala)
    def changelist_view(self, request, extra_context=None):
        total_por_tipo = (
            RegistroGeral.objects.values('tipo_sala')
            .annotate(total=Count('tipo_sala'))
            .order_by('tipo_sala')
        )
        extra_context = extra_context or {}
        extra_context['total_por_tipo'] = total_por_tipo  # Passa a contagem para o contexto do template
        return super().changelist_view(request, extra_context=extra_context)
    

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj = None):
        return False
    def has_delete_permission(self, request, obj = None):
        return False
# Registro das outras salas
@admin.register(AntiSala)
class AntiSalaAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza', 'created_at',)

@admin.register(SalaCofre)
class SalaCofreAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza', 'created_at')

@admin.register(SalaTelecom)
class SalaTelecomAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza', 'created_at')

@admin.register(SalaEnergia)
class SalaEnergiaAdmin(admin.ModelAdmin):
    list_display = ('observation', 'temperature', 'limpeza', 'created_at')
