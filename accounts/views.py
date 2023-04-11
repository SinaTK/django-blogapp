from django.shortcuts import redirect, render
from django.views import View
from accounts.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User


# Create your views here.
class UserRegisterView(View):
    class_form = RegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.class_form
        context = {'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            r_form=form.cleaned_data
            user = User.objects.create_user(username=r_form['username'], email=r_form['email'], password=r_form['password'], first_name=r_form['first_name'], last_name=r_form['last_name'])
            messages.success(request, 'You registered successfully.', 'success')
            login(request, user)
            return redirect('home:index')
        else:
            return render(request, self.template_name, {'form':form})
        

class UserLoginView(View):
    class_form = LoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.class_form
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            login_form = form.cleaned_data
            user = authenticate(username=login_form['username'], password=login_form['password'])
            print(user, login_form['username'], login_form['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You log in successfully.')
                if self.next:
                    return redirect(self.next)
                return redirect('home:index')
            else:
                login_error = 'Username or Password is not correct'
                context =  {'form':form, 'login_error': login_error}
                return render(request, self.template_name, context)
        else:
            return redirect('accounts:login')
        

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You log out successfully.')
        return redirect('home:index')

