from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth

# Create your views here.

def home(request):
  return render(request, 'accounts/dashboard.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password = password)

    if user is not None:
      auth.login(request, user)
      messages.success(request, 'Logged In')

      return redirect('home')
    else:
      messages.error(request, 'Invalid Credentials')

      return redirect('login')
  
  else:
    return render(request, 'accounts/login.html')

def signup(request):

  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    # Check for passwords
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.error(request, 'Username exists')

        return redirect('signup')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request, 'Email already exists')
          return redirect('signup')
        else:
          # When all looks good
          user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)

          user.save()
          messages.success(request, 'You are now registered and can log in')

          return redirect('login')
    else:
          messages.error(request, 'Passwords do not match')
  return render(request, 'accounts/signup.html')

def logout(request):
    auth.logout(request)

    messages.success(request, 'Logged Out')

    return redirect('home')
