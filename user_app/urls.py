from django.urls import path, include, re_path
from . import views, social_login
from dj_rest_auth.registration import urls

from .views import CustomRegisterView, ResendEmailVerificationView, CustomVerifyEmailView, \
    CustomPasswordResetConfirmView, CustomPasswordResetView, customPasswordResetView, customPasswordResetConfirmView, \
    user_details, update_profile


urlpatterns = [
    path('send-email/', views.send_test_email, name='send_email'), #RM-FOR mail check


    path('user_details/<int:user_id>', user_details, name='details'),
    path('auth/password/reset/confirm/<id>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('auth/password/reset/confirm/',
         CustomPasswordResetView.as_view(), name='password_reset'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('getUser/', views.getUser, name="getUser"),
    
#     path('permission/', views.ws_permission, name="ws_permission"),
    path('permission/<pk>/<type>/', views.ws_permission, name="ws_permission"),
    
    path('update-me/', update_profile, name="update-me"),

    path('setReferral/', views.setReferral, name="setReferral"),

    path('updateUser/<int:user_id>/', views.updateUser, name="updateUser"),
    path('updateUserProfile/', views.updateUserProfile, name="updateUserProfile"),
    path('auth/google/', social_login.GoogleLogin.as_view(), name='google'),
    path('update_last_online/', views.update_last_online,
         name='update_last_online'),
    path('get_user_by_search_name/', views.get_user_by_search_name,
         name='get_user_by_search_name'),
    path('update_profile_picture/', views.ProfilePictureUpdate.as_view(),
         name='update_profile_picture'),
    path('exchangeCoinToToken/', views.exchangeCoinToToken,
         name='exchangeCoinToToken'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('auth/registration/custom/',
         CustomRegisterView.as_view(), name='rest_register'),
    path('auth/registration/custom-verify-email/',
         CustomVerifyEmailView.as_view(), name='rest_verify_email'),
    path('auth/registration/custom-resend-email/',
         ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('auth/registration/custom-reset-password/',
         customPasswordResetView, name="rest_password_reset"),
    path('auth/registration/custom-reset-password-confirm/',
         customPasswordResetConfirmView, name="rest_password_reset_confirm"),
    # ref

    
]
