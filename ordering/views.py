
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime

# Create your views here.
from django.template.loader import render_to_string

from accounts.models import History, PersonalHistory
from ordering import forms
from ordering.forms import EditOrderModelForm, IngredientModelForm, MenuModelForm
from ordering.models import Shop, OrderItem, Order, Menu, ShopQueue, Ingredient


def home(request):
    if request.user.is_authenticated:
        user_type = User.objects.get(id=request.user.id).userprofile.type
        if user_type == "01":
            return redirect('show_shop')
        else:
            return shop_order(request)
    else:
        return redirect('show_shop')


def select_shop(request):
    shop_list = Shop.objects.all()
    context = {
        'shop_list': shop_list
    }
    return render(request, template_name='ordering/select_shop.html', context=context)


def select_menu(request, shop_id):
    shop = Shop.objects.get(id=shop_id)
    menu_list = Menu.objects.filter(menu_of_id=shop_id).filter(is_daily_menu=True)
    ingredient = Ingredient.objects.filter(ingredient_of=shop)
    context = {
        'shop': shop,
        'menu_list': menu_list,
        'ingredient': ingredient
    }
    return render(request, template_name="ordering/select_menu.html", context=context)


@login_required()
def edit_order(request, menu_of, menu_id):
    ingredient = Ingredient.objects.filter(ingredient_of=menu_of)
    shop = Shop.objects.get(id=menu_of)
    menu = Menu.objects.get(id=menu_id)
    user = User.objects.get(id=request.user.id)
    shop_queue = shop.shopqueue
    if request.method == 'POST':
        form = forms.EditOrderModelForm(request.POST)
        if form.is_valid():
            order_datetime = datetime.datetime.now()
            add_queue(shop)
            if menu.menu_type == "01":
                if request.POST.get('food-size') == "01":
                    price = menu.normal_price
                elif request.POST.get('food-size') == "02":
                    price = menu.special_price
            elif menu.menu_type == "02":
                if request.POST.get('drink-size') == "03":
                    price = menu.hot_price
                elif request.POST.get('drink-size') == "04":
                    price = menu.cold_price
                elif request.POST.get('drink-size') == "05":
                    price = menu.frappe_price
            OrderItem.objects.create(
                menu=menu,
                queue=shop_queue,
                order=user.userprofile.order,
                order_datetime=order_datetime,
                this_queue=shop_queue.current_queue,
                special_requirement=form.cleaned_data.get('special_requirement'),
                price=price
            )
            order_item = OrderItem.objects.get(menu=menu, queue=shop_queue, order=user.userprofile.order, order_datetime=order_datetime)
            order_item.wait = order_item.this_queue - shop_queue.last_queue
            order_item.save()
            mail_subject = 'New order'
            message = render_to_string('ordering/shop_notify_email.html', {
                'user': user,
                'shop': shop,
                'menu': order_item.menu,
                'price': order_item.price,
                'orderDT': order_item.order_datetime,
                'special_requirement': order_item.special_requirement
            })
            to_email = shop.shop_host.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('order_status')
    else:
        form = EditOrderModelForm()
    context = {
        'shop': shop,
        'menu': menu,
        'forms': form,
        'ingredient': ingredient
    }
    return render(request, 'ordering/edit_order.html', context=context)


def add_queue(shop):
    shop_queue = shop.shopqueue
    shop_queue.current_queue += 1
    shop_queue.queue = shop_queue.current_queue - shop_queue.last_queue
    shop_queue.save()


def remove_queue(shop, rem_queue):
    shop_queue = shop.shopqueue
    OrderItem.objects.filter(queue=shop_queue, this_queue=rem_queue).delete()
    for i in OrderItem.objects.filter(queue=shop_queue):
        if i.this_queue > rem_queue:
            i.this_queue -= 1
            i.save()
    shop_queue.current_queue -= 1
    shop_queue.queue = shop_queue.current_queue - shop_queue.last_queue
    shop_queue.save()
    update_wait(shop)


def update_wait(shop):
    shop_queue = shop.shopqueue
    order_in_shop = OrderItem.objects.filter(queue=shop_queue)
    for i in order_in_shop:
        i.wait = i.this_queue - shop_queue.last_queue
        i.save()
    shop_queue.save()


@login_required()
def show_order_status(request):
    user = User.objects.get(id=request.user.id).userprofile
    order = user.order
    order_item = OrderItem.objects.filter(order=order)
    if (order_item.aggregate(Sum('price')))['price__sum']:
        order.total_price = (order_item.aggregate(Sum('price')))['price__sum']
    else:
        order.total_price = 0
    order.save()
    context = {
        'order': order,
        'order_item': order_item,
    }
    return render(request, 'ordering/order_status.html', context=context)


@login_required()
def update_order(request, queue):
    order_item = OrderItem.objects.get(this_queue=queue)
    shop = order_item.queue.shop
    menu = order_item.menu
    ingredient = Ingredient.objects.filter(ingredient_of=shop)
    if request.method == 'POST':
        form = forms.EditOrderModelForm(request.POST, instance=order_item)
        if form.is_valid():
            if menu.menu_type == "01":
                if request.POST.get('food-size') == "01":
                    price = menu.normal_price
                elif request.POST.get('food-size') == "02":
                    price = menu.special_price
            elif menu.menu_type == "02":
                if request.POST.get('drink-size') == "03":
                    price = menu.hot_price
                elif request.POST.get('drink-size') == "04":
                    price = menu.cold_price
                elif request.POST.get('drink-size') == "05":
                    price = menu.frappe_price
            order_item.special_requirement = form.cleaned_data.get('special_requirement')
            order_item.price = price
            order_item.save()
            form.save()
            return redirect('order_status')
    else:
        form = EditOrderModelForm(instance=order_item)
    context = {
        'shop': shop,
        'menu': menu,
        'forms': form,
        'ingredient': ingredient,
        'order_item': order_item,
    }
    return render(request, 'ordering/update_order.html', context=context)

@login_required()
def show_order_history(request):
    user = User.objects.get(id=request.user.id)
    detail = PersonalHistory.objects.filter(history=History.objects.get(user=user.userprofile))
    context = {
        'history': History.objects.get(user=user.userprofile),
        'detail': detail
    }
    return render(request, 'ordering/show_order_history.html', context=context)


@login_required()
def remove_order(request, shop, menu_id, queue):
    shop = Shop.objects.get(id=shop)
    menu = Menu.objects.get(id=menu_id)
    user = User.objects.get(id=request.user.id)
    shop_queue = shop.shopqueue
    remove_queue(shop, queue)
    return redirect('order_status')


@login_required()
def shop_order(request):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    shop_queue = shop.shopqueue
    order_item = OrderItem.objects.filter(queue=shop_queue)
    context = {
        'shop': shop,
        'shop_queue': shop_queue,
        'order_item': order_item
    }
    return render(request, 'ordering/shop_order.html',  context=context)


@login_required()
def start_cook(request, shop, order_item_id, queue):
    shop = Shop.objects.get(id=shop)
    order_item = OrderItem.objects.get(id=order_item_id)
    user = order_item.order.user
    history = History.objects.get(user=user)
    PersonalHistory.objects.create(
        history=History.objects.get(user=user),
        menu=order_item.menu,
        shop=shop,
        order_datetime=order_item.order_datetime,
        price=order_item.price,
    )
    PersonalHistory.objects.all().last().save()
    history.total_price = (PersonalHistory.objects.filter(history=history).aggregate(Sum('price')))['price__sum']
    history.save()
    mail_subject = 'Get your food.'
    message = render_to_string('ordering/food_notify_email.html', {
        'user': user,
        'shop': shop,
        'menu': order_item.menu,
        'price': order_item.price,
        'orderDT': order_item.order_datetime
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    remove_queue(shop, queue)
    return redirect('home')


@login_required()
def create_ingredient(request):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    if request.method == 'POST':
        form = IngredientModelForm(request.POST)
        if form.is_valid():
            Ingredient.objects.create(
                ingredient_of=shop,
                is_empty=form.cleaned_data.get('is_empty'),
                ingredient_name=form.cleaned_data.get('ingredient_name')
            )
            Ingredient.objects.all().last().save()
            return redirect('show_ingredient')
    else:
        form = IngredientModelForm()
    context = {
        'form': form
    }
    return render(request, 'ordering/create_ingredient.html', context=context)


@login_required()
def create_menu(request):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    if request.method == 'POST':
        form = MenuModelForm(request.POST, request.FILES)
        if form.is_valid():
            value = form.save(commit=False)
            value.menu_of = shop
            value.save()
            form.save()
            return redirect('show_menu')
    else:
        form = MenuModelForm()
    context = {
        'form': form
    }
    return render(request, 'ordering/create_menu.html', context=context)


@login_required()
def edit_status(request, status):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    if status == 1:
        shop.status = '01'
    elif status == 2:
        shop.status = '02'
    else:
        shop.status = '03'
    shop.save()
    return redirect('home')


@login_required()
def show_ingredient(request):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    ingredient = Ingredient.objects.filter(ingredient_of=shop)
    context = {
        'ingredient': ingredient
    }
    return render(request, 'ordering/show_ingredient.html', context)


@login_required()
def show_menu(request):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    menu = Menu.objects.filter(menu_of=shop)
    context = {
        'menu': menu
    }
    return render(request, 'ordering/show_menu.html', context)


@login_required()
def update_ingredient(request, ingre_id):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    ingredient = Ingredient.objects.get(pk=ingre_id)
    if request.method == 'POST':
        form = IngredientModelForm(request.POST, instance=ingredient)
        if form.is_valid():
            value = form.save(commit=False)
            value.ingredient_of = shop
            value.save()
            form.save()
            return redirect('show_ingredient')
    else:
        form = IngredientModelForm(instance=ingredient)
    context = {
        'form': form,
        'ingredient': ingredient
    }
    return render(request, 'ordering/update_ingredient.html', context=context)


@login_required()
def update_menu(request, menu_id):
    shop = User.objects.get(id=request.user.id).userprofile.shop
    menu = Menu.objects.get(pk=menu_id)
    if request.method == 'POST':
        form = MenuModelForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            value = form.save(commit=False)
            value.menu_of = shop
            value.save()
            form.save()
            return redirect('show_menu')
    else:
        form = MenuModelForm(instance=menu)
    context = {
        'form': form,
        'menu': menu
    }
    return render(request, 'ordering/update_menu.html', context=context)


@login_required()
def remove_ingredient(request, ingre_id):
    Ingredient.objects.get(id=ingre_id).delete()
    return redirect('show_ingredient')


@login_required()
def remove_menu(request, menu_id):
    Menu.objects.get(id=menu_id).delete()
    return redirect('show_menu')
