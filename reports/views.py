# reports/views.py
from datetime import date
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import localdate
from django.views.decorators.http import require_POST

from sales.models import Sale


@login_required
def report_daily(request):
    """
    Ежедневный отчёт за локальную дату (Europe/Vaduz).
    Показываем список продаж, суммы и разрез по способам оплаты.
    """
    day = localdate()  # локальная дата с учётом TIME_ZONE/USE_TZ
    qs = (
        Sale.objects
        .filter(created_at__date=day)
        .select_related('cashier', 'customer')      # ВАЖНО: у Sale есть cashier, customer
        .prefetch_related('items__product')         # тянем позиции и товары
    )

    total = qs.aggregate(sum=Sum('total'))['sum'] or 0
    by_pm = (
        qs.values('payment_method')
        .annotate(sum=Sum('total'))
        .order_by()
    )

    return render(
        request,
        'reports/report_daily.html',
        {
            'date': day,
            'sales': qs,
            'total': total,
            'by_pm': by_pm,
        },
    )


@require_POST
@login_required
@permission_required('sales.delete_sale', raise_exception=True)
def sale_delete_bulk(request):
    """
    Массовое удаление продаж. Принимает JSON: {"ids": [1,2,3]}
    Возвращает JSON: {"ok": true, "deleted": N}
    """
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'bad json'}, status=400)

    ids = payload.get('ids', [])
    if not isinstance(ids, list):
        return JsonResponse({'ok': False, 'error': 'ids must be list'}, status=400)

    qs = Sale.objects.filter(pk__in=ids)
    deleted_count = qs.count()
    qs.delete()  # позиции удалятся каскадом (если FK on_delete=CASCADE)

    return JsonResponse({'ok': True, 'deleted': deleted_count})