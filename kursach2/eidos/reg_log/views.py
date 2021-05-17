from django.shortcuts import render

def reg(request):
    return render(request, 'reg_log/registration.html')
