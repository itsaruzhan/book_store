import imp
from django.shortcuts import render, redirect,  get_object_or_404
# Create your views here.
from .forms import NewUserForm
from django.contrib.auth import login,  authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import *
                                       
def home(request):
    return render(request, 'book_advertise/home.html')

def register_request(request):
    if request.method == 'POST':
       
        form = NewUserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('valid')
            
            user = form.save()
            user.refresh_from_db()  
            user.profile.fname = form.cleaned_data.get('first_name')
            user.profile.lname = form.cleaned_data.get('last_name')
            user.profile.phoneNumber = form.cleaned_data.get('phoneNumber')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.save
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('my_profile')

    else:
        form = NewUserForm()
    print('invalid')
    return render(request, 'book_advertise/registration_student.html', {'register_form': form})


def login_request(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
           
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}.")
        return redirect("profile", id = user.id) 
      else:
        messages.error(request,"Invalid username or password.")
    else:
      messages.error(request,"Invalid username or password.")
  form = AuthenticationForm()
  return render(request=request, template_name="book_advertise/login.html", context={"login_form":form})

def mainpage_books(request):
    books1 = Book.objects.filter(category_id=42)
    books2 = Book.objects.filter(category_id=43)
    books3 = Book.objects.filter(category_id=44)
    return render(request, 'book_advertise/main.html', {'books1':books1,'books2':books2, 'books3':books3 })

def my_profile(request, id):
    student = User.objects.get(id=id)
    return render(request, 'book_advertise/profile.html',  context={"user":student})

class DetailCart(DetailView):
    model = Cart
    template_name='cart/detail_cart.html'

class ListCart(ListView):
    model = Cart
    context_object_name = 'carts'
    template_name='cart/list_carts.html'

class CreateCart(CreateView):
    model = Cart
    template_name = 'cart/create_cart.html'

class Updatecart(UpdateView):
    model = Cart
    template_name = 'cart/update_cart.html'

class DeleteCart(DeleteView):
    model = Cart
    template_name = 'cart/delete_cart.html'  

class DetailCartItem(DetailView):
    model = CartItem
    template_name='cartitem/detail_cartitem.html'

class ListCartItem(ListView):
    model = CartItem
    context_object_name = 'cartitems'
    template_name='library/list_cartitems.html'

class CreateCartItem(CreateView):
    model = CartItem
    template_name = 'cartitem/create_cartitem.html'

class UpdateCartItem(UpdateView):
    model = CartItem
    template_name = 'cartitem/update_cartitem.html'

class DeleteCartItem(DeleteView):
    model = Cart
    template_name = 'cartitem/delete_cartitem.html'

    