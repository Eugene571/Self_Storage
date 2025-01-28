from django.db import models
from django.utils.timezone import now, timedelta


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class CellTariff(models.Model):
    size = models.CharField(max_length=100)  # например: Малая ячейка (до 1 м3)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.size}, цена: {self.price_per_day}'


class Cell(models.Model):
    cell_size = models.ForeignKey(CellTariff,
                                  on_delete=models.CASCADE)
    is_occupied = models.BooleanField(null=True)
    start_storage = models.DateTimeField(null=True, blank=True)
    end_storage = models.DateTimeField(null=True, blank=True)
    address = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.id}, {self.cell_size.size}'

    def save(self, days=None, *args, **kwargs):  # метод для сохранения или обнуления сроков хранения
        if self.is_occupied:
            self.start_storage = now()
            if days is not None:
                self.end_storage = self.start_storage + timedelta(days=days)
        else:
            self.start_storage = None
            self.end_storage = None
        super().save(*args, **kwargs)


class Client(models.Model):
    tg_id = models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.client_name}, {self.tg_id}'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contacts = models.CharField(max_length=100)
    start_storage = models.DateTimeField()
    end_storage = models.DateTimeField()
    address = models.CharField(max_length=200)
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)  # на случай если в заказе может быть только одна ячейка
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, null=True)

    def __str__(self):
        return f'{self.client.client_name}, {self.contacts}'

    def save(self, *args, **kwargs):
        price_per_day = self.cell.cell_size.price_per_day
        days = (self.end_storage - self.start_storage).days
        self.total_price = days * price_per_day
        super().save(*args, **kwargs)


from django.db import models

# Create your models here.
