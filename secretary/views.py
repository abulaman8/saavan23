from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Secretary
from event.models import Event


def secretary_required(view_func):
    @login_required(login_url='/secretary/login/')
    def wrap(request, *args, **kwargs):
        try:
            secretary = Secretary.objects.get(user=request.user)
            if secretary:
                return view_func(request, *args, **kwargs)
        
            else:
                messages.error(request, 'You are not authorized to view this page')
                return redirect('/secretary/login/')
        except Secretary.DoesNotExist:
            messages.error(request, 'You are not authorized to view this page')
            return redirect('/secretary/login/')
    return wrap


def secretary_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                secretary = Secretary.objects.get(user=user)
                if secretary:
                    login(request, user)
                    return redirect('/secretary')
                else:
                    messages.error(
                            request,
                            'Secretary not found with this user, if you are a secretary please contact the web admin'
                            )
                    return render(request, 'login.html')
            except Secretary.DoesNotExist:
                messages.error(
                        request,
                        'Secretary not found with this user, if you are a secretary please contact the web admin'
                        )
                return render(request, 'login.html')
        else:
            messages.error(request, 'Username or password not correct')
            return render(request, 'login.html')
            
    else:
        return render(request, 'login.html')


@secretary_required
def secretary_home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


@secretary_required
def event_details(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        return render(request, 'event_details.html', {'event': event})
    except Event.DoesNotExist:
        messages.error(request, 'Event not found')
        return redirect('/secretary')


@secretary_required
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, 'Event deleted successfully')
        return redirect('/secretary')
    except Event.DoesNotExist:
        messages.error(request, 'Event not found')
        return redirect('/secretary')


def secretary_logout(request):
    logout(request)
    return redirect('/secretary/login/')


