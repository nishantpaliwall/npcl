from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import cls_view_details
#from django.http import HttpResponse
"""
view_details = [
    {   'name': 'DART_EQ_Trade_view'
        ,'region': 'HK'
        ,'create_date': 'July 22, 2020'

},
{   'name': 'DART_FI_Trade_view'
        ,'region': 'HK'
        ,'create_date': 'July 22, 2020'

}
]
"""
# Create your views here.
def home(request):
    content = {
        'view_details': cls_view_details.objects.all()
    }
    #return HttpResponse('<h1>View Home</h1>')
    return render(request, 'dart/home.html', content)


class DartListView(ListView):
    model = cls_view_details
    template_name = 'dart/home.html' # <app>/<model>_<viewType>.html
    context_object_name = 'view_details'
    ordering = ['-create_date'] # to change the display order on UI DESC order
    paginate_by = 3

# User dart list view 
class UserDartListView(ListView):
    model = cls_view_details
    template_name = 'dart/user_darts.html' # <app>/<model>_<viewType>.html
    context_object_name = 'view_details'
    ordering = ['-create_date'] # to change the display order on UI DESC order
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username')) # If user exists then retun user else through 404 error
        return cls_view_details.objects.filter(user=user).order_by('-create_date')

        
class DartDetailView(DetailView):
    model = cls_view_details


class DartCreateView(LoginRequiredMixin, CreateView):
    model = cls_view_details
    fields = ['tittle', 'name', 'region']

    def form_valid(self, form): # Override the parent class method to set values like user/author
        form.instance.user = self.request.user
        return super().form_valid(form)

class DartUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = cls_view_details
    fields = ['tittle', 'name', 'region']

    def form_valid(self, form): # Override the parent class method to set values like user/author
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self): # To check if modifications are being done by the same user who created the entry
        dart = self.get_object()
        if self.request.user == dart.user:
            return True
        return False        


class DartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = cls_view_details
    success_url = '/' # if deleted succesfully reditect to home page
    
    def test_func(self): # To check if modifications are being done by the same user who created the entry
        dart = self.get_object()
        if self.request.user == dart.user:
            return True
        return False  


def about(request):
    #return HttpResponse('<h1>View about</h1>')
    return render(request, 'dart/about.html', {'title': 'DART View List'})