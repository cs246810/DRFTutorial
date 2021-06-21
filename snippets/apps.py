from django.apps import AppConfig


class SnippetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'snippets'
    verbose_name = '片段管理'
