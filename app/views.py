from django.views.generic import View
from django.shortcuts import render
from .models import Post,Odai,Title,AddTitle,AddOdai
from accounts.models import CustomUser
from app.forms import AddOdaiForm
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse 
from django.utils import timezone
import datetime
from django.core.mail import send_mail, EmailMessage,BadHeaderError
from django.views import generic
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.utils.timezone import localtime, make_aware
from django.views.decorators.http import require_POST
import json

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        odai=[]
        for i in odai_data:
            odai.append(i.odai)
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'odai':json.dumps(odai),
        })

class DetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Title.objects.order_by("-id")
        title_data = Title.objects.get(title=self.kwargs['title'])
        odai_data = Odai.objects.order_by("?").filter(title=title_data)
        odai=[]
        for i in odai_data:
            odai.append(i.odai)
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'title_data':title_data,
            'odai':json.dumps(odai),
        })

class AddView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        form = AddOdaiForm(request.POST, request.FILES)
        return render(request, 'app/add.html', {
            'post_data': post_data,
            'form':form,
        })
    def post(self, request, *args, **kwargs):
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        form = AddOdaiForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = AddOdai()
            form_data.author = CustomUser.objects.get(id=request.user.id) 
            form_data.title = form.cleaned_data['title']
            form_data.odai = form.cleaned_data['odai']
            form_data.save()
            return redirect('/')
        return render(request, 'app/add.html', {
            'post_data': post_data,
            'form':form,
        })


class Admin_AddView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/')
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        add_odai = AddOdai.objects.order_by("-id")
        form = AddOdaiForm(request.POST, request.FILES)
        return render(request, 'app/add_admin.html', {
            'post_data': post_data,
            'add_odai':add_odai,
            'form':form,
        })
    def post(self, request, *args, **kwargs):
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        add_odai = AddOdai.objects.order_by("-id")
        form = AddOdaiForm(request.POST, request.FILES)

        check = request.POST.getlist[[id]]
        print(check)
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'add_odai':add_odai,
            'form':form,
        })

class Admin_SendView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/')
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        add_odai = AddOdai.objects.order_by("-id")
        form = AddOdaiForm(request.POST, request.FILES)
        check = request.POST.getlist('id')
        for i in check:
            print(i)
        for i in check:
            form_data = Odai()
            post = AddOdai.objects.get(id=i)
            form_data.author = post.author
            form_data.title = post.title
            form_data.odai = post.odai
            post.delete()
            form_data.save()

        # check = request.POST["id"]
        # print(check)
        return render(request, 'app/index.html', {
            'post_data': post_data,
            'add_odai':add_odai,
            'form':form,
        })

class ExplanationView(View):
    def get(self, request, *args, **kwargs):
        post_data = Title.objects.order_by("-id")
        odai_data = Odai.objects.order_by("?")
        odai=[]
        for i in odai_data:
            odai.append(i.odai)
        return render(request, 'app/explanation.html', {
            'post_data': post_data,
            'odai':json.dumps(odai),
        })