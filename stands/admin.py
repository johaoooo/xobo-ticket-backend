from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Stand, Validation


class ValidationInline(admin.TabularInline):
    model = Validation
    extra = 0
    readonly_fields = ['valide_par', 'password_validation', 'created_at']
    can_delete = False
    verbose_name = "Validation enregistrée"
    verbose_name_plural = "Historique des validations"


@admin.register(Stand)
class StandAdmin(admin.ModelAdmin):
    list_display = [
        'numero_stand', 'nom', 'proprietaire_complet',
        'email', 'statut_badge', 'a_code_en_attente', 'created_at'
    ]
    list_filter = ['statut', 'created_at']
    search_fields = ['nom', 'email', 'nom_prop', 'prenom_prop', 'numero_stand']
    readonly_fields = ['numero_stand', 'created_at', 'updated_at', 'validation_comment']
    ordering = ['-created_at']
    inlines = [ValidationInline]

    fieldsets = (
        ('Informations du stand', {
            'fields': ('numero_stand', 'nom', 'adresse', 'email', 'statut')
        }),
        ('Propriétaire', {
            'fields': ('nom_prop', 'prenom_prop', 'user')
        }),
        ('Validation', {
            'fields': ('temp_password', 'validation_comment'),
            'classes': ('collapse',),
            'description': 'Champs gérés automatiquement lors de la validation.'
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['marquer_valide', 'marquer_rejete', 'marquer_en_attente']

    def proprietaire_complet(self, obj):
        return f"{obj.prenom_prop} {obj.nom_prop}"
    proprietaire_complet.short_description = "Propriétaire"

    def statut_badge(self, obj):
        colors = {
            'en_attente': ('#f59e0b', '#fff8e1', '⏳ En attente'),
            'valide':     ('#10b981', '#e8f5e9', '✅ Validé'),
            'rejete':     ('#ef4444', '#fdecea', '❌ Rejeté'),
        }
        color, bg, label = colors.get(obj.statut, ('#888', '#f5f5f5', obj.statut))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:12px;font-size:0.82em;font-weight:600">{}</span>',
            bg, color, label
        )
    statut_badge.short_description = "Statut"

    def a_code_en_attente(self, obj):
        if obj.temp_password:
            return format_html('<span style="color:#f59e0b;font-weight:600">🔑 Code envoyé</span>')
        return "—"
    a_code_en_attente.short_description = "Code propriétaire"

    @admin.action(description="✅ Marquer comme Validé")
    def marquer_valide(self, request, queryset):
        updated = queryset.update(statut='valide')
        self.message_user(request, f"{updated} stand(s) marqué(s) comme validé(s).")

    @admin.action(description="❌ Marquer comme Rejeté")
    def marquer_rejete(self, request, queryset):
        updated = queryset.update(statut='rejete')
        self.message_user(request, f"{updated} stand(s) marqué(s) comme rejeté(s).")

    @admin.action(description="⏳ Remettre En attente")
    def marquer_en_attente(self, request, queryset):
        updated = queryset.update(statut='en_attente', temp_password=None)
        self.message_user(request, f"{updated} stand(s) remis en attente.")


@admin.register(Validation)
class ValidationAdmin(admin.ModelAdmin):
    list_display = ['stand_nom', 'stand_statut', 'valide_par', 'created_at']
    list_filter = ['created_at', 'stand__statut']
    search_fields = ['stand__nom', 'valide_par__username']
    readonly_fields = ['stand', 'valide_par', 'password_validation', 'created_at']
    ordering = ['-created_at']

    def stand_nom(self, obj):
        return obj.stand.nom
    stand_nom.short_description = "Stand"

    def stand_statut(self, obj):
        colors = {
            'en_attente': ('#f59e0b', '#fff8e1', '⏳ En attente'),
            'valide':     ('#10b981', '#e8f5e9', '✅ Validé'),
            'rejete':     ('#ef4444', '#fdecea', '❌ Rejeté'),
        }
        color, bg, label = colors.get(obj.stand.statut, ('#888', '#f5f5f5', obj.stand.statut))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:12px;font-size:0.82em;font-weight:600">{}</span>',
            bg, color, label
        )
    stand_statut.short_description = "Statut du stand"

    def has_add_permission(self, request):
        return False
