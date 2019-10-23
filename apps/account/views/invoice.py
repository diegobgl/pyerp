"""Sub Vistas del módulo
"""
# Standard Library
import logging

# Django Library
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DeleteView

# Thirdparty Library
from apps.base.models import PyProduct, PyTax
from apps.base.views.web_father import (
    FatherCreateView, FatherDetailView, FatherListView, FatherUpdateView)

# Localfolder Library
from ..forms import PRODUCT_FORMSET, InvoiceForm
from ..models import PyInvoice, PyInvoiceDetail

LOGGER = logging.getLogger(__name__)

OBJECT_LIST_FIELDS = [
    {'string': _('Name'), 'field': 'name'},
    {'string': _('Client'), 'field': 'partner_id'},
    {'string': ('Date'), 'field': 'date_invoice'},
    {'string': ('Net Amount'), 'field': 'amount_untaxed', 'align': 'text-right', 'humanize': True},
    {'string': ('Total'), 'field': 'amount_total', 'align': 'text-right', 'humanize': True},
]

OBJECT_TOTAL_FIELDS = [
    {'string': _('Net Amount or Affection:'), 'field': 'amount_untaxed'},
    {'string': _('Exempt Amount:'), 'field': 'amount_exempt'},
    {'string': _('IVA:'), 'field': 'amount_tax_iva'},
    {'string': _('Other taxes:'), 'field': 'amount_tax_other'},
    {'string': _('Total taxes:'), 'field': 'amount_tax_total'},
    {'string': _('Total:'), 'field': 'amount_total'},
]

OBJECT_DETAIL_FIELDS = [
    {'string': _('Name'), 'field': 'name'},
    {'string': ('Date'), 'field': 'date_invoice'},
    {'string': _('Client'), 'field': 'partner_id'},
]

DETAIL_OBJECT_LIST_FIELDS = [
    {'string': _('Product'), 'field': 'product_id'},
    {'string': _('Description'), 'field': 'description'},
    {'string': _('Quantity'), 'field': 'quantity', 'align': 'text-center', 'humanize': True},
    {'string': ('UOM'), 'field': 'uom_id', 'align': 'text-left', 'humanize': True},
    {'string': ('Price'), 'field': 'price', 'align': 'text-right', 'humanize': True},
    {'string': _('Discount'), 'field': 'discount', 'align': 'text-right', 'humanize': True},
    {'string': _('Tax'), 'field': 'tax_id'},
    {'string': _('Sub Total'), 'field': 'amount_total', 'align': 'text-right', 'humanize': True},
]


# ========================================================================== #
class InvoiceListView(LoginRequiredMixin, FatherListView):
    """Lista de las ordenes de venta
    """
    model = PyInvoice
    extra_context = {'fields': OBJECT_LIST_FIELDS}


# ========================================================================== #
class InvoiceDetailView(LoginRequiredMixin, FatherDetailView):
    model = PyInvoice
    template_name = 'invoice/detail.html'
    extra_context = {
        'master_fields': OBJECT_DETAIL_FIELDS,
        'detail_fields': DETAIL_OBJECT_LIST_FIELDS,
        'total_fields': OBJECT_TOTAL_FIELDS
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        context['breadcrumbs'] = [
            {
                'url': '{}:list'.format(object_name),
                'name': '{}'.format(verbose_name)
            },
            {
                'url': False,
                'name': self.object.name
            }
        ]
        context['print_url'] = '{}:pdf'.format(object_name)
        context['detail'] = PyInvoiceDetail.objects.filter(
            active=True,
            company_id=self.request.user.active_company_id,
            invoice_id=self.object.pk
        )
        return context


# ========================================================================== #
class InvoiceCreateView(LoginRequiredMixin, FatherCreateView):
    """Vista para agregar las sale
    """
    model = PyInvoice
    form_class = InvoiceForm
    template_name = 'invoice/form.html'
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        context['breadcrumbs'] = [
            {
                'url': '{}:list'.format(object_name),
                'name': '{}'.format(verbose_name)
            }
        ]
        if self.request.POST:
            context['products'] = PRODUCT_FORMSET(self.request.POST)
        else:
            context['products'] = PRODUCT_FORMSET()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        product = context['products']
        with transaction.atomic():
            form.instance.uc = self.request.user.pk
            self.object = form.save()
            if product.is_valid():
                product.instance = self.object
                product.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('PyInvoice:detail', kwargs={'pk': self.object.pk})


# ========================================================================== #
class InvoiceUpdateView(LoginRequiredMixin, FatherUpdateView):
    """Vista para editarar las sale
    """
    model = PyInvoice
    form_class = InvoiceForm
    template_name = 'invoice/form.html'

    def get_context_data(self, **kwargs):
        _pk = self.kwargs.get(self.pk_url_kwarg)
        context = super().get_context_data(**kwargs)
        object_name = self.model._meta.object_name
        verbose_name = self.model._meta.verbose_name
        context['breadcrumbs'] = [
            {
                'url': '{}:list'.format(object_name),
                'name': '{}'.format(verbose_name)
            },
            {
                'url': False,
                'name': self.object.name
            }
        ]
        context['print_url'] = '{}:pdf'.format(object_name)
        if self.request.POST:
            context['form'] = InvoiceForm(self.request.POST, instance=self.object)
            context['products'] = PRODUCT_FORMSET(self.request.POST, instance=self.object)
        else:
            context['form'] = InvoiceForm(instance=self.object)
            context['products'] = PRODUCT_FORMSET(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        products = context['products']
        if self.object.state == 0:
            with transaction.atomic():
                form.instance.um = self.request.user.pk
                if form.is_valid() and products.is_valid():
                    print("Form valid")
                    self.object = form.save(commit=False)
                    products.instance = self.object
                    products.save()
                    self.object.save()
                    return super().form_valid(form)
                else:
                    return super().form_invalid(form)
        else:
            messages.warning(
                self.request,
                _('The current invoice %(obj)s status does not allow updates.') % {'obj': self.object.name}
            )
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('PyInvoice:detail', kwargs={'pk': self.object.pk})


# ========================================================================== #
class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar las sale
    """
    model = PyInvoice
    template_name = 'account/delete.html'
    success_url = reverse_lazy('PyInvoice:list')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete Invoice')
        context['action_url'] = 'PyInvoice:delete'
        context['delete_message'] = '<p>¿Está seguro de eliminar la orden de compras <strong>' + self.object.name + '</strong>?</p>'
        context['cant_delete_message'] = '<p>La orden de compras <strong>' + self.object.name + '</strong>, no puede ser eliminada.</p>'
        # context['detail'] = PyInvoiceDetail.objects.filter(invoice_id=pk).exists()
        context['detail'] = True
        return context

    def delete(self, request, *args, **kwargs):
        # pk = self.kwargs.get(self.pk_url_kwarg)
        # self.object = self.get_object()
        # success_url = self.get_success_url()
        # detail = PyInvoiceDetail.objects.filter(invoice_id=pk).exists()
        # if not detail:
        #     self.object.delete()
        return HttpResponseRedirect(self.success_url)


# ========================================================================== #
@login_required()
def load_product(request):
    context = {}
    product_id = request.GET.get('product')
    product = PyProduct.objects.filter(pk=product_id)
    context['product'] = serializers.serialize('json', product)
    return JsonResponse(data=context, safe=False)


# ========================================================================== #
@login_required()
def load_tax(request):
    context = {}
    tax_id = request.GET.getlist('tax[]')
    tax = PyTax.objects.filter(pk__in=tax_id)
    context['tax'] = serializers.serialize('json', tax)
    return JsonResponse(data=context, safe=False)


# ========================================================================== #
@login_required()
def invoice_state(request, pk, state):
    invoice = PyInvoice.objects.get(pk=pk)
    invoice.state = state
    invoice.save()
    return redirect(
        reverse_lazy('PyInvoice:detail', kwargs={'pk': pk})
    )
