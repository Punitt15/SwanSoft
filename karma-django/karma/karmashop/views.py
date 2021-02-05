from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken import models as token_models
from . import forms as my_forms
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
import json
from . import models as core_models
from . import tasks as core_tasks

# Create your views here.


class LoginView(FormView):
    template_name = "login.html"
    title = "login"
    success_url =reverse_lazy('index')
    form_class = my_forms.LoginForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username = username,password=password)
        if user:
            login(self.request,user)
            print("***** successfully Logged in......*****")
            token_instance = token_models.Token.objects.filter(user=user).last()
            if token_instance:
                token_instance.delete()
            token_instance, _ = token_models.Token.objects.get_or_create(user=user)
            print(token_instance)
        else:
            print("user doesnot exist..")
            return render(self.request,"login.html",{'form': form})
        return super(LoginView, self).form_valid(form)


def Logout(request):
    print(request.user)
    token_instance = token_models.Token.objects.filter(user=request.user).last()
    logout(request)
    if token_instance:
        try:
            token_instance.delete()
        except:
            pass
    return redirect('/login/')



def register(request):
    form = my_forms.SignUpForm()

    if request.method == "POST":
        form = my_forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Account Created Successfully  Please Login "
            messages.success(request,message)
            return redirect('/login/')
    return render(request,"register.html",{"form" : form})


class index(TemplateView):
    template_name = "index.html"
    model = core_models.Product
    context_object_name = 'products'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,*kwargs)
        context['categories'] = core_models.Product.objects.values('category').order_by().annotate(Count('category'))
        context['order'] = {'get_cart_total': {'total_items': 0}}
        print(context)
        context['products'] = core_models.Product.objects.all()
        if self.request.user.is_authenticated:
            order_instance = core_models.Order.objects.filter(user=self.request.user, is_completed=False).last()
            if order_instance:
                context['order'] = order_instance
        return context

class ProfileView(TemplateView):
    template_name = "profile.html"

    def post(self,request):
        form = my_forms.ProfileForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data["firstname"]
            lastname = form.cleaned_data["lastname"]
            mobileno = form.cleaned_data['mobileno']
            alternatemobile = form.cleaned_data["alternamemobile"]
            addressone = form.cleaned_data["addressline1"]
            addresstwo = form.cleaned_data["addressline2"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            country = form.cleaned_data["country"]
            user_instance = request.user
            profile_instance = core_models.Profile.objects.filter(user_id=user_instance).last()

            if profile_instance:
                add_inst,created = core_models.Address.objects.get_or_create(address_line1 = addressone,
                                                                     address_line2 = addresstwo,
                                                                     city = city,
                                                                     state = state,
                                                                     zipcode = zipcode,
                                                                     country = country)

                profile_instance.address.add(add_inst)
                add_inst.save()
                user_instance.first_name = firstname
                user_instance.last_name = lastname
                user_instance.save()
                profile_instance.mobile_number = mobileno
                profile_instance.alternate_mobile_number = alternatemobile
                profile_instance.save()



            else:
                profile_instance = core_models.Profile(user_id = user_instance,
                                                         mobile_number = mobileno,
                                                         alternate_mobile_number = alternatemobile,
                                                         )
                profile_instance.save()

                add_inst = core_models.Address(address_line1 = addressone,
                                                 address_line2 = addresstwo,
                                                 city = city,
                                                 state = state,
                                                 zipcode = zipcode,
                                                 country = country)
                add_inst.save()
                profile_instance.address.add(add_inst)
                profile_instance.save()
            messages.add_message(request, messages.SUCCESS, "Profile updated successfully .....")
        return redirect('/profile/')

    def get(self, request):
        if request.user.is_authenticated:
            form = self.form_details(request)
            return render(request,"profile.html",{'form':form})
        else:
            return redirect('/login/')

    def form_details(self,request):
        userinfo = request.user
        profile = core_models.Profile.objects.filter(user_id=userinfo).last()
        form = my_forms.ProfileForm(initial={'firstname': userinfo.first_name,
                                                       'lastname': userinfo.last_name,
                                                       'email': userinfo.email,})
        if profile:
            mobileno = profile.mobile_number
            alternate_mobile = profile.alternate_mobile_number
            address = profile.address
            add_inst = core_models.Address.objects.filter(profile__id=profile.pk).last()
            if add_inst:
                addressline1 = add_inst.address_line1
                addressline2 = add_inst.address_line2
                city = add_inst.city
                state = add_inst.state
                zipcode = add_inst.zipcode
                country = add_inst.country
                form = my_forms.ProfileForm(initial={'firstname': userinfo.first_name,
                                                       'lastname': userinfo.last_name,
                                                       'email': userinfo.email,
                                                       'mobileno': mobileno,
                                                       'alternamemobile': alternate_mobile,
                                                       'addressline1': addressline1,
                                                       'addressline2': addressline2,
                                                       'city': city,
                                                       'state': state,
                                                       'zipcode': zipcode,
                                                       'country': country
                                                       })
        return form

class ProductView(ListView):
    template_name = "category.html"
    title = "Product"
    paginate_by = 10
    model = core_models.Product
    context_object_name = 'products'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,*kwargs)
        context['categories'] = core_models.Product.objects.values('category').order_by().annotate(Count('category'))
        context['order'] = {'get_cart_total': {'total_items': 0}}

        if self.request.user.is_authenticated:
            order_instance = core_models.Order.objects.filter(user=self.request.user, is_completed=False).last()
            if order_instance:
                context['order'] = order_instance
        return context


    def get_template_names(self):
        if self.request.user:
            template_name = self.template_name
        else:
            template_name = 'login.html'
        return[template_name]

class SearchView(ListView):
    model = core_models.Product
    template_name = 'search-' \
                    'product.html'
    context_object_name = 'Search'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        query = self.request.GET.get('search')
        print(query)
        products= core_models.Product.objects.all()

        context['products'] = [item for item in products if query in item.name.lower() or query in item.discription.lower() or query in item.category.lower()]
        print(products)
        return context


class CartView(ListView):
    template_name = "cart.html"
    model = core_models.Order
    title = 'Cart'


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        context['products'] = {}
        context['order'] = {'get_cart_total': {'total_items': 0, 'total': 0}}
        if self.request.user.is_authenticated:
            order_instance = core_models.Order.objects.filter(user = self.request.user,is_completed = False).last()
            if order_instance:
                orderitem_instance = core_models.OrderItem.objects.filter(order = order_instance)
                part = []
                part = order_instance.orderitem_set.all()
                context['products'] = part
                context['order'] = order_instance
            else:
                messages.success(self.request,'The cart is empty')
        return context





def addToBag(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    user = request.user
    product_instance = core_models.Product.objects.get(pk=product_id)

    order_instance,created = core_models.Order.objects.get_or_create(user = user,is_completed = False)

    orderitems_instance,created = core_models.OrderItem.objects.get_or_create(product = product_instance,order = order_instance)
    if action == 'add':
        orderitems_instance.quantity += 1
    elif action == 'remove':
        orderitems_instance.quantity -= 1
    orderitems_instance.save()

    if orderitems_instance.quantity <= 0:
        orderitems_instance.delete()
    order_quantity = order_instance.get_cart_total['total_items']
    return JsonResponse(order_quantity ,safe=False)



class Checkout(ListView):
    template_name = "checkout.html"

    model = core_models.Order
    title = 'Checkout'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, *kwargs)
        context['products'] = {}
        context['order'] = {'get_cart_total': {'total_items': 0, 'total': 0}}
        part = []

        if self.request.user.is_authenticated:
            order_instance = core_models.Order.objects.filter(user = self.request.user,is_completed = False).last()
            if order_instance:

                part = order_instance.orderitem_set.all()
                context['products'] = part
                context['order'] = order_instance
        return context


class PlaceOrder(TemplateView):
    template_name = 'index.html'
    title = 'Home'

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            order_instnce = core_models.Order.objects.filter(user = request.user,is_completed= False ).last()
            if order_instnce:
                orderitems = order_instnce.orderitem_set.all()
                for orderitem in orderitems:
                    if orderitem.quantity <= orderitem.product.quantity:
                        print('True')
                core_tasks.background_task.delay(request.user.id)
                print("********   thsi is after celery statement *********")
                messages.success(request,"Order Plased Successfully, Continue shopping")
                return redirect('/')
            else:
                return redirect('/category/')
        else:
            return redirect('/login/')



def SingleProductView(request, product_id):
    print(product_id)
    product_instance = core_models.Product.objects.filter(pk=product_id).last()
    order = {'get_cart_total': {'total_items': 0, 'total': 0}}
    context = {'product': product_instance, 'order': order}
    if request.user.is_authenticated:
        order_instnce = core_models.Order.objects.filter(user=request.user, is_completed=False).last()
        if order_instnce:
            order = order_instnce
            context = {'product': product_instance, 'order': order}

    return render(request,'single-product.html',context)
