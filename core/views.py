from django.shortcuts import render


def home(request):
    return render(request, "core/index.html")


def story(request):
    return render(request, "core/story.html")