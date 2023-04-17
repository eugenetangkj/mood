from django.contrib import admin
from .models import User, Entry
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "number_of_meditations")



class EntryAdmin(admin.ModelAdmin):
    list_display = ("owner", "date", "entry_title", "entry_body", "emotion", "image")


admin.site.register(User, UserAdmin)
admin.site.register(Entry, EntryAdmin)