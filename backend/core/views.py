import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import POSProduct, Sale, POSCustomer


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['posproduct_count'] = POSProduct.objects.count()
    ctx['posproduct_active'] = POSProduct.objects.filter(status='active').count()
    ctx['posproduct_inactive'] = POSProduct.objects.filter(status='inactive').count()
    ctx['posproduct_total_price'] = POSProduct.objects.aggregate(t=Sum('price'))['t'] or 0
    ctx['sale_count'] = Sale.objects.count()
    ctx['sale_cash'] = Sale.objects.filter(payment_method='cash').count()
    ctx['sale_card'] = Sale.objects.filter(payment_method='card').count()
    ctx['sale_upi'] = Sale.objects.filter(payment_method='upi').count()
    ctx['sale_total_total'] = Sale.objects.aggregate(t=Sum('total'))['t'] or 0
    ctx['poscustomer_count'] = POSCustomer.objects.count()
    ctx['poscustomer_bronze'] = POSCustomer.objects.filter(tier='bronze').count()
    ctx['poscustomer_silver'] = POSCustomer.objects.filter(tier='silver').count()
    ctx['poscustomer_gold'] = POSCustomer.objects.filter(tier='gold').count()
    ctx['poscustomer_total_total_purchases'] = POSCustomer.objects.aggregate(t=Sum('total_purchases'))['t'] or 0
    ctx['recent'] = POSProduct.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def posproduct_list(request):
    qs = POSProduct.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'posproduct_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def posproduct_create(request):
    if request.method == 'POST':
        obj = POSProduct()
        obj.name = request.POST.get('name', '')
        obj.sku = request.POST.get('sku', '')
        obj.category = request.POST.get('category', '')
        obj.price = request.POST.get('price') or 0
        obj.cost = request.POST.get('cost') or 0
        obj.quantity = request.POST.get('quantity') or 0
        obj.barcode = request.POST.get('barcode', '')
        obj.status = request.POST.get('status', '')
        obj.tax_rate = request.POST.get('tax_rate') or 0
        obj.save()
        return redirect('/posproducts/')
    return render(request, 'posproduct_form.html', {'editing': False})


@login_required
def posproduct_edit(request, pk):
    obj = get_object_or_404(POSProduct, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.sku = request.POST.get('sku', '')
        obj.category = request.POST.get('category', '')
        obj.price = request.POST.get('price') or 0
        obj.cost = request.POST.get('cost') or 0
        obj.quantity = request.POST.get('quantity') or 0
        obj.barcode = request.POST.get('barcode', '')
        obj.status = request.POST.get('status', '')
        obj.tax_rate = request.POST.get('tax_rate') or 0
        obj.save()
        return redirect('/posproducts/')
    return render(request, 'posproduct_form.html', {'record': obj, 'editing': True})


@login_required
def posproduct_delete(request, pk):
    obj = get_object_or_404(POSProduct, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/posproducts/')


@login_required
def sale_list(request):
    qs = Sale.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(receipt_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(payment_method=status_filter)
    return render(request, 'sale_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def sale_create(request):
    if request.method == 'POST':
        obj = Sale()
        obj.receipt_number = request.POST.get('receipt_number', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.total = request.POST.get('total') or 0
        obj.discount = request.POST.get('discount') or 0
        obj.tax = request.POST.get('tax') or 0
        obj.payment_method = request.POST.get('payment_method', '')
        obj.date = request.POST.get('date') or None
        obj.cashier = request.POST.get('cashier', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.save()
        return redirect('/sales/')
    return render(request, 'sale_form.html', {'editing': False})


@login_required
def sale_edit(request, pk):
    obj = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        obj.receipt_number = request.POST.get('receipt_number', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.total = request.POST.get('total') or 0
        obj.discount = request.POST.get('discount') or 0
        obj.tax = request.POST.get('tax') or 0
        obj.payment_method = request.POST.get('payment_method', '')
        obj.date = request.POST.get('date') or None
        obj.cashier = request.POST.get('cashier', '')
        obj.items_count = request.POST.get('items_count') or 0
        obj.save()
        return redirect('/sales/')
    return render(request, 'sale_form.html', {'record': obj, 'editing': True})


@login_required
def sale_delete(request, pk):
    obj = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/sales/')


@login_required
def poscustomer_list(request):
    qs = POSCustomer.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(tier=status_filter)
    return render(request, 'poscustomer_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def poscustomer_create(request):
    if request.method == 'POST':
        obj = POSCustomer()
        obj.name = request.POST.get('name', '')
        obj.phone = request.POST.get('phone', '')
        obj.email = request.POST.get('email', '')
        obj.loyalty_points = request.POST.get('loyalty_points') or 0
        obj.total_purchases = request.POST.get('total_purchases') or 0
        obj.visit_count = request.POST.get('visit_count') or 0
        obj.last_visit = request.POST.get('last_visit') or None
        obj.tier = request.POST.get('tier', '')
        obj.save()
        return redirect('/poscustomers/')
    return render(request, 'poscustomer_form.html', {'editing': False})


@login_required
def poscustomer_edit(request, pk):
    obj = get_object_or_404(POSCustomer, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.phone = request.POST.get('phone', '')
        obj.email = request.POST.get('email', '')
        obj.loyalty_points = request.POST.get('loyalty_points') or 0
        obj.total_purchases = request.POST.get('total_purchases') or 0
        obj.visit_count = request.POST.get('visit_count') or 0
        obj.last_visit = request.POST.get('last_visit') or None
        obj.tier = request.POST.get('tier', '')
        obj.save()
        return redirect('/poscustomers/')
    return render(request, 'poscustomer_form.html', {'record': obj, 'editing': True})


@login_required
def poscustomer_delete(request, pk):
    obj = get_object_or_404(POSCustomer, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/poscustomers/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['posproduct_count'] = POSProduct.objects.count()
    data['sale_count'] = Sale.objects.count()
    data['poscustomer_count'] = POSCustomer.objects.count()
    return JsonResponse(data)
