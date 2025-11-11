# products/views.py
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required, permission_required

from .models import Product, Category
from .forms import ProductSearchForm, ProductForm


@login_required
def product_list(request):
    form = ProductSearchForm(request.GET or None)
    qs = Product.objects.select_related('category').all()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(sku__icontains=q)
                | Q(category__name__icontains=q)
            )
    return render(request, 'products/product_list.html', {
        'form': form,
        'products': qs,
    })


@login_required
@require_http_methods(["GET"])
def product_detail_api(request, pk):
    p = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    data = {
        'id': p.id,
        'sku': p.sku,
        'name': p.name,
        'category': p.category_id,
        'category_name': p.category.name if p.category_id else '',
        'price': str(p.price),
        'stock': p.stock,
        'is_active': p.is_active,
        'image_url': p.image.url if p.image else '',
        'categories': [
            {'id': c.id, 'name': c.name}
            for c in Category.objects.all().order_by('name')
        ],
    }
    return JsonResponse({'ok': True, 'product': data})


@login_required
@permission_required('products.change_product', raise_exception=True)
@require_http_methods(["POST"])
def product_update_api(request, pk):
    p = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST, request.FILES, instance=p)
    if form.is_valid():
        p = form.save()
        return JsonResponse({
            'ok': True,
            'message': 'Товар сохранён',
            'image_url': (p.image.url if p.image else '')
        })
    return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["GET"])
def product_autocomplete(request):
    q = (request.GET.get('q') or '').strip()
    if not q:
        return JsonResponse({'results': []})
    hits = (Product.objects
            .filter(Q(name__icontains=q) | Q(sku__icontains=q))
            .order_by('name')[:10]
            .values('id', 'sku', 'name'))
    results = [{'id': h['id'], 'label': f"{h['name']} ({h['sku']})"} for h in hits]
    return JsonResponse({'results': results})


# --- НОВОЕ: удаление фото товара ---
@login_required
@permission_required('products.change_product', raise_exception=True)
@require_POST
def product_image_delete_api(request, pk):
    """
    Удаляет файл изображения из MEDIA и очищает поле image у продукта.
    Возвращает {'ok': True} и пустой image_url.
    """
    p = get_object_or_404(Product, pk=pk)
    if not p.image:
        return JsonResponse({'ok': True, 'image_url': ''})

    # удалить файл с диска, НЕ сохраняя модель автоматически
    try:
        p.image.delete(save=False)
    except Exception as exc:
        return JsonResponse({'ok': False, 'error': f'file_delete_failed: {exc}'}, status=500)

    # сбросить ссылку в БД
    p.image = None
    p.save(update_fields=['image'])
    return JsonResponse({'ok': True, 'image_url': ''})