from django.shortcuts import render, redirect
from django.contrib import auth, messages

# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        q = request.GET.get("q")
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            if not request.user.user_type == "Administrator":
                messages.error(request, "No account found")
                auth.logout(request)
                return redirect("admin_login")
            if 'next' in request.GET:
                return redirect(q)
            else:
                return redirect("home")
        else:
            messages.error(request, "Incorrect Email Address or Password")
    return render(request, 'admin_login.html')