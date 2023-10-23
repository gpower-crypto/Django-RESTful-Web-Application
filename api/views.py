from django.shortcuts import render

# Create your views here.

# render the home page
def displayHomePage(request):
    return render(request, 'homePage.html')