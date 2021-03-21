from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .models import Transaction
from .forms import SearchForm, UploadForm

# Create your views here.
class DashboardView(ListView):
    template_name = 'midterm_dashboard.html'
    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 20
    queryset = Transaction.objects.all()
    extra_ordering = {}
    #  queryset = Transaction.objects.filter(pk__range=(1, 10))

    #  def get_context_data(self, **kwargs):
        #  ctx = super().get_context_data(**kwargs)
        #  return ctx

    def get_queryset(self):
        qs = self.queryset
        #  qs = qs.order_by(
            #  'hshd_num'
            #  #  'hshd_num', 'basket_num', 'date', 'product_num', *self.extra_ordering#, 'product_num__department', 'product_num__commodity'
            #  #  'hshd_num', 'basket_num', 'date', 'product_num', *self.extra_ordering#, 'product_num__department', 'product_num__commodity'
        #  )
        _ordering = {
            '1': 'hshd_num',
            '2': 'basket_num',
            '3': 'date',
            '4': 'product_num',
            '5': 'product_num__department',
            '6': 'product_num__commodity'
        }
        hshd_num = self.request.GET.get('hshd_num')
        order_by = self.request.GET.get('order_by')

        q = {}
        if hshd_num:
            q['hshd_num'] = hshd_num

        o = []
        if _ordering.get(order_by):
            o = [_ordering.get(order_by)]

        qs = qs.filter(**q).order_by(*o)
        #  print(qs.query)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        prd_ids = list(ctx[self.context_object_name].values_list('product_num', flat=True))
        #  prd_ids = ctx[self.context_object_name].values_list('product_num', flat=True)
        #  print(prd_ids.query)
        self.queryset = self.queryset.filter(product_num__product_num__in=prd_ids)
        #  self.extra_ordering = {'product_num__department', 'product_num__commodity'}
        self.get_queryset()
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = SearchForm(self.request.GET)
        ctx['upload_form'] = UploadForm()
        #  ctx[self.context_object_name] = 
        return ctx

    #  def post(self, request, *args, **kwargs):
        #  upload_form = UploadForm(self.request.POST, self.request.FILES)
        #  if upload_form.is_valid():
            #  upload_form.save(self.request.FILES)
        #  return redirect('/')
    #  @method_decorator(login_required)
    #  def get(self, request, *args, **kwargs):
        #  ctx = {}
        #  return render(request=request, template_name='midterm_dashboard.html', context=ctx)

    #  def get(self, request, *args, **kwargs):
        #  for tr in list(self.queryset):
            #  print(tr.hshd_num_id)
        #  return super().get(request, *args, **kwargs)

class MidtermIndexView(TemplateView):
    template_name = 'midterm_index.html'


class UploadDatasetView(FormView):
    form_class = UploadForm
    template_name = 'midterm_upload_dataset.html'
    success_url = reverse_lazy('midterm:dashboard')


class ChartsView(TemplateView):
    template_name = 'midterm_charts.html'
