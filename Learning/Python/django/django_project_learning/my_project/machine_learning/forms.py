from django import forms

from .models import ml_models

# Create machine learning specefic forms
 
class MLSelectModelForm(forms.Form):
    model_list = forms.ModelChoiceField(queryset=ml_models.objects.distinct().order_by('model_name'), 
                                        label="Models"
    )
    class meta:
        #model = ml_models
        fields = ["model_list"]


class predictAdvertisementClick(forms.Form):
    Daily_Time_Spent_On_Site = forms.FloatField()
    Age = forms.IntegerField()
    Area_Income = forms.FloatField()
    Daily_Internet_Usage = forms.IntegerField()
    Male = forms.IntegerField()
    
    class meta:
        fields = ['Daily_Time_Spent_On_Site', 'Age', 'Area_Income', 'Daily_Internet_Usage', 'Male']