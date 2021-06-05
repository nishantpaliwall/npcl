from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import MLSelectModelForm, predictAdvertisementClick

from .models import ml_models
from .linear_regression.HelloWord import get_hello_word
from .linear_regression.linearModels import LinearModels
from joblib import load 
 
import os

# Create your views here.
def home(request):
    return render(request, "machine_learning/home.html")

def about(request):
    return render(request, "machine_learning/about.html")


class MLDetailView(DetailView):
    model = ml_models

class MLListView(ListView):
    model = ml_models
    template_name = 'machine_learning/home.html' # <app>/<model>_<viewType>.html
    context_object_name = 'model_list'
    ordering = ['-create_date'] # to change the display order on UI DESC order
   


class MLCreateView(LoginRequiredMixin, CreateView):
    model = ml_models
    fields = ['model_name', 'description']

    def form_valid(self, form): # Override the parent class method to set values like user/author
        form.instance.created_by = self.request.user # created_by
        return super().form_valid(form)


class MLUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ml_models
    fields = ['model_name', 'description']

    def form_valid(self, form): # Override the parent class method to set values like user/author
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self): # To check if modifications are being done by the same user who created the entry
        current_user = self.get_object()
        if self.request.user == current_user.created_by:
            return True
        return False        


class MLDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ml_models
    success_url = '/' # if deleted succesfully reditect to home page
    
    def test_func(self): # To check if modifications are being done by the same user who created the entry
        current_user = self.get_object()
        if self.request.user == current_user.created_by:
            return True
        return False  


def MLModelExecuteView(request):
    print("Request Type Is")
    print(request.method)
    return render(request, "machine_learning/ml_models_execute.html",{'data': get_hello_word()})       


def temp_homeView(request):
    if request.method == 'POST':
        form = MLSelectModelForm(request.POST)
        print("FORM Details: ")
        print(form)
        if form.is_valid():
            pass 
    else:
        form = MLSelectModelForm()  

    return render(request, 'machine_learning/temp_home.html', {'form': form})      

def displayECSModelResults(request):
    lm = LinearModels()
    content = lm.EcommerceCustomersShopping() 
    print(content['0'])
    #print(content['index'])
    return render(request, "machine_learning/ecs_linear_model.html",{'content': content['0']} )  

def predictAdvertisementClickView(request):
    if request.method == 'POST':
        form = predictAdvertisementClick(request.POST)
        print("FORM Details: ")
        print(form)
        
        
        Daily_Time_Spent_On_Site = form.cleaned_data["Daily_Time_Spent_On_Site"]
        Age = form.cleaned_data["Age"]
        Area_Income = form.cleaned_data["Area_Income"]
        Daily_Internet_Usage = form.cleaned_data["Daily_Internet_Usage"]
        Male = form.cleaned_data["Male"]
        data = [Daily_Time_Spent_On_Site, Age, Area_Income, Daily_Internet_Usage, Male]
        print(data)
        
        #model = os.path.join(settings.,'LR_clickAdvertisement.sav')
        model = load("machine_learning/logistic_regression/LR_clickAdvertisement.sav")

        prediction = model.predict([data])
        
        print(prediction)
        if form.is_valid():
            return render(request, "machine_learning/advertisement_click.html" , {'form': form}) 
            #return redirect('login') # Login page   
    else:
        form = predictAdvertisementClick()

    return render(request, "machine_learning/advertisement_click.html" , {'form': form})    