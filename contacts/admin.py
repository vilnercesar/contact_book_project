from django.contrib import admin

from .models import Category, Contact


# Register your models here.
@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'cell_phone', 'is_publish')
    list_display_links = ('first_name', 'last_name')
    # list_filter = ('id', 'first_name', 'last_name')
    list_per_page = 10
    search_fields = ('id', 'first_name', 'last_name')
    list_editable = ('cell_phone', 'is_publish')
