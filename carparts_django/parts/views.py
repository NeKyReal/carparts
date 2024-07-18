from django.db.models import Q
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Mark, Model, Part
import json


class MarkListView(View):
    def get(self, request):
        marks = Mark.objects.all()
        data = [{"id": mark.id, "name": mark.name, "producer_country_name": mark.producer_country_name} for mark in marks]
        return JsonResponse(data, safe=False)


class ModelListView(View):
    def get(self, request):
        models = Model.objects.all()
        data = [{"id": model.id, "name": model.name, "mark_id": model.mark.id} for model in models]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class PartSearchView(View):
    def post(self, request):
        body = json.loads(request.body)
        mark_list = body.get('mark_list')
        mark_name = body.get('mark_name')
        part_name = body.get('part_name')
        params = body.get('params', {})
        price_gte = body.get('price_gte')
        price_lte = body.get('price_lte')
        page = body.get('page', 1)

        parts_query = Part.objects.filter(is_visible=True)

        if mark_name:
            parts_query = parts_query.filter(mark__name__icontains=mark_name)
        if part_name:
            # icontains не работает с кириллицей, а в настройки бд нет доступа
            parts_query = parts_query.filter(Q(name__icontains=part_name) | Q(name__icontains=part_name.capitalize()))
        if 'color' in params:
            parts_query = parts_query.filter(json_data__color=params['color'])
        if 'is_new_part' in params:
            parts_query = parts_query.filter(json_data__is_new_part=params['is_new_part'])
        if price_gte is not None:
            parts_query = parts_query.filter(price__gte=price_gte)
        if price_lte is not None:
            parts_query = parts_query.filter(price__lte=price_lte)
        if mark_list:
            parts_query = parts_query.filter(mark_id__in=mark_list)

        paginator = Paginator(parts_query, 10)
        parts_page = paginator.get_page(page)
        response_data = []

        for part in parts_page:
            response_data.append({
                "mark": {
                    "id": part.mark.id,
                    "name": part.mark.name,
                    "producer_country_name": part.mark.producer_country_name
                },
                "model": {
                    "id": part.model.id,
                    "name": part.model.name
                },
                "name": part.name,
                "json_data": part.json_data,
                "price": part.price
            })

        summ = sum(part.price for part in parts_page)

        return JsonResponse({
            "response": response_data,
            "count": paginator.count,
            "summ": summ
        })
