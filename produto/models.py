from django.db import models
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        db_table='categoria'

    def get_absolute_path(self):
        return reverse('produto:lista_produtos_por_categoria', args=[self.slug])

    def __str__(self):
        return self.nome

class Tamanho(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        db_table='tamanho'

    def get_absolute_path(self):
        return reverse('produto:lista_produtos_por_tamanho', args=[self.slug])

    def __str__(self):
        return self.nome

class Preco(models.Model):
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        db_table='preco'

    def get_absolute_path(self):
        return reverse('produto:lista_produtos_por_preco', args=[self.slug])

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.DO_NOTHING)
    tamanho = models.ForeignKey(Tamanho, related_name='tamanhos', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    imagem = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    class Meta:
        db_table = 'produto'

    def get_absolute_path(self):
        return reverse('produto:exibe_produto', args=[self.id, self.slug])

    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    produto = models.ForeignKey(Produto, related_name='produto', on_delete=models.DO_NOTHING)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(max_length=10)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table='carrinho'

    def get_absolute_path(self):
        return reverse('')

    def __str__(self):
        return self.preco