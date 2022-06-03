from django.shortcuts import render, redirect
#from urllib3 import HTTPResponse
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def generate(request):
    s1 = request.POST['string1']
    a = 0
    for i in s1:
        a+=ord(i) #taking the sum of the ascii values of the characters in the given string

    sum = 0
    for digit in str(a):
        sum+=int(digit)  #taking the sum of digits of a
    
    c1 = chr((sum*1000 % 26) + 65) #Taking characters in Capital letters
    c2 = chr((sum*1500 % 26) + 65)
    c3 = chr((sum*2000 % 26) + 65)
    c1, c2, c3 = c1+c2+c3, c2+c3+c1, c3+c1+c2 #Performing some operation to construct the evaluted strings
    l = [c1, c2, c3]

    return render(request, "home.html", {'s1':s1, 'l':l})