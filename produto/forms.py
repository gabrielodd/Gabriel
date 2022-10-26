from decimal import Decimal
from django import forms
from django.core.validators import RegexValidator
from produto.models import Produto, Categoria, Tamanho, Preco, Carrinho
from projeto import settings
from datetime import datetime, timedelta

class PesquisaProdutoForm(forms.Form):
   class Meta:
      fields = ('busca_por')

   busca_por = forms.CharField(
      widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
      required=False)

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ('produto_id', 'categoria', 'nome', 'slug', 'descricao', 'imagem', 'preco', 'tamanho')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    # <input type="hidden" name="produto_id" id="id_produto_id" value="xxx">

    categoria = forms.ModelChoiceField(
        error_messages={'required': 'Campo obrigatório.', },
        queryset=Categoria.objects.all().order_by('nome'),
        empty_label='--- Selecione uma categoria ---',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        required=True)

    tamanho = forms.ModelChoiceField(
        error_messages={'required': 'Campo obrigatório.', },
        queryset=Tamanho.objects.all().order_by('nome'),
        empty_label='--- Selecione o tamanho ---',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        required=False)
    
    nome = forms.CharField(
        error_messages={'required': 'Campo obrigatório.',
                        'unique': 'Produto duplicado.'},
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=True)

    slug = forms.CharField(
        error_messages={'required': 'Campo obrigatório.',
                        'unique': 'Produto duplicado.'},
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=True)

    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'maxlength': '340'}),
        required=True)

    imagem = forms.CharField(
        error_messages={
                        'unique': 'Produto duplicado.'},
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '120'}),
        required=True)

    preco = forms.CharField(
        localize=True,
        error_messages={'required': 'Campo obrigatório.', },
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm',
                                      'maxlength': '10',
                                      'onkeypress': 'return (event.charCode >= 48 && event.charCode <= 57) || event.charCode == 44'}),
        required=True)

class RemoveProdutoForm(forms.Form):
    class Meta:
        fields = ('produto_id')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=True)

class AtualizaProdutoForm(forms.ModelForm):

    class Meta:
        model = Carrinho
        fields = ('quantidade',)

    quantidade = forms.CharField(
        error_messages={'required': 'Campo obrigatório.', },
        validators=[RegexValidator(regex='^[0-9]{1,5}$', message="Informe o valor no formato 99999.")],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm quantidade',
                                      'maxlength': '5',
                                      'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57'}),
        required=True)

class CarrinhoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ('produto_id',)

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=False)

class RemoveCarrinho(forms.Form):
    class Meta:
        fields = ('produto_id')

    produto_id = forms.CharField(widget=forms.HiddenInput(), required=True)

    # <input type="hidden" name="produto_id" id="id_produto_id" value="xxx">