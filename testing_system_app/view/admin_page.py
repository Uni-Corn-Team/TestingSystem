from django.shortcuts import render, redirect


def admin_page(request):
    if request.user.is_authenticated:
        return render(request, 'admin_page.html')
    else:
        return redirect('/sign_in/')

