#from adminfilters.multiselect import UnionFieldListFilter
#from advanced_filters.admin import AdminAdvancedFiltersMixin
from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _
from .models import Task, Team
#from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter



class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'deadline', 'state')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'item__item_description',
                     'user__username', 'user__first_name', 'user__last_name')

    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_modified', 'created_by')
    autocomplete_fields = ['user']

    fieldsets = (               # Edition form
        (None,                   {'fields': ('title', ('user', 'deadline'), ('state'), ('description', 'resolution'))}),
        (_('More...'), {'fields': (('created_at', 'last_modified'), 'created_by'), 'classes': ('collapse',)}),
    )

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('title', ('user', 'deadline'), ('state'), 'description')}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'users')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'created_by',
                     'user__username')

    ordering = ('-title',)
    readonly_fields = ('created_by',)
    autocomplete_fields = ['users']

    fieldsets = (               # Edition form
        (None,                   {'fields': ('title', ('users',),)}),
        (_('More...'), {'fields': ('created_by',), 'classes': ('collapse',)}),
    )

    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 4, 'cols': 32})
        }
    }

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            fieldsets = (      # Creation form
                (None, {'fields': ('title', 'users')}),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        if change is False:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Team, TeamAdmin)