from django.shortcuts import render, redirect


def user_page(request):
    if request.user.is_authenticated:
        return render(request, 'user_page.html')
    else:
        return redirect('/sign_in/')
