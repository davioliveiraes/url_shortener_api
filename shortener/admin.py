from django.contrib import admin
from django.http import HttpRequest

from .models import Click, ShortenedURL


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = [
        "short_code",
        "original_url_truncated",
        "is_active",
        "total_clicks",
        "expires_at",
        "created_at",
    ]

    list_filter = ["is_active", "created_at", "expires_at"]
    search_fields = ["short_code", "original_url"]
    readonly_fields = [
        "short_code",
        "total_clicks",
        "unique_clicks",
        "qr_code",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Informacoes Basicas",
            {"fields": ("original_url", "short_code", "qr_code")},
        ),
        (
            "Configuracoes",
            {
                "fields": ("is_active", "expires_at", "max_clicks"),
                "description": "Configure as restricoes do link",
            },
        ),
        (
            "Estatisticas",
            {
                "fields": ("total_clicks", "unique_clicks"),
                "description": "Contadores de cliques",
            },
        ),
        (
            "Metadados",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
                "description": "Informacoes de criacao e atualizacao",
            },
        ),
    )

    def original_url_truncated(self, obj):
        if len(obj.original_url) > 50:
            return obj.original_url[:47] + "..."
        return obj.original_url

    original_url_truncated.short_description = "URL Original"


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ["url", "ip_address", "clicked_at"]
    list_filter = ["clicked_at"]
    search_fields = ["url_short_code", "ip_address"]
    readonly_fields = ["url", "ip_address", "user_agent", "referer", "clicked_at"]
    date_hierarchy = "clicked_at"

    def has_add_permission(self, request):
        return False
