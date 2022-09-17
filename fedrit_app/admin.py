from django.contrib import admin
from .models import SiteUser, Sub, Post, PGP

class SubAdmin(admin.ModelAdmin):
    pass#fields = [dstr for dstr in dir(Sub) if dstr[0] != '_']

class PostAdmin(admin.ModelAdmin):
    pass

@admin.action(description='Generate PGP key for an existing PGP record.')
def gen_pgp_action(modeladmin, request, queryset):
    for pgp in queryset:
        pgp.generate_key()

class PGPAdmin(admin.ModelAdmin):
    list_display = ['key_type', 'key_length', 'name_real', 'name_email',
                    'name_comment', 'fingerprint']
    actions = [gen_pgp_action]
    exclude = ('fingerprint',)

admin.site.register(Sub, SubAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PGP, PGPAdmin)
