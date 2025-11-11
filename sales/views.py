from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sale
from .forms import SaleForm, SaleItemFormSet
@login_required
def checkout(request):
    sale = Sale.objects.create(cashier=request.user) if request.method=='GET' else None
    if request.method=='GET':
        return render(request,'sales/checkout.html',{'form':SaleForm(instance=sale),'formset':SaleItemFormSet(instance=sale),'sale':sale})
    sale=get_object_or_404(Sale, pk=request.POST.get('sale_id'))
    form=SaleForm(request.POST, instance=sale); formset=SaleItemFormSet(request.POST, instance=sale)
    if form.is_valid() and formset.is_valid():
        form.save(); formset.save(); messages.success(request, f'Продажа #{sale.id} оформлена. Итог: {sale.total} ₽')
        return redirect('sales:detail', pk=sale.id)
    return render(request,'sales/checkout.html',{'form':form,'formset':formset,'sale':sale})
@login_required
def sale_detail(request, pk):
    sale=get_object_or_404(Sale, pk=pk)
    return render(request,'sales/sale_detail.html',{'sale':sale})
