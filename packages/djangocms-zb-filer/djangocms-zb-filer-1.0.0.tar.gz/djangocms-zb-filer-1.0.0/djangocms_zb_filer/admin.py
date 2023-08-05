#      Copyright (C)  2022. CQ Inversiones SAS.
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
import pytz
from django.contrib import admin
from django.utils import dateformat
from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Category, Publication, Certificate, CertificateConfigs


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "certificate"]
    search_fields = ["name"]
    list_filter = ["parent"]
    autocomplete_fields = ["parent"]


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "published_at", "publish_end_at", ]
    search_fields = ["title", "published_at"]
    list_filter = ["category", "author", "published_at"]
    date_hierarchy = "published_at"
    readonly_fields = ["created_at", "modified_at", "actions_buttons", "last_certificate"]
    ordering = ["-published_at"]
    autocomplete_fields = ["category"]
    fieldsets = (
        (_("Main Options"), {
            'fields': ('title', 'description', ('category', 'author'), 'file')
        }),
        (_('Date Options'), {
            'classes': ('collapse',),
            'fields': (('published_at', 'publish_end_at'),),
        }),
        (_('Advance Options'), {
            'classes': ('collapse',),
            'fields': (('notification', 'icon_class'),),
        }),
    )

    def actions_buttons(self, obj):
        publication = Publication.objects.get(id=obj.id)
        generate = _("Generate PDF certificate")
        send = _("Send Certificate")
        if not publication.category.certificate:
            return
        return format_html(
            f'<a href="/djangocms_zb_filer/generate-pdf/{obj.id}" '
            f'class="btn" style="padding:10px 20px !important;" target="_parent">{generate}</a>&nbsp;'
            f'<a href="" class="btn" style="padding:10px 20px !important;">{send}</a>'
        )

    actions_buttons.short_description = _("Actions")

    def last_certificate(self, obj):
        publication = Publication.objects.get(id=obj.id)
        certificates_publications = publication.zb_certifies_publication.all().order_by("-created_at")
        for cer in certificates_publications:
            time_zone = pytz.timezone(settings.TIME_ZONE)
            date_created = dateformat.format(cer.created_at.astimezone(time_zone), "d \d\e F \d\e Y H:i:s")
            see = _("See Certificate")
            return format_html(
                f'<a href="{cer.file_path}" target="_blank" class="button">{see}</a> {date_created}'
            )

    last_certificate.short_description = _("Last Certificate")

    def get_fieldsets(self, request, obj=None):
        if obj:  # editing an existing object
            return self.fieldsets + (
                (_('Additional Information'), {
                    'fields': ('created_at', 'modified_at')
                }),
                (_('Additional Actions'), {
                    'fields': ('actions_buttons',)
                }),
                (_('Certificate'), {
                    'fields': ('last_certificate',)
                }),
            )
        return self.fieldsets


@admin.register(CertificateConfigs)
class CertificateConfigsAdmin(admin.ModelAdmin):
    list_display = ["name", "header", "sign"]
    search_fields = ["name", "title"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def certificate(self, obj):
        pk = obj.id
        certificate = Certificate.objects.get(id=pk)
        see = _("See Certificate")
        return format_html(
            f'<a href="{certificate.file_path}" target="_blank" class="button">{see}</a>'
        )

    certificate.short_description = _("Certificate")

    list_display = ["created_at", "publication", "certificate"]
    list_display_links = None
    search_fields = ["publication__title", "created_at", "file_path"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
