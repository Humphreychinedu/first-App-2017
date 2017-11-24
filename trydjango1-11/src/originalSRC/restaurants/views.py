#import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation

# Create your views here.
#function based view


'''
def home(request):
	num = None 
	some_list = [random.randint(0, 100000000), 
				random.randint(0, 1000000000),
				random.randint(0, 1000000000)]
#A condition simply saying that if condition is a boolean, Num = random.randint()
	condition_bool_item = False
	if condition_bool_item:
		num = random.randint(0, 100000000)			
	context = {	"num": num, 
				"some_list":some_list}

	return render(request, "home.html", context)


def about(request):	
	context = {	}

	return render(request, "about.html", context)

def contact(request):			
	context = {	}

	return render(request, "contact.html", context)'''
'''
class ContactView(View):
	def  get(self, request, *args, **kwargs):
		context = {	}
		return render(request, "contact.html", context)
class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, *args, **kwargs):
		context= super(HomeView, self).get_context_data(*args, **kwargs)
		num = None 
		some_list = [random.randint(0, 100000000), 
				random.randint(0, 1000000000),
				random.randint(0, 1000000000)]
#A condition simply saying that if condition is a boolean, Num = random.randint()
		condition_bool_item = True
		if condition_bool_item:
			num = random.randint(0, 100000000)			
		context = {	"num": num, 
					"some_list":some_list}

		return context

#class AboutView(TemplateView):
#	template_name = 'about.html'

#class ContactView(TemplateView):
#	template_name = 'contact.html'

	def  post(self, request, *args, **kwargs):
		print(kwargs)
		context = {	}
		return render(request, "contact.html", context)

	def  put(self, request, *args, **kwargs):
		print(kwargs)
		context = {	}
		return render(request, "contact.html", context)
		'''
@login_required(login_url='/login/')
def restaurant_createview(request):
	form = RestaurantLocationCreateForm(request.POST or None)
	errors = None
	#if request.method == "GET":
	#	print('get data')
	#if request.method == "POST":
		#print('post data')
		#print(request.POST)
		#title = request.POST.get("title")
		#location = request.POST.get("location")
		#category= request.POST.get("category")
		#form = RestaurantCreateForm(request.POST)
	if form.is_valid():
		if request.user.is_authenticated():
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
		#obj = RestaurantLocation.objects.create(
		#		name = form.cleaned_data.get('name'),
		#		location = form.cleaned_data.get('location'),
		#		category = form.cleaned_data.get('category'),

		#	)
			return HttpResponseRedirect("/restaurants/")
		else: 
			return HttpResponseRedirect("/login/")
	if form.errors:
		#print(form.errors)
		errors = form.errors
		
		
	template_name = 'restaurants/form.html'
	context ={"form":form, "errors":errors}
	return render(request, template_name,context)

def restaurant_listview(request,):
	template_name = 'restaurants/restaurants_list.html'
	queryset = RestaurantLocation.objects.all()
	context ={
		"object_list": queryset
	}
	return render(request, template_name,context)


#ListView 
class RestaurantListView(LoginRequiredMixin, ListView):
	
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner = self.request.user)

class RestaurantDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner = self.request.user)

class RestaurantCreateView(LoginRequiredMixin, CreateView):
	form_class = RestaurantLocationCreateForm
	login_url = '/login/'
	template_name = 'form.html'
	#success_url = "/restaurants/"

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.owner = self.request.user
		return super(RestaurantCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Restaurant'
		return context

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
	form_class = RestaurantLocationCreateForm
	login_url = '/login/'
	template_name = 'restaurants/detail-update.html'
	#success_url = "/restaurants/"

	
	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
		name = self.get_object().name
		context['title'] = f'Update Restaurant: {name}'
		return context

	def get_queryset(self):
		return RestaurantLocation.objects.filter(owner = self.request.user)