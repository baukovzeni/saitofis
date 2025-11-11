from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
@login_required
def customer_list(request):
    return render(request,'customers/customer_list.html',{'customers': Customer.objects.all()})
@login_required
def customer_create(request):
    form=CustomerForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save(); return redirect('customers:list')
    return render(request,'customers/customer_form.html',{'form':form})
@login_required
def customer_update(request, pk):
    obj=get_object_or_404(Customer, pk=pk)
    form=CustomerForm(request.POST or None, instance=obj)
    if request.method=='POST' and form.is_valid():
        form.save(); return redirect('customers:list')
    return render(request,'customers/customer_form.html',{'form':form})
