from django.db import models


class Mark(models.Model):
    name = models.CharField(max_length=100)
    producer_country_name = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=100)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, db_index=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, db_index=True)
    price = models.IntegerField()
    json_data = models.JSONField(null=True, blank=True)
    is_visible = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name', 'mark', 'price']),
            models.Index(fields=['json_data'])
        ]