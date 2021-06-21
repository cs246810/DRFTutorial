from django.contrib import admin
from .models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    # Custom admin list view
    list_display = ('title', 'language', 'style', 'created', 'owner')
    # list_display_links = ('title', ) # default
    # sortable_by # a sub set of list_display. All fields are sortable by default.

    '''define which fields are editable on list view'''
    list_editable = ('owner',)

    '''10 items per page'''
    list_per_page = 5

    '''Max 200 when clicking show all'''
    list_max_show_all = 200  # default

    '''Calling select related objects to reduce SQL queries'''
    # list_select_related = ('language', )

    '''Render a search box at top. ^, =, @, None=icontains'''
    search_fields = ['owner__username', 'language']

    '''Render date options at top. do not accept tuple'''
    date_hierarchy = 'created'

    '''Replacement value for empty field'''
    empty_value_display = 'NA'

    '''filter options'''
    list_filter = ('language', 'owner__is_superuser', 'created' )


# Register your models here.
admin.site.register(Snippet, SnippetAdmin)


admin.site.site_title = 'DRFTutorial后台管理'
admin.site.site_header = admin.site.site_title
