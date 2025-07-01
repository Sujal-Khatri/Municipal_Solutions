from django.contrib import admin
from .models import DiscussionPost
from django.utils.html import format_html

@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'preview_image', 'map_link')

    readonly_fields = ('preview_image', 'map_link')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "-"
    preview_image.short_description = "Image"

    def map_link(self, obj):
        if obj.location:
            lat, lng = obj.location.split(',')
            url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}#map=16/{lat}/{lng}"
            return format_html('<a href="{}" target="_blank">View Map</a>', url)
        return "-"
    map_link.short_description = "Location"