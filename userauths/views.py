from django.shortcuts import render, redirect
from userauths.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hey {username}, Your account was created successfully")
            new_user = authenticate(request, 
                                    username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            
            login(request, new_user)
            return redirect('core:index')
        else:
            messages.warning(request, form.errors)
    
    else:
        form = UserCreationForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'userauths/register.html', context)
