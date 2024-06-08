from django.contrib import admin
from .models import Task, Contract, OfficialLink, Social, ScrapingJob

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('coin', 'price', 'price_change', 'market_cap', 'market_cap_rank', 'volume', 'volume_rank', 'volume_change', 'circulating_supply', 'total_supply', 'diluted_market_cap')
    filter_horizontal = ('contracts', 'official_links', 'socials')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')

@admin.register(OfficialLink)
class OfficialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')

@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(ScrapingJob)
class ScrapingJobAdmin(admin.ModelAdmin):
    list_display = ('job_id',)  # Ensure this is a tuple
