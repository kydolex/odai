from django.views.generic import View
from django.shortcuts import render
from .models import Post
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

class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        return render(request, 'app/index.html', {
            'post_data': post_data,
        })