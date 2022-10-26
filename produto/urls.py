from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),

    path('<slug:slug_da_categoria>/', views.lista_produtos, name='lista_produtos_por_categoria'),

    path('<int:id>/<slug:slug_do_produto>/', views.exibe_produto, name='exibe_produto'),

    path('tamanho/<slug:slug_do_tamanho>/', views.lista_produtos, name='lista_produtos_por_tamanho'),

    path('preco/<slug:slug_do_preco>/', views.lista_produtos, name='lista_produtos_por_preco'),

    path('edita_produto/<int:id>/', views.edita_produto, name='edita_produto'),

    path('cadastra_produto', views.cadastra_produto, name='cadastra'),

    path('pesquisa_produto', views.pesquisa_produto, name='pesquisa_produto'),

    path('remove_produto', views.remove_produto, name='remove_produto'),

    path('lista_produto_cadastrado', views.lista_produto_cadastrado, name='lista_produto_cadastrado'),

    path('exibe_produto_cadastrado/<int:id>/', views.exibe_produto_cadastrado, name='exibe_produto_cadastrado'),

    path('atualiza_produto', views.atualiza_produto, name='atualiza_produto'),

    path('adiciona_carrinho', views.adiciona_carrinho, name='adiciona_carrinho'),

    path('remove_carrinho', views.remove_carrinho, name='remove_carrinho'),
]
