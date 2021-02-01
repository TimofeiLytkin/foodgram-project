from django.conf import settings
from django.conf.urls import handler400, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view

from django.urls import include, path


handler400 = 'recipes.views.page_bad_request'  # noqa
handler404 = 'recipes.views.page_not_found'  # noqa
handler500 = 'recipes.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("users.urls")),
    path('about/', include("about.urls")),
    path('api/', include("api.urls")),
    path('', include("recipes.urls")),
]

urlpatterns += [
    path(
        'auth/',
        include(
            [
                path(
                    'login/',
                    auth_view.LoginView.as_view(template_name='authForm.html'),
                    name='login',
                ),
                path(
                    'logout/',
                    auth_view.LogoutView.as_view(
                        template_name='logged_out.html'
                    ),
                    name='logout',
                ),
                path(
                    'password_change/',
                    auth_view.PasswordChangeView.as_view(
                        template_name='changePassword.html'
                    ),
                    name='password_change',
                ),
                path(
                    'password_change/done/',
                    auth_view.PasswordChangeDoneView.as_view(
                        template_name='password_change_done.html'
                    ),
                    name='password_change_done',
                ),
                path(
                    'password_reset/',
                    auth_view.PasswordResetView.as_view(
                        template_name='resetPassword.html'
                    ),
                    name='password_reset',
                ),
                path(
                    'reset/<uidb64>/<token>/',
                    auth_view.PasswordResetConfirmView.as_view(
                        template_name='password_reset_confirm.html'
                    ),
                    name='password_reset_confirm',
                ),
                path(
                    'password_reset/done/',
                    auth_view.PasswordResetDoneView.as_view(
                        template_name='password_reset_done.html'
                    ),
                    name='password_reset_done',
                ),
            ]
        ),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
