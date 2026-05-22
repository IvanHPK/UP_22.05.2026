from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Restaurant, Dish, Client, Courier, Order, OrderItem


def index(request):
    dishes = Dish.objects.all()
    client = Client.objects.order_by('-id').first()

    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        delivery_address = request.POST.get('delivery_address')

        dish = get_object_or_404(Dish, id=dish_id)

        client = Client.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            delivery_address=delivery_address
        )

        order = Order.objects.create(
            client=client,
            courier=None,
            total_price=dish.price,
            status='Новый'
        )

        OrderItem.objects.create(
            dish=dish,
            order=order,
            quantity=1
        )

        return redirect('index')

    return render(request, 'index.html', {
        'dishes': dishes,
        'client': client
    })


def account(request):
    client = Client.objects.order_by('-id').first()

    if client is None:
        client = Client.objects.create(
            full_name='Иван Петров',
            email='ivan@mail.ru',
            phone='+7 999 123-45-67',
            delivery_address='г. Абакан'
        )

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save':
            client.full_name = request.POST.get('full_name')
            client.email = request.POST.get('email')
            client.phone = request.POST.get('phone')
            client.delivery_address = request.POST.get('delivery_address')
            client.save()

        elif action == 'delete':
            client.delete()
            return redirect('index')

        return redirect('account')

    return render(request, 'account.html', {
        'client': client
    })


def admin_panel(request):
    dishes = Dish.objects.all().order_by('id')
    orders = Order.objects.select_related('client', 'courier').all().order_by('-id')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete_dish':
            dish_id = request.POST.get('dish_id')
            Dish.objects.filter(id=dish_id).delete()
            return redirect('admin_panel')

        if action == 'delete_order':
            order_id = request.POST.get('order_id')
            Order.objects.filter(id=order_id).delete()
            return redirect('admin_panel')

        if action == 'update_dish':
            dish = get_object_or_404(Dish, id=request.POST.get('dish_id'))
            field = request.POST.get('field')
            value = request.POST.get('value', '').strip()

            if field == 'name':
                dish.name = value
            elif field == 'description':
                dish.description = value
            elif field == 'price':
                dish.price = value.replace('₽', '').replace(',', '.').strip()
            elif field == 'status':
                dish.status = value

            dish.save()
            return JsonResponse({'ok': True})

        if action == 'update_order':
            order = get_object_or_404(Order, id=request.POST.get('order_id'))
            field = request.POST.get('field')
            value = request.POST.get('value', '').strip()

            if field == 'client':
                order.client.full_name = value
                order.client.save()
            elif field == 'total_price':
                order.total_price = value.replace('₽', '').replace(',', '.').strip()
                order.save()
            elif field == 'status':
                order.status = value
                order.save()

            return JsonResponse({'ok': True})

    return render(request, 'admin_panel.html', {
        'dishes': dishes,
        'orders': orders
    })

def employee_panel(request):
    orders = Order.objects.select_related('client', 'courier').all().order_by('-id')
    couriers = Courier.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')

        order = get_object_or_404(Order, id=order_id)

        if action == 'check':
            order.status = 'Проверен'

        elif action == 'form':
            order.status = 'Сформирован'

        elif action == 'assign':
            courier_id = request.POST.get('courier_id')

            if courier_id:
                courier = get_object_or_404(Courier, id=courier_id)
                order.courier = courier
                order.status = 'Передан курьеру'

        elif action == 'change_status':
            new_status = request.POST.get('status')

            if new_status:
                order.status = new_status

        order.save()
        return redirect('employee_panel')

    return render(request, 'employee_panel.html', {
        'orders': orders,
        'couriers': couriers
    })


def courier_panel(request):
    selected_order = None
    selected_id = request.GET.get('selected')

    if selected_id:
        selected_order = Order.objects.select_related('client', 'courier').filter(id=selected_id).first()

    orders = Order.objects.select_related('client', 'courier').filter(
        courier__isnull=False
    ).exclude(
        status='Доставлен'
    ).order_by('-id')

    if selected_order:
        orders = orders.exclude(id=selected_order.id)

    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')

        order = get_object_or_404(Order, id=order_id)

        if action == 'select':
            order.status = 'В доставке'
            order.save()
            return redirect(f'/courier-panel/?selected={order.id}')

        elif action == 'confirm':
            order.status = 'Доставлен'
            order.save()
            return redirect('courier_panel')

    return render(request, 'courier_panel.html', {
        'orders': orders,
        'selected_order': selected_order
    })


def clients_data(request):
    clients = Client.objects.all().order_by('id')

    if request.method == 'POST':
        action = request.POST.get('action')
        client_id = request.POST.get('client_id')

        if action == 'update':
            client = get_object_or_404(Client, id=client_id)
            client.full_name = request.POST.get('full_name')
            client.email = request.POST.get('email')
            client.phone = request.POST.get('phone')
            client.delivery_address = request.POST.get('delivery_address')
            client.save()

        elif action == 'delete':
            Client.objects.filter(id=client_id).delete()

        return redirect('clients_data')

    return render(request, 'clients_data.html', {
        'clients': clients
    })


def couriers_data(request):
    couriers = Courier.objects.all().order_by('id')

    if request.method == 'POST':
        action = request.POST.get('action')
        courier_id = request.POST.get('courier_id')

        if action == 'update':
            courier = get_object_or_404(Courier, id=courier_id)
            courier.full_name = request.POST.get('full_name')
            courier.phone = request.POST.get('phone')
            courier.transport = request.POST.get('transport')
            courier.status = request.POST.get('status')
            courier.save()

        elif action == 'delete':
            Courier.objects.filter(id=courier_id).delete()

        return redirect('couriers_data')

    return render(request, 'couriers_data.html', {
        'couriers': couriers
    })


def restaurants_data(request):
    restaurants = Restaurant.objects.all().order_by('id')

    if request.method == 'POST':
        action = request.POST.get('action')
        restaurant_id = request.POST.get('restaurant_id')

        if action == 'update':
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            restaurant.name = request.POST.get('name')
            restaurant.address = request.POST.get('address')
            restaurant.phone = request.POST.get('phone')
            restaurant.rating = request.POST.get('rating')
            restaurant.save()

        elif action == 'delete':
            Restaurant.objects.filter(id=restaurant_id).delete()

        return redirect('restaurants_data')

    return render(request, 'restaurants_data.html', {
        'restaurants': restaurants
    })


def employees_data(request):
    if not User.objects.exists():
        User.objects.create_user(
            username='Иванов Иван',
            email='ivanov@mail.ru',
            password='12345'
        )

        User.objects.create_user(
            username='Петров Пётр',
            email='petrov@mail.ru',
            password='12345'
        )

        User.objects.create_user(
            username='Сидоров Алексей',
            email='sidorov@mail.ru',
            password='12345'
        )

    employees = User.objects.all().order_by('id')

    if request.method == 'POST':
        action = request.POST.get('action')
        employee_id = request.POST.get('employee_id')

        if action == 'update':
            employee = get_object_or_404(User, id=employee_id)
            employee.username = request.POST.get('username')
            employee.email = request.POST.get('email')
            employee.save()

        elif action == 'delete':
            User.objects.filter(id=employee_id).delete()

        return redirect('employees_data')

    return render(request, 'employees_data.html', {
        'employees': employees
    })
def menu_edit(request):
    dishes = Dish.objects.all().order_by('id')

    if request.method == 'POST':
        action = request.POST.get('action')
        dish_id = request.POST.get('dish_id')

        dish = get_object_or_404(Dish, id=dish_id)

        if action == 'update':
            dish.name = request.POST.get('name')
            dish.description = request.POST.get('description')
            dish.price = request.POST.get('price')
            dish.status = request.POST.get('status')
            dish.save()

        elif action == 'delete':
            dish.delete()

        return redirect('menu_edit')

    return render(request, 'menu_edit.html', {
        'dishes': dishes
    })
def orders_edit(request):
    orders = Order.objects.select_related('client', 'courier').all().order_by('-id')

    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')

        order = get_object_or_404(Order, id=order_id)

        if action == 'update':
            order.client.full_name = request.POST.get('client_name')
            order.client.save()

            order.total_price = request.POST.get('total_price')
            order.status = request.POST.get('status')
            order.save()

        elif action == 'delete':
            order.delete()

        return redirect('orders_edit')

    return render(request, 'orders_edit.html', {
        'orders': orders
    })