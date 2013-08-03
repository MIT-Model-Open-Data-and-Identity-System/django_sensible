from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class ScopeAdmin(admin.ModelAdmin):
        list_display = ('scope', 'description')
        class Meta:
                verbose_name = 'scope'

admin.site.register(Scope, ScopeAdmin)

class TypeAdmin(admin.ModelAdmin):
        list_display = ('type', )

admin.site.register(Type, TypeAdmin)

class AccessTokenAdmin(admin.ModelAdmin):
        list_display = ('user', 'token')

admin.site.register(AccessToken, AccessTokenAdmin)

class StateAdmin(admin.ModelAdmin):
        list_display = ('user', 'nonce')

admin.site.register(State, StateAdmin)

class AttributeAdmin(admin.ModelAdmin):
        list_display = ('attribute',)

admin.site.register(Attribute, AttributeAdmin)

class FirstLoginInline(admin.StackedInline):
	model = FirstLogin
	can_delete = True

class UserAdmin(UserAdmin):
	inlines = (FirstLoginInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CasInline(admin.StackedInline):
	model = Cas
	can_delete = True

class UserAdmin(UserAdmin):
	inlines = (CasInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
