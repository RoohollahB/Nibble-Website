from django.urls import path
from .views import registerView, LoginView, activate_account, SendActivationMailView, HomeView, LogoutView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('register/', registerView.as_view(), name='registerPage'),
    path('login/', LoginView.as_view(), name='loginPage'),
    path('logout/', LogoutView.as_view(), name='logoutPage'),
    path('activaton-link/<str:email>',SendActivationMailView, name='send-activation'),
    path('activate/<uid>/<token>/', activate_account, name='activateAccount'),
]
