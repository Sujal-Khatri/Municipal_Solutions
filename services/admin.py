from django.contrib import admin
from .models import DiscussionPost, PostReaction, Notice, Report, TaxReturn, SelfAssessmentReturn, Hospital
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

admin.site.register(PostReaction)    

admin.site.register(Notice)

admin.site.register(Report)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'allocated_beds', 'total_beds',
        'active_patients', 'hospital_type', 'contact_person', 'contact_number'
    )
    list_editable = (
        'allocated_beds', 'total_beds',
        'active_patients', 'hospital_type', 'contact_person', 'contact_number'
    )
    list_per_page = 20
@admin.register(SelfAssessmentReturn)
class SelfAssessmentReturnAdmin(admin.ModelAdmin):
    list_display    = ('submission_no','username','pan_no','created_at','submitted')
    readonly_fields = ('submission_no','created_at',     )
@admin.register(TaxReturn)
class TaxReturnAdmin(admin.ModelAdmin):
    list_display = (
      'id',
      'user',
      'pan_no',
      'fiscal_year',
      'tax_amount',
      'submitted_at',
    )
    readonly_fields = ('submitted_at',)