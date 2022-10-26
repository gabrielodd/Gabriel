from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Produto, Tamanho, Preco, Carrinho
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Sum, F, FloatField
from datetime import datetime, timedelta
from produto.forms import ProdutoForm, RemoveProdutoForm, PesquisaProdutoForm, CarrinhoForm, AtualizaProdutoForm, RemoveCarrinho
from django.contrib import messages

def lista_produtos(request, slug_da_categoria=None, slug_do_tamanho=None, slug_do_preco=None):
   categoria = None
   tamanho = None
   preco = None
   categorias = Categoria.objects.all().order_by("nome")
   tamanhos = Tamanho.objects.all().order_by("id")
   precos = Preco.objects.all().order_by("id")
   produtos = Produto.objects.filter().order_by("nome")
   if slug_da_categoria:
      categoria = get_object_or_404(Categoria, slug=slug_da_categoria)
      produtos = produtos.filter(categoria_id=categoria).order_by("nome")

   if slug_do_tamanho: 
      tamanho = get_object_or_404(Tamanho, slug=slug_do_tamanho)
      produtos = produtos.filter(tamanho_id=tamanho).order_by("nome")

   if slug_do_preco:
      preco = get_object_or_404(Preco, slug=slug_do_preco)
      produtos = produtos.filter(preco_id=preco).order_by("nome")

   return render(request, 'produto/lista.html', {'categorias': categorias,
                                                 'tamanhos': tamanhos,
                                                 'precos' : precos,
                                                 'produtos': produtos,
                                                 'categoria': categoria,
                                                 'tamanho': tamanho,
                                                 'preco': preco
                                                 })

def exibe_produto(request, id, slug_do_produto):
   produto = get_object_or_404(Produto, id=id)

   if request.POST:
      if Carrinho.objects.filter(produto_id = id).exists():
         carrinho = get_object_or_404(Carrinho, produto_id = id)
         carrinho.quantidade = carrinho.quantidade + 1
         carrinho.total = carrinho.quantidade * carrinho.preco
         carrinho.save()
      else:
         carrinho = Carrinho()
         carrinho.preco = produto.preco
         carrinho.produto_id = produto.id
         carrinho.quantidade = 1
         carrinho.total = carrinho.preco
         carrinho.save()
   
   produtos = Produto.objects.all().order_by('nome')
   produtos_carrinho = Carrinho.objects.all().order_by('id')

   res = produtos_carrinho.aggregate(
      ptotal = Sum(F('quantidade') * F('preco'), output_field=FloatField()))
   
   resultado = produtos_carrinho.aggregate(
       total=Sum(F('quantidade') * F('preco'), output_field=FloatField()))
   
   if res['ptotal']:
      ptotal = '{0:.2f}'.format(res['ptotal'])
   else:
      ptotal = '0,00'

   if resultado['total']:
      total = '{0:.2f}'.format(resultado['total'])
   else:
      total = '0,00'

   lista_de_ids = []
   lista_de_forms = []
   for carrinho in produtos_carrinho:
      lista_de_ids.append(carrinho.id)
      lista_de_forms.append(AtualizaProdutoForm(initial={'quantidade': carrinho.quantidade}))

   return render(request, 'produto/exibe.html', {'produto': produto})

def cadastra_produto(request):
   if request.POST:
      produto_id = request.POST.get('produto_id')
      if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)
            produto_form = ProdutoForm(request.POST, instance=produto)
      else:
            produto_form = ProdutoForm(request.POST)

      if produto_form.is_valid():
         produto = produto_form.save(commit=False)
         if produto_id:
            messages.add_message(request, messages.INFO, 'Produto alterado com sucesso!')
         else:
            produto.user = request.user
            messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso!')
         produto.save()
         return redirect('produto:exibe_produto_cadastrado', id=produto.id)
      else:
            messages.add_message(request, messages.ERROR, 'Corrija o(s) erro(s) abaixo.')
   else:
      produto_form = ProdutoForm()

   return render(request, 'produto/cadastra.html', {
      'form': produto_form
   })

def exibe_produto_cadastrado(request, id):
    produto = get_object_or_404(Produto, pk=id)
    form_remove_produto = RemoveProdutoForm(initial={'produto_id': id})
    return render(request, 'produto/exibe_produto_cadastrado.html', {
       'produto': produto,
       'form_remove_produto': form_remove_produto
    })

def edita_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto_form = ProdutoForm(instance=produto)
    produto_form.fields['produto_id'].initial = id

    return render(request, 'produto/cadastra.html', {
       'form': produto_form
    })

def remove_produto(request):
   #form_remove_produto = RemoveProdutoForm(request.POST)
    #if form_remove_produto.is_valid:
   #produto_id = form_remove_produto.cleaned_data['produto_id']
   produto_id = request.POST.get('produto_id')
   produto = get_object_or_404(Produto, id=produto_id)
      #if produto.user == request.user:
   produto.delete()
   messages.add_message(request, messages.INFO, 'Produto removido com sucesso.')
      #else:
         #messages.add_message(request, messages.ERROR, 'Você não tem permissão para remover esse produto.')
   return render(request, 'produto/exibe_produto_cadastrado.html', {'produto': produto})

def pesquisa_produto(request):
   form = PesquisaProdutoForm()
   return render(request, 'produto/pesquisa_produto.html', {
      'form': form
   })

def lista_produto_cadastrado(request):
   form = PesquisaProdutoForm(request.GET)
   if (form.is_valid()):
      busca_por = form.cleaned_data['busca_por']
      lista_de_produtos = Produto.objects.filter(nome__icontains=busca_por).order_by('nome')

      resultado = lista_de_produtos.aggregate(
          total=Sum(F('preco'), output_field=FloatField()))
      
      if resultado['total']:
         total = '{0:.2f}'.format(resultado['total'])
      else:
         total = '0,00'

      paginator = Paginator(lista_de_produtos, 5)
      pagina = request.GET.get('pagina')
      produtos = paginator.get_page(pagina)

#      lista_de_forms = []
#      for produto in produtos:
#         lista_de_forms.append(RemoveProdutoForm(initial={'produto_id': produto.id}))

      lista_de_ids = []
      for produto in produtos:
         lista_de_ids.append(produto.id)

      return render(request, 'produto/pesquisa_produto.html', {
         'form': form,
#        'listas': zip(produtos, lista_de_forms),
         'produtos': produtos,
         'lista_de_ids': lista_de_ids,
         'total': total,
         'busca_por': busca_por
      })

   else:
      raise ValueError('Ocorreu um erro inesperado ao tentar pesquisar um produto.')


def adiciona_carrinho(request):
   produtos = Produto.objects.all().order_by('nome')
   produtos_carrinho = Carrinho.objects.all().order_by('id')

   resultado = produtos_carrinho.aggregate(
       total=Sum(F('quantidade') * F('preco'), output_field=FloatField()))
   
   if resultado['total']:
      total = '{0:.2f}'.format(resultado['total'])
   else:
      total = '0,00'
   
   lista_de_ids = []
   lista_de_forms = []
   lista_de_ptotal = []
   for carrinho in produtos_carrinho:
      lista_de_ids.append(carrinho.id)
      lista_de_forms.append(AtualizaProdutoForm(initial={'quantidade': carrinho.quantidade}))

   return render(request, 'produto/carrinho.html', {
      'produtos': produtos,
      'listas': zip(produtos_carrinho, lista_de_forms),
      'lista_de_ids': lista_de_ids,
      'total': total
   })

def remove_carrinho(request):
   produto_id = request.POST.get('produto_id')
   carrinho = get_object_or_404(Carrinho, id=produto_id)
   carrinho.delete()

   resultado = Carrinho.objects.all().aggregate(
       total=Sum(F('quantidade') * F('preco'), output_field=FloatField()))

   if resultado['total']:
      total = '{0:.2f}'.format(resultado['total'])
   else:
      total = '0,00'

   #res = produtos_carrinho.aggregate(
   #   ptotal = Sum(F('quantidade') * F('preco'), output_field=FloatField()))

   #if res['ptotal']:
   #   ptotal = '{0:.2f}'.format(res['ptotal'])
   #else:
   #   ptotal = '0,00'

   return render(request, 'produto/valor_do_estoque.html', 
   {'total': total

   })


def atualiza_produto(request):
   carrinho = get_object_or_404(Carrinho, pk=request.POST.get('produto_id'))
   form = AtualizaProdutoForm(request.POST, instance=carrinho)
   if form.is_valid:
      carrinho.total = carrinho.quantidade * carrinho.preco
      form.save()

      resultado = Carrinho.objects.all().aggregate(
         total=Sum(F('quantidade') * F('preco'), output_field=FloatField()))
         
      if resultado['total']:
         total = '{0:.2f}'.format(resultado['total'])
      else:
         total = '0,00'

      return render(request, 'produto/valor_do_estoque.html', 
      {'total': total
      })

   else:
      raise ValueError('Ocorreu um erro inesperado ao tentar alterar um produto.')   