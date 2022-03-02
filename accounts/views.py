from django.views import View
from app.models import Post
from accounts.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account import views
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from accounts.forms import  UserCreateForm,UserCreateForm2,ProfileForm
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.conf import settings
from django.views import generic
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage,BadHeaderError
User = get_user_model()
from django.contrib.auth import login
from accounts.forms import ContactForm


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class UserCreate(views.SignupView):
    template_name = 'accounts/user_create.html'
    form_class = UserCreateForm
    def form_valid(self, form):
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        subject = "アカウント仮登録"
        message = render_to_string('accounts/mail_template/message_2.txt',context)
        from_email = 'kydolex@gmail.com'
        recipient_list = [user.email,'kydolex@gmail.com'] # 宛先リスト
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse('無効なヘッダが検出されました。')
        # user.email(subject, message)
        return redirect('user_create_done')


class UserCreateDone(generic.TemplateView):
    template_name = 'accounts/user_create_done.html'


class UserCreateComplete(views.LoginView):
    template_name = 'accounts/user_create_complte.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
    def get(self, request, **kwargs):
        # """tokenが正しければ本登録"""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()
        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()
        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest()

class RuleView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        return render(request, 'accounts/rule.html', {
            'post_data': post_data,
        })

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
        })

class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'user_name': user_data.user_name,
                'user_id': user_data.user_id,
                'content': user_data.content,
                'icon': user_data.icon,
                'header': user_data.header,
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'user_data':user_data,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.user_name = form.cleaned_data['user_name']
            user_data.user_id = form.cleaned_data['user_id']
            user_data.content = form.cleaned_data['content']

            if request.FILES.get('icon'):
                user_data.icon = request.FILES.get('icon')
                
            if request.FILES.get('header'):
                user_data.header = request.FILES.get('header')
                
            user_data.save()

            return redirect('profile')

        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'form': form,
            
        })

