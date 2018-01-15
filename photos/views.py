from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Photo
from .forms import PhotoForm

# Create your views here.
def hello(request):
    return HttpResponse('Hello!')

def detail(request, pk):
    #photo = Photo.objects.get(pk=pk)
    photo = get_object_or_404(Photo, pk=pk)

    messages = (
        '<p>{pk} picture displayed</p>'.format(pk=photo.pk),
        '<p>address {url}</p>'.format(url=photo.image.url),
        '<p><img src="{url}" /></p>'.format(url=photo.image.url),
    )
    return HttpResponse('\n'.join(messages))

@login_required
def create(request):
   if request.method == "GET":
       form = PhotoForm()
   elif request.method == "POST":
       form = PhotoForm(request.POST, request.FILES)

       if form.is_valid():
           obj = form.save(commit=False)
           obj.user = request.user
           obj.save()
           return redirect(obj)

   ctx = { 'form': form, }
   return render(request, 'edit.html', ctx)

