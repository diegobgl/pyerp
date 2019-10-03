"""Formularios del modulo sale
"""
# Django Library
from django import forms
from django.forms.models import inlineformset_factory

# Thirdparty Library
from dal import autocomplete

# Localfolder Library
from .models import PySaleOrder, PySaleOrderDetail


# ========================================================================== #
class SaleOrderForm(forms.ModelForm):
    """Formulario para agregar y/o editar ordenes de compra
    """
    class Meta:
        model = PySaleOrder
        fields = [
            'partner_id',
            'description',
        ]
        labels = {
            'partner_id': 'Cliente',
            'description': 'Descripción',
        }
        widgets = {
            'partner_id': autocomplete.ModelSelect2(
                url='PyPartner:autocomplete',
                attrs={
                    'class': 'form-control',
                    'data-placeholder': 'Seleccione un cliente ...',
                    'style': 'width: 100%',
                },
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'data-placeholder': 'Descripción del presupuesto ...',
                    'style': 'width: 100%',
                },
            ),
        }


# ========================================================================== #
class SaleOrderDetailForm(forms.ModelForm):
    """Formulario para agregar y/o editar ordenes de compra
    """
    class Meta:
        model = PySaleOrderDetail
        exclude = ()
        fields = [
            # 'sale_order_id',
            'product',
            'description',
            'quantity',
            # 'measure_unit',
            # 'product_tax',
            'amount_untaxed',
            'discount',
            # 'amount_total',
        ]
        labels = {
            'product': 'Producto',
            'description': 'Descripción',
            'quantity': 'Cantidad',
            # 'measure_unit': 'Unidad',
            # 'product_tax': 'Impuesto',
            'amount_untaxed': 'Precio',
            'discount': 'Descuento',
            # 'amount_total': 'Sub total',
        }
        widgets = {
            'sale_order': forms.HiddenInput(),
            # 'product': autocomplete.ModelSelect2(
            #     url='PySaleOrder:product-autocomplete',
            #     attrs={
            #         'class': 'form-control',
            #         'data-placeholder': 'Seleccione un producto ...',
            #         'style': 'width: 100%',
            #     },
            # ),
            'product': forms.Select(
                attrs={
                    'class': 'form-control select2',
                    'data-placeholder': 'Seleccione un producto ...',
                    'style': 'width: 100%',
                },
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripción del producto ...',
                    'style': 'width: 100%',
                },
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'data-placeholder': 'Cantidad del producto ...',
                    'style': 'width: 100%',
                },
            ),
            # 'measure_unit': autocomplete.ModelSelect2(
            #     url='measure-unit-autocomplete',
            #     attrs={
            #         'class': 'form-control',
            #         'data-placeholder': 'Seleccione un unidad ...',
            #         'style': 'width: 100%',
            #     },
            # ),
            # 'product_tax': autocomplete.ModelSelect2(
            #     url='PyTax:autocomplete',
            #     attrs={
            #         'class': 'form-control',
            #         'data-placeholder': 'Seleccione un Impuesto ...',
            #         'style': 'width: 100%',
            #     },
            # ),
            'amount_untaxed': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'data-placeholder': 'Precio del producto ...',
                    'style': 'width: 100%',
                },
            ),
            'discount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'data-placeholder': 'Descuento ...',
                    'style': 'width: 100%',
                },
            ),
            # 'amount_total': NumberInput(
            #     attrs={
            #         'class': 'form-control',
            #         'data-placeholder': 'Sub total ...',
            #         'style': 'width: 100%',
            #     },
            # ),
        }


PRODUCT_FORMSET = inlineformset_factory(
    PySaleOrder, PySaleOrderDetail,
    # form=SaleOrderDetailForm,
    # fields=['product', 'description'],
    fields=[
        'sale_order_id',
        'product',
        'description',
        'quantity',
        # 'measure_unit',
        # 'product_tax',
        'amount_untaxed',
        'discount',
        # 'amount_total',
    ],
    widgets={
        'product': forms.Select(
            attrs={
                'class': 'form-control  form-control-sm custom-select custom-select-sm',
                'data-placeholder': 'Seleccione un producto ...',
                'style': 'width: 100%',
            },
        ),
        'description': forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Descripción del producto ...',
                'style': 'width: 100%',
            },
        ),
        'quantity': forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'data-placeholder': 'Cantidad del producto ...',
                'style': 'width: 100%',
            },
        ),
        'amount_untaxed': forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'data-placeholder': 'Precio del producto ...',
                'style': 'width: 100%',
            },
        ),
        'discount': forms.NumberInput(
            attrs={
                'class': 'form-control form-control-sm',
                'data-placeholder': 'Descuento ...',
                'style': 'width: 100%',
            },
        ),
    },
    extra=0,
    can_delete=True
)
