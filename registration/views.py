from django.shortcuts import render,reverse ,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserRegistrationForm,ImageForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate,login
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from .models import show_image
def index(request):
    form = ImageForm(request.FILES)
    if request.method == "POST":

        p = show_image(request.FILES['pics'])
        p.save()
    context={
        'form':form
    }

    return render(request,'image.html',context)
# Create your views here.
def user_login(request):
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user= authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    HttpResponseRedirect(reverse('index'))
                else:
                    HttpResponse('user is not active')
            else:
                HttpResponse('User is not authenticated')
    else:
        form = UserLogin()
    context = {
        'form':form,
    }
    return render(request,'login.html',context)



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please Confirm you email')
    else:
            form = UserRegistrationForm()
    context = {
            'form':form
        }
    return render(request,'register.html',context)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')





