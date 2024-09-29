from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from .views import PageNotFound
from . import views
from knox import views as knox_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bazigaar apis",
        default_version='v1',
        description="Your API Description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('account_inactive/', views.account_inactive, name='account_inactive'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

    # admin
    path('admin/', admin.site.urls),

    path('api/sup-admin/', include('SuperAdminPanel.urls'),),
    path('api/admin/', include('AdminPanel.urls'),),
    path('api/agent/', include('AgentPanel.urls'),),
    path('lottery/', include('Lottery.urls'),),

    # logout for all user
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout_token'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logout_token_all'),

    # reseller
    path('reseller/', include('reseller_app.urls'),),
    path('leaderboard/', include('leaderboard.urls'),),

    # slider
    path('api/slider/', include('SliderApp.urls'),),
    path('user/', include('user_app.urls'),),
    path('livestream/', include('livestream.urls'),),
    path('follow/', include('follow.urls'),),
    path('notifications/', include('notifications.urls'),),
    path('chatWithFriend/', include('chat_with_friend.urls'),),
    path('chatInGroup/', include('chat_in_group.urls'),),
    path('calling_app2/', include('calling_app2.urls'),),
    path('ticket_draw_app/', include('ticket_draw_app.urls'),),
    path('reseller_app/', include('reseller_app.urls'),),
    path('group_call/', include('group_call.urls'),),
    path('contact_us/', include('contact_us.urls'),),
    path('server_sent_event/', include('server_sent_event.urls'),),
    path('reseller_payment_method/', include('reseller_payment_method.urls'),),
    path('level_and_achievement/', include('level_and_achievement.urls'),),
    path('leaderboard/', include('leaderboard.urls'),),
    path('spinning_game/', include('spinning_game.urls'),),
    path('wallet_app/', include('wallet_app.urls'),),
    path('website/', include('website.urls'),),
    path("*/", PageNotFound, name="page_not_found"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
