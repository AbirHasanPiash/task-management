from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from users.forms import CustomRegistrationForm, AssignRoleForm, CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm
from django.contrib import messages
from django.contrib import messages
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView, CreateView
from django.views import View

User = get_user_model()



class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

class SignUpView(FormView):
    template_name = 'registration/register.html'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()

        messages.success(
            self.request,
            'A Confirmation mail sent. Please check your email'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is not valid")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')


class ActivateUserView(View):
    def get(self, request, user_id, token, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('sign-in')
            else:
                return HttpResponse('Invalid Id or token')
        except User.DoesNotExist:
            return HttpResponse('User not found')



admin_required = user_passes_test(is_admin, login_url='no-permission')

@method_decorator(admin_required, name='dispatch')
class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()

        for user in users:
            if user.all_groups:
                user.group_name = user.all_groups[0].name
            else:
                user.group_name = 'No Group Assigned'

        context['users'] = users
        return context


@method_decorator(admin_required, name='dispatch')
class AssignRoleView(FormView):
    template_name = 'admin/assign_role.html'
    form_class = AssignRoleForm

    def dispatch(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, id=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        user = self.user_instance
        user.groups.clear()
        user.groups.add(role)
        messages.success(self.request, f"User {user.username} has been assigned to the {role.name} role")
        return redirect('admin-dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user_instance
        return context


@method_decorator(admin_required, name='dispatch')
class CreateGroupView(CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('create-group')

    def form_valid(self, form):
        response = super().form_valid(form)
        group = form.instance
        messages.success(self.request, f"Group {group.name} has been created successfully")
        return response


@method_decorator(admin_required, name='dispatch')
class GroupListView(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()



class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)