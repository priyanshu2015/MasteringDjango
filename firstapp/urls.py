from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib import admin
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name="index"),
    path('contactus/', views.contactus2, name="contact"),
    path('contactusclass/', views.ContactUs.as_view(), name="contactclass"),
    path('testsessions/', views.testsessions, name="testsessions"),
    path('firstasyncview/', views.firstasyncview, name="firstasyncview"),

    #path('listproducts/', views.ListProducts.as_view(), name="listproducts"),
    path('listproducts/', views.listProducts, name="listproducts"),
    path('productdetail/<int:pk>/', views.ProductDetail.as_view(), name="productdetail"),
    path('addtocart/<int:id>/', views.addToCart, name="addtocart"),
    path('displaycart/', views.DisplayCart.as_view(), name="displaycart"),
    path('updatecart/<int:pk>/', views.UpdateCart.as_view(), name="updatecart"),
    path('deletefromcart/<int:pk>/', views.DeleteFromCart.as_view(), name="deletefromcart"),

    
    path('addtopremium/', views.addToPremiumGroup, name="addtopremium"),
    #path('premiumproducts/', views.premiumProducts, name="premiumproducts"),
    path('premiumproducts/', views.PremiumProducts.as_view(), name="premiumproducts"),

    path('api/listproductsapi/', views.listProductsApi, name="listproductsapi"),
    path('api/suggestionapi/', views.suggestionApi, name="suggestionapi"),

    # Payment APIs
    path('payment/', views.payment, name = 'payment'),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),
    # Generating Invoice
    path('generateinvoice/<int:pk>/', views.GenerateInvoice.as_view(), name = 'generateinvoice'),


    # Authentication Endpoints
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),


    # change password
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='firstapp/registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='firstapp/registration/password_change.html', success_url = reverse_lazy("password_change_done")), 
        name='password_change'),

    #Forgot password
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "firstapp/registration/password_reset_form.html", success_url = reverse_lazy("password_reset_complete")), 
    name="password_reset_confirm"),  # 3
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "firstapp/registration/password_reset.html", success_url = reverse_lazy("password_reset_done"), email_template_name = 'firstapp/registration/forgot_password_email.html'), 
    name="reset_password"),     # 1
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "firstapp/registration/password_reset_sent.html"), 
    name="password_reset_done"),    # 2
    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "firstapp/registration/password_reset_done.html"), 
    name="password_reset_complete"),   # 4
    
]


# when debug=True
#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL ,document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)














# path('signupcustomer/', views.RegisterViewCustomer.as_view(), name="signupcustomer"),
# path('login/', views.LoginViewUser.as_view(), name="login"),
#     path('logout/', views.LogoutViewUser.as_view(), name="logout"),