
from django import forms


import items.models

import solicitudesCambio.models


class VotoForm(forms.ModelForm):
    class Meta:
        model=solicitudesCambio.models.Voto
        fields=['voto']