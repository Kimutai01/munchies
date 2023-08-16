from django.shortcuts import render, HttpResponse, redirect
from .forms import UserForm

# Create your views here.

def registerUser(request):
    form = UserForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.role = user.CUSTOMER
            user.set_password(password)
            user.save()
            return redirect('register-user')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = UserForm()
    
    context = {
        'form': form
    }
    return render(request, 'registerUser.html', context)
