from django.contrib import admin
from .models import CastMember,Movie,Review
# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(CastMember)