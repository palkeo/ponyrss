from django import forms
from sautadet import spouts

SPOUTS_CHOICES = [(i, i) for i in dir(spouts) if not i.startswith('_')]

class SpoutSelectForm(forms.Form):
    spout_name = forms.ChoiceField(choices=SPOUTS_CHOICES)

class FeedAddForm(forms.Form):
    title = forms.CharField()
    base_score = forms.FloatField(label="Base score")
    mult_score = forms.FloatField(label="Multiply entries score by")
    tags = forms.CharField(help_text="Comma separated tags (will be created if they don't exist)", required=False)

class EmptyForm(forms.Form):
    pass
