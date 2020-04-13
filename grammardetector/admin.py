from django.contrib import admin
from .models import Phrases,Mots,Tags, Entrees, Prononciations #classe créées dans models

admin.site.register(Phrases)
admin.site.register(Mots)
admin.site.register(Tags)
admin.site.register(Entrees)
admin.site.register(Prononciations)

