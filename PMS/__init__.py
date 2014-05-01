from django.contrib.auth.models import Group

u=Group.objects.get_or_create(name='Lider')

