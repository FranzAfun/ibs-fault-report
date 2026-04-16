from django.contrib import admin
from .models import AssetRecord, AssetItem


@admin.register(AssetRecord)
class AssetRecordAdmin(admin.ModelAdmin):
	list_display = ('reference_number', 'employee_name', 'project', 'job_title', 'approved_by', 'approval_date', 'created_at')
	search_fields = ('reference_number', 'employee_name', 'project', 'job_title')
	list_filter = ('approval_date', 'created_at')


@admin.register(AssetItem)
class AssetItemAdmin(admin.ModelAdmin):
	list_display = ('asset_type', 'date_issued', 'issued_by', 'asset_record')
	search_fields = ('asset_type', 'issued_by')
	list_filter = ('date_issued',)
