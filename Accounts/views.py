from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

@login_required
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('course_list')  # Redirect to the 'courses' page
        
        else:
            # Handle invalid login
            return render(request, 'Accounts/login.html', {'error_message': 'Invalid username or password.'})
    
    return render(request, 'Accounts/login.html')