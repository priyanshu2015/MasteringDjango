from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.core.exceptions import ValidationError
from .forms import ContactUsForm, RegistrationFormSeller, RegistrationForm, RegistrationFormSeller2, CartForm
from django.urls import reverse_lazy, reverse
from .models import SellerAdditional, CustomUser, Contact, Product, ProductInCart, Cart
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin


from firstproject import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# def index(request):
#     age = 10
#     arr = ['priyanshu', 'aman', 'rohit', 'shubhi']
#     dic = {'a':'one', 'b':'two'}
#     return render(request, 'firstapp/index.html', {'age':age, 'array':arr, 'dic':dic})
#     #return HttpResponse("<h1>Hello</h1>")

class Index(TemplateView):
    template_name = 'firstapp/index.html'
    def get_context_data(self, **kwargs):
        age = 10
        arr = ['priyanshu', 'aman', 'rohit', 'shubhi']
        dic = {'a':'one', 'b':'two'}
        context_old = super().get_context_data(**kwargs)
        context = {'age':age, 'array':arr, 'dic':dic, 'context_old':context_old}
        return context



def testsessions(request):
    if request.session.get('test', False):
        print(request.session["test"])
    #request.session.set_expiry(1)
    # if request.session['test']:
    #     print(request.session['test'])
    request.session['test'] = "testing"
    request.session['test2'] = "testing2"
    return render(request, "firstapp/sessiontesting.html")





def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST['phone']
        if len(phone)<10 or len(phone)>10:
            raise ValidationError("Phone number length is not right")
        query = request.POST['query']
        print(name + " " + email + " " + phone + " " +query)
    return render(request, 'firstapp/contactus.html')

def contactus2(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():      #clean_data
            if len(form.cleaned_data.get('query'))>10:
                form.add_error('query', 'Query length is not right')
                return render(request, 'firstapp/contactus2.html', {'form':form})
            form.save()
            return HttpResponse("Thank YOu")
        else:
            if len(form.cleaned_data.get('query'))>10:
                #form.add_error('query', 'Query length is not right')
                form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
            return render(request, 'firstapp/contactus2.html', {'form':form})
    return render(request, 'firstapp/contactus2.html', {'form':ContactUsForm})

class ContactUs(FormView):
    form_class = ContactUsForm
    template_name = 'firstapp/contactus2.html'
    #success_url = '/'   #hardcoded url
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            return render(self.request, 'firstapp/contactus2.html', {'form':form})
        form.save()
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            #form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
        response = super().form_invalid(form)
        return response


# class RegisterViewSeller(CreateView):
#     template_name = 'firstapp/register.html'
#     form_class = RegistrationFormSeller
#     success_url = reverse_lazy('index')

#     def post(self, request, *args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         if response.status_code == 302:
#             gst = request.POST.get('gst')
#             warehouse_location = request.POST.get('warehouse_location')
#             user = CustomUser.objects.get(email = request.POST.get('email'))
#             s_add = SellerAdditional.objects.create(user = user, gst = gst, warehouse_location = warehouse_location)
#             return response
#         else:
#             return response

class RegisterView(CreateView):
    template_name = 'firstapp/registerbasicuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('signup')

    def post(self, request, *args, **kwargs):
        #form = RegistrationForm(request.POST)
        user_email = request.POST.get('email')
        try:
            existing_user = CustomUser.objects.get(email = user_email)
            if(existing_user.is_active == False):
                existing_user.delete()
        except:
            pass
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = CustomUser.objects.get(email = user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)     #www.wondershop.in:8000  127.0.0.1:8000 
            mail_subject = 'Activate your account.'
            message = render_to_string('firstapp/registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            #print(message)
            to_email = user_email   
            #form = RegistrationForm(request.POST)   # here we are again calling all its validations
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list= [to_email],
                    fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
                )
                messages.success(request, "link has been sent to your email id. please check your inbox and if its not there check your spam as well.")
                return self.render_to_response({'form':form})
            except:
                form.add_error('', 'Error Occured In Sending Mail, Try Again')
                messages.error(request, "Error Occured In Sending Mail, Try Again")
                return self.render_to_response({'form':form})
        else:
            return response


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully Logged In")
        return redirect(reverse_lazy('index'))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')

class LoginViewUser(LoginView):
    template_name = "firstapp/login.html"
    #success_url = reverse_lazy('index')

# class RegisterViewSeller(LoginRequiredMixin, CreateView):
#     template_name = 'firstapp/registerseller.html'
#     form_class = RegistrationFormSeller2
#     success_url = reverse_lazy('index')

#     def form_valid(self, form):
#         user = self.request.user
#         user.type.append(user.Types.SELLER)
#         user.save()
#         form.instance.user = self.request.user
#         return super().form_valid(form)
        

class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('index')


class ListProducts(ListView):
    template_name = "firstapp/listproducts.html"
    model = Product
    context_object_name = "product"
    paginate_by = 2



from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
PRODUCTS_PER_PAGE = 2
def listProducts(request):
    
    ordering = request.GET.get('ordering', "")     # http://www.wondershop.in:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('search', "")
    price = request.GET.get('price', "")

    if search:
        product = Product.objects.filter(Q(product_name__icontains=search) | Q(brand__icontains=search)) # SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite

    else:
        product = Product.objects.all()

    if ordering:
        product = product.order_by(ordering) 

    if price:
        product = product.filter(price__lt = price)
    

    # Pagination
    page = request.GET.get('page',1)
    product_paginator = Paginator(product, PRODUCTS_PER_PAGE)
    try:
        product = product_paginator.page(page)
    except EmptyPage:
        product = product_paginator.page(product_paginator.num_pages)
    except:
        product = product_paginator.page(PRODUCTS_PER_PAGE)
    return render(request, "firstapp/listproducts.html", {"product":product, 'page_obj':product, 'is_paginated':True, 'paginator':product_paginator})


def suggestionApi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Product.objects.filter(Q(product_name__icontains=search))[0:10]
        # print(list(qs.values()))
        # print(json.dumps(list(qs.values()), cls = DjangoJSONEncoder))
        titles = list()
        for product in qs:
            titles.append(product.product_name)
        #print(titles)
        if len(qs)<10:
            length = 10 - len(qs)
            qs2 = Product.objects.filter(Q(brand__icontains=search))[0:length]
            for product in qs2:
                titles.append(product.brand)
        return JsonResponse(titles, safe=False)      # [1,2,3,4] ---> "[1,2,3,4]"   queryset ---> serialize into list or dict format ---> json format using json.dumps with a DjangoJSONEncoder(encoder to handle datetime like objects)




def listProductsApi(request):
    # print(Product.objects.all())
    # print(Product.objects.values())
    #result = json.dumps(list(Product.objects.values()), sort_keys=False, indent=0, cls=DjangoJSONEncoder)   # will return error if you have a datetime object as it is not jsonserializable  so thats why use DjangoJSONEncoder, indent to beautify and sort_keys to sort keys
    #print(type(result))    #str type  
    #print(result)
    result = list(Product.objects.values())          # will work like passing queryset as a context data if used by a template
    #print(result)
    #return render(request, "firstapp/listproducts.html", {"product":result})
    return JsonResponse(result, safe=False)




class ProductDetail(DetailView):
    model = Product
    template_name = "firstapp/productdetail.html"
    context_object_name = "product"


@login_required
def addToCart(request, id):
    try:
        cart = Cart.objects.get(user = request.user)
        try:
            product = Product.objects.get(product_id = id)
            try:
                productincart = ProductInCart.objects.get(cart = cart, product = product)
                productincart.quantity = productincart.quantity + 1
                productincart.save()
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
            except:
                productincart = ProductInCart.objects.create(cart = cart, product = product, quantity=1)
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Product can not be found")
            return redirect(reverse_lazy('listproducts'))
    except:
        cart = Cart.objects.create(user = request.user)
        try:
            product = Product.objects.get(product_id = id)
            productincart = ProductInCart.objects.create(cart = cart, product = product, quantity = 1)
            messages.success(request, "Successfully added to cart")
            return redirect(reverse_lazy("displaycart"))
        except:
            messages.error(request, "Error in adding to cart. Please try again")
            return redirect(reverse_lazy('listproducts'))


class DisplayCart(LoginRequiredMixin, ListView):
    model = ProductInCart
    template_name = "firstapp/displaycart.html"
    context_object_name = "cart"

    def get_queryset(self):
        queryset = ProductInCart.objects.filter(cart = self.request.user.cart)
        return queryset

class UpdateCart(LoginRequiredMixin, UpdateView):
    model = ProductInCart
    form_class = CartForm
    success_url = reverse_lazy("displaycart")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            if int(request.POST.get("quantity")) == 0:
                productincart = self.get_object()
                productincart.delete()
            return response
        else:
            messages.error(request, "error in quantity")
            return redirect(reverse_lazy("displaycart"))

class DeleteFromCart(LoginRequiredMixin, DeleteView):
    model = ProductInCart
    success_url = reverse_lazy("displaycart")  



# Adding Payment Gateway
import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

from .models import Order, ProductInOrder, Cart

@login_required
def payment(request):
    if request.method == "POST":
        try:
            cart = Cart.objects.get(user = request.user)
            products_in_cart = ProductInCart.objects.filter(cart = cart)
            final_price = 0
            if(len(products_in_cart)>0):
                order = Order.objects.create(user = request.user, total_amount = 0)
                # order.save()
                for product in products_in_cart:
                    product_in_order = ProductInOrder.objects.create(order = order, product = product.product, quantity = product.quantity, price = product.product.price)
                    final_price = final_price + (product.product.price * product.quantity)
            else:
                return HttpResponse("No product in cart")
        except:
            return HttpResponse("No product in cart")

        order.total_amount = final_price
        order.save()

        order_currency = 'INR'

        callback_url = 'http://'+ str(get_current_site(request))+"/handlerequest/"
        print(callback_url)
        notes = {'order-type': "basic order from the website", 'key':'value'}
        razorpay_order = razorpay_client.order.create(dict(amount=final_price*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        return render(request, 'firstapp/payment/paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':final_price, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})
    else:
        return HttpResponse("505 Not Found") 


# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os



def fetch_resources(uri, rel):
    path = os.path.join(uri.replace(settings.STATIC_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

from django.core.mail import EmailMultiAlternatives
@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                amount = order_db.total_amount * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()

                    ## For generating Invoice PDF
                    template = get_template('firstapp/payment/invoice.html')
                    data = {
                        'order_id': order_db.order_id,
                        'transaction_id': order_db.razorpay_payment_id,
                        'user_email': order_db.user.email,
                        'date': str(order_db.datetime_of_payment),
                        'name': order_db.user.name,
                        'order': order_db,
                        'amount': order_db.total_amount,
                    }
                    html  = template.render(data)
                    result = BytesIO()
                    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
                    pdf = result.getvalue()
                    filename = 'Invoice_' + data['order_id'] + '.pdf'

                    mail_subject = 'Recent Order Details'
                    # message = render_to_string('firstapp/payment/emailinvoice.html', {
                    #     'user': order_db.user,
                    #     'order': order_db
                    # })
                    context_dict = {
                        'user': order_db.user,
                        'order': order_db
                    }
                    template = get_template('firstapp/payment/emailinvoice.html')
                    message  = template.render(context_dict)
                    to_email = order_db.user.email
                    # email = EmailMessage(
                    #     mail_subject,
                    #     message, 
                    #     settings.EMAIL_HOST_USER,
                    #     [to_email]
                    # )

                    # for including css(only inline css works) in mail and remove autoescape off
                    email = EmailMultiAlternatives(
                        mail_subject,
                        "hello",       # necessary to pass some message here
                        settings.EMAIL_HOST_USER,
                        [to_email]
                    )
                    email.attach_alternative(message, "text/html")
                    email.attach(filename, pdf, 'application/pdf')
                    email.send(fail_silently=False)

                    return render(request, 'firstapp/payment/paymentsuccess.html',{'id':order_db.id})
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, 'firstapp/payment/paymentfailed.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                return render(request, 'firstapp/payment/paymentfailed.html')
        except:
            return HttpResponse("505 not found")


class GenerateInvoice(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            order_db = Order.objects.get(id = pk, user = request.user, payment_status = 1)     #you can filter using order_id as well
        except:
            return HttpResponse("505 Not Found")
        data = {
            'order_id': order_db.order_id,
            'transaction_id': order_db.razorpay_payment_id,
            'user_email': order_db.user.email,
            'date': str(order_db.datetime_of_payment),
            'name': order_db.user.name,
            'order': order_db,
            'amount': order_db.total_amount,
        }
        pdf = render_to_pdf('firstapp/payment/invoice.html', data)
        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")






# Relating To Group

# to make a new group you can do that like any other models by creating a new record in it

# associating a user to a group
from django.contrib.auth.models import Group
@login_required
def addToPremiumGroup(request):
    group = Group.objects.get(name="premium")
    request.user.groups.add(group)
    return HttpResponse("successfully added")


# checking group not permission 
# in function based view inside the view or "custom decorator"
from .models import PremiumProduct
# from .decorators import group_required
# @group_required('premium')
# def premiumProducts(request):       
#     #if request.user.groups.filter(name = "premium").exists():
#         product = PremiumProduct.objects.all()
#         return render(request, "firstapp/listpremiumproducts.html", {"product":product})

#     #else:
#         #return HttpResponse("Only for premium members")

# # in class based view inside the view or a "custom mixin"
# from .mixins import CheckPremiumGroupMixin
# class PremiumProducts(CheckPremiumGroupMixin, ListView):
#     template_name = "firstapp/listpremiumproducts.html"
#     model = PremiumProduct
#     context_object_name = "product"
#     #paginate_by = 2



# Relating To Permission
# checking permission and that permission can belong to that user or to the group that user is associated
from django.contrib.auth.decorators import permission_required
@permission_required('firstapp.view_premiumproduct')
def premiumProducts(request):
    # ct = ContentType.objects.get_for_model(PremiumProduct)     
    # if request.user.permissions.filter(codename = "view_premiumproducts" , contentype = ct).exists():
    
    #if request.user.has_perm('firstapp.view_premiumproduct'):
        product = PremiumProduct.objects.all()
        return render(request, "firstapp/listpremiumproducts.html", {"product":product})
    # else:
    #     return HttpResponse("Not allowed")


from django.contrib.auth.mixins import PermissionRequiredMixin
class PremiumProducts(PermissionRequiredMixin, ListView):
    template_name = "firstapp/listpremiumproducts.html"
    model = PremiumProduct
    context_object_name = "product"
    paginate_by = 2
    permission_required = "firstapp.view_premiumproduct"  # if using PermissionRequiredMixin


# for creating permissions
#1 Creating Custom Model Depenedent Permission through Code
#from django.contrib.auth.models import Group, ContentType, Permission
# ct = ContentType.objects.get_for_model(PremiumProduct)
# permission = Permission.objects.create(codename="can_do_this", contentype = ct)


#2 Creating Custom Model Dependent Permission by adding in Meta of that model

#3 Creating Custom Model Independent Permission by creating a separate model for permissions

# filtering existing permissions
# ct = ContentType.obejcts.get_for_model(PremiumProduct)
# permission = Permission.objects.get(codename='view_premiumproduct', content_type=ct)


# Adding permission to user
# user.permissions.add(permission)

# Adding permission to group
# new_group, created = Group.objects.get_or_create(name="new_group")
# new_group.permissions.add(permission)




































        




