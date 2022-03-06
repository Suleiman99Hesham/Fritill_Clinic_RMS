from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

# Checks if the user is authenticated,
# to prevent authenticated user to access login and register pages
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# Check the Group of the user
# if prevent who is not an admin to access the view given this decorator,
# and redirect him to the home page
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        else:
            group = Group.objects.get(name='admin')
            request.user.groups.add(group)
        if group == 'Client':
            return redirect('client_dashboard', request.user.client.name)
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func

# Check all the entries of a given list to dtermine if he is allowed or not
# if the user'group is in the allowed_role list so he can access the view
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('You are not autherized to view this page.')
        return wrapper_func
    return decorator