from django.db import models
from django.utils import timezone

# Create your models here.
'''CONTATOS
id: INT (automático)
nome: STR * (obrigatório)
sobrenome: STR (opcional)
telefone: STR * (obrigatório)
email: STR (opcional)
data_criacao: DATETIME (automático)
descricao: texto
categoria: CATEGORIA (outro model)

 CATEGORIA
 id: INT
 nome: STR * (obrigatório)
'''


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65, blank=True)
    cell_phone = models.CharField(max_length=65)
    email = models.CharField(max_length=65, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=165)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    is_publish = models.BooleanField(default=True)
    profile_picture = models.ImageField(
        upload_to='contacts/profile_pictures/%Y/%m/%d/', blank=True)

    def __str__(self) -> str:
        return self.first_name
