from django.forms import ModelForm

from api.models import Cotes


class CotesForm(ModelForm):
    class Meta:
        model = Cotes
        fields = ['label','ponderation','date', 'ponderation_blobal']