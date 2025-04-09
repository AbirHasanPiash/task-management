from django.urls import path
from users.views import SignUpView, sign_out, ActivateUserView, AdminDashboardView, AssignRoleView, CreateGroupView, GroupListView, CustomLoginView, ProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView, EditProfileView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    # path('sign-up/', sign_up, name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/', sign_out, name='logout'),
    path('sign-out/', LogoutView.as_view(), name='logout'),
    path('activate/<int:user_id>/<str:token>/', ActivateUserView.as_view(), name='activate-user'),
    # path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    # path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', AssignRoleView.as_view(), name='assign-role'),
    # path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', CreateGroupView.as_view(), name='create-group'),
    # path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', GroupListView.as_view(), name='group-list'),
    # path('admin/group-list/', group_list, name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')
]