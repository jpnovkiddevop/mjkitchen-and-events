from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Menu
from .forms import MenuForm
from django.contrib import messages

# Create your views here.

def menu(request):
    myMenu = Menu.objects.all()
    return render(request, 'menus/menu.html', {'menus': myMenu})

def details(request, id):
    myDetails = Menu.objects.get(id=id)
    print(myDetails.foodimage)
    return render(request, 'menus/details.html', {'menudetails': myDetails})

def deleteMenu(request, id):
    menu = Menu.objects.get(pk=id)
    menu.delete()
    return redirect('menus-menu')

def addMenu(request):
    submitted = False
    
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MenuForm(request.POST, request.FILES)
            print(request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'food added successfully!')
                return HttpResponseRedirect('/addMenu?submitted=True')

        else:
            form = MenuForm()
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'menus/addmenu.html', {'form': form, 'submitted': submitted})

def updateMenu(request, id):
    menu = Menu.objects.get(pk=id)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = MenuForm(request.POST, request.FILES, instance=menu)
            if form.is_valid():
                form.save()
                return redirect('menus-menu')
        else:
            form = MenuForm(instance=menu)
        return render(request, 'menus/updatemenu.html', {'menu':menu, 'form': form})

CART = []
TOTAL_PRICE = 0

def add_to_cart(request, id):
    global TOTAL_PRICE
    if request.method == 'POST':
        selected_menu_items = request.POST.getlist('menu_items')
        for menu_id in selected_menu_items:
            fooditem = Menu.objects.get(pk=menu_id)
            CART.append({'foodname': fooditem.foodname,
                        'price': int(fooditem.foodprice)})           
            TOTAL_PRICE += int(fooditem.foodprice)
            print(TOTAL_PRICE)
        # Redirect to the cart page, providing the first selected menu item ID if available
        first_menu_id = selected_menu_items[0] if selected_menu_items else 0
        return redirect('cart', id=first_menu_id)

    return render(request, 'menus/cart.html', {'cartitems': CART, 'total_price':TOTAL_PRICE})

def placeOrder(request):
    if len(CART) > 0:
        messages.success(request, 'order placed successfully')
        return redirect('menus-menu')
    else:
        messages.warning(request, 'no items in cart')
        return redirect('menus-menu')