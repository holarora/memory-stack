from django.contrib import admin
from .models import Entry, Weather, Image

# Register your models here.


class WeatherAdmin(admin.ModelAdmin):
    pass


admin.site.register(Weather, WeatherAdmin)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    max_num = 2


class EntryAdmin(admin.ModelAdmin):
    # list_display = ('date', 'title', 'slug', 'content', 'weather')
    # prepopulated_fields = {'slug': ('date',)}
    # search_fields = ('title', 'content')
    inlines = [ImageInline]
    readonly_fields = ('slug',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('date',)
        return self.readonly_fields


admin.site.register(Entry, EntryAdmin)
admin.site.register(Image)
