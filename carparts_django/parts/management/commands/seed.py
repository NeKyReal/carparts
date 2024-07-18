from django.core.management.base import BaseCommand
from parts.models import Mark, Model, Part
from random import randint, choice, random
import json


class Command(BaseCommand):
    help = 'Заполнить базу данных начальными значениями'

    def handle(self, *args, **kwargs):
        marks = [
            {"name": "Honda", "producer_country_name": "Япония"},
            {"name": "Toyota", "producer_country_name": "Япония"},
            {"name": "Ford", "producer_country_name": "США"},
            {"name": "BMW", "producer_country_name": "Германия"},
            {"name": "Mercedes", "producer_country_name": "Германия"},
        ]

        models = [
            {"name": "Accord", "mark_id": 1},
            {"name": "Civic", "mark_id": 1},
            {"name": "Corolla", "mark_id": 2},
            {"name": "Mustang", "mark_id": 3},
            {"name": "X5", "mark_id": 4},
        ]

        parts_names = ["Бампер", "Капот", "Дверь", "Двигатель", "Колесо"]
        colors = ["красный", "черный", "белый", "синий", "зеленый"]

        for mark in marks:
            Mark.objects.create(**mark)

        for model in models:
            Model.objects.create(**model)

        for _ in range(10000):
            part = {
                "name": choice(parts_names),
                "mark_id": randint(1, 5),
                "model_id": randint(1, 5),
                "price": randint(1000, 10000),
                "json_data": {
                    # шанс 70% на добавление поля
                    "color": choice(colors) if random() > 0.7 else None,
                    "is_new_part": choice([True, False]) if random() > 0.7 else None,
                    "count": randint(1, 10) if random() > 0.5 else None
                },
                "is_visible": choice([True, False])
            }
            Part.objects.create(**part)

        self.stdout.write(self.style.SUCCESS('База данных заполнена'))
