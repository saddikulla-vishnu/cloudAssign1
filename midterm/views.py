import pandas as pd
import json
import itertools

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
    queryset = Transaction.objects.all()
    COLORS = [
        '#3e95cd', '#8e5ea2', '#3cba9f', '#e8c3b9', '#c45850', '#67595E', '#E8B4B8',
        '#A49393', '#3CACAE', '#3A4A3D', '#C26DBC', '#EEB5EB', '#313E61', '#444444',
    ]
    COLORS_CYCLE = itertools.cycle(COLORS)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ALL_VALUES = (
            'basket_num', 'date', 'spend', 'units', 'store_region', 'week_num', 'year', 'hshd_num_id', 'product_num_id',
            'hshd_num__loyalty_flag', 'hshd_num__age_range', 'hshd_num__marital_status', 'hshd_num__income_range',
            'hshd_num__homeowner_desc', 'hshd_num__hshd_composition', 'hshd_num__hshd_size', 'hshd_num__children',
            'product_num__department', 'product_num__commodity', 'product_num__brand_type', 'product_num__natural_organic_flag',
        )
        #  df = pd.DataFrame(self.queryset.select_related('hshd_num', 'product_num').values(*ALL_VALUES)[:10000])
        df = pd.DataFrame(self.queryset.select_related('hshd_num', 'product_num').values(*ALL_VALUES))
        #  print(df.head())
        ctx['chart_data'] = []

        spnd_by_yr_and_dprmnt = self.get_spend_by_year_and_department(df)
        #  print(spnd_by_yr_and_dprmnt)
        ctx['chart_data'].append(spnd_by_yr_and_dprmnt)

        spnd_by_yr = self.get_spend_by_year(df)
        #  print(spnd_by_yr)
        ctx['chart_data'].append(spnd_by_yr)

        spnd_by_marital = self.get_spend_by_marital(df)
        #  print(spnd_by_marital)
        ctx['chart_data'].append(spnd_by_marital)

        spnd_by_cmdity_yr = self.get_spend_by_cmdty_yr(df)
        #  print(spnd_by_cmdity_yr)
        ctx['chart_data'].append(spnd_by_cmdity_yr)

        spend_by_marital_incm = self.get_spend_by_marital_incm(df)
        #  print(spend_by_marital_incm)
        ctx['chart_data'].append(spend_by_marital_incm)

        spend_by_hshd_size = self.get_spend_by_hshd_size(df)
        #  print(spend_by_hshd_size)
        ctx['chart_data'].append(spend_by_hshd_size)

        spend_by_chldrn_hshd_size = self.get_spend_by_chldrn_hshd_size(df)
        #  print(spend_by_chldrn_hshd_size)
        ctx['chart_data'].append(spend_by_chldrn_hshd_size)

        ctx['chart_data'] = json.dumps(ctx['chart_data'])
        return ctx

    def get_spend_by_year_and_department(self, df):
        dataset = df.groupby(['product_num__department', 'year'])['spend'].sum().reset_index().to_dict('records')
        data = {'labels': set(), 'datasets': []}
        for key, grp in itertools.groupby(dataset, lambda x: x['product_num__department']):
            grp = list(grp)
            grp.sort(key=lambda x: x['year'])
            grp_data = [not data['labels'].add(x['year']) and x['spend'] for x in grp]
            data['datasets'].append({
                'data': grp_data,
                'label': key.strip(),
                'backgroundColor': next(self.COLORS_CYCLE),
            })
        data['labels'] = list(data['labels'])
        ctx = {
            'type': 'bar',
            'data': data,
            'options': {
                #  'legend': {'display': True},
                'title': {
                    'display': True,
                    'text': 'SPEND by Year and DEPARTMENT'
                },
                #  'responsive': False,
                #  'maintainAspectRatio': True
            },
            'canvas_id': 'id_spnd_b_yr_dprmnt'
        }
        return ctx

    def get_spend_by_year(self, df):
        dataset = df.groupby(['year'])['spend'].sum().reset_index().to_dict('records')
        data = {
            'labels': [x['year'] for x in dataset],
            'datasets': [{
                'label': "Spend",
                'data': [x['spend'] for x in dataset],
                #  'borderColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                'borderColor': next(self.COLORS_CYCLE),
                'fill': False
            }]
        }
        ctx = {
            'type': 'line',
            'data': data,
            'options': {
                #  'legend': {'display': True},
                'title': {
                    'display': True,
                    'text': 'SPEND by Year'
                },
            },
            'canvas_id': 'id_spnd_b_yr'
        }
        return ctx

    def get_spend_by_marital(self, df):
        dataset = df.groupby(['hshd_num__marital_status'])['spend'].sum().reset_index().to_dict('records')
        data = {
            'labels': [x['hshd_num__marital_status'] for x in dataset],
            'datasets': [{
                'label': "Spend",
                'data': [x['spend'] for x in dataset],
                #  'borderColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                'backgroundColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                #  'borderColor': next(self.COLORS_CYCLE),
                #  'fill': False
            }]
        }
        ctx = {
            'type': 'pie',
            'data': data,
            'options': {
                #  'legend': {'display': True},
                'title': {
                    'display': True,
                    'text': 'SPEND by MARITAL'
                },
            },
            'canvas_id': 'id_spnd_b_marital'
        }
        return ctx

    def get_spend_by_cmdty_yr(self, df):
        dataset = df.groupby(['year', 'product_num__commodity'])['spend'].sum().reset_index().to_dict('records')
        data = {'labels': set(), 'datasets': []}
        for key, grp in itertools.groupby(dataset, lambda x: x['year']):
            grp = list(grp)
            grp.sort(key=lambda x: x['product_num__commodity'])
            grp_data = [not data['labels'].add(x['product_num__commodity']) and x['spend'] for x in grp]
            data['datasets'].append({
                'data': grp_data,
                'label': key,
                'backgroundColor': next(self.COLORS_CYCLE),
            })
        data['labels'] = list(data['labels'])
        ctx = {
            'type': 'bar',
            'data': data,
            'options': {
                #  'legend': {'display': True},
                'title': {
                    'display': True,
                    'text': 'SPEND by COMMODITY and Year'
                },
                'scales': {
                    'xAxes': [{
                        'stacked': True
                    }],
                    'yAxes': [{
                        'stacked': True
                    }]

                },
            },
            'canvas_id': 'id_spend_by_cmdty_yr'
        }
        return ctx

    def get_spend_by_marital_incm(self, df):
        dataset = df.groupby(['hshd_num__marital_status', 'hshd_num__income_range'])['spend'].sum().reset_index().to_dict('records')
        dataset.sort(key=lambda x: x['hshd_num__marital_status'])
        #  print(dataset)
        data = {'labels': set(), 'datasets': []}

        # First Way
        marital_status = {x['hshd_num__marital_status'] for x in dataset}
        marital_status_colors = {x: next(self.COLORS_CYCLE) for x in marital_status}
        data = {
            'labels': [x['hshd_num__income_range'] for x in dataset],
            'datasets': [{
                'label': "Spend",
                'data': [x['spend'] for x in dataset],
                #  'borderColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                'backgroundColor': [marital_status_colors[x['hshd_num__marital_status']] for x in dataset],
            }]
        }

        # Second Way
        #  for key, grp in itertools.groupby(dataset, lambda x: x['hshd_num__marital_status']):
            #  grp = list(grp)
            #  grp.sort(key=lambda x: x['hshd_num__income_range'])
            #  for x in grp:
                #  data['labels'].add(x['hshd_num__income_range'])
        #  data['labels'] = list(data['labels'])

        #  for key, grp in itertools.groupby(dataset, lambda x: x['hshd_num__marital_status']):
            #  grp = list(grp)
            #  grp.sort(key=lambda x: x['hshd_num__income_range'])
            #  grp_data = [0]*len(data['labels'])
            #  for x in grp:
                #  grp_data[data['labels'].index(x['hshd_num__income_range'])] = x['spend']
            #  data['datasets'].append({
                #  'data': grp_data,
                #  'label': key.strip(),
                #  'backgroundColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
            #  })
        ctx = {
            'type': 'pie',
            'data': data,
            'options': {
                #  'legend': {'display': False},
                'title': {
                    'display': True,
                    'text': 'SPEND by MARITAL and INCOME_RANG'
                },
                #  'responsive': False,
                #  'maintainAspectRatio': True
            },
            'canvas_id': 'id_spend_by_marital_incm'
        }
        return ctx

    def get_spend_by_hshd_size(self, df):
        dataset = df.groupby(['hshd_num__hshd_size'])['spend'].sum().reset_index().to_dict('records')
        data = {
            'labels': [x['hshd_num__hshd_size'] for x in dataset],
            'datasets': [{
                'label': "Spend",
                'data': [x['spend'] for x in dataset],
                #  'borderColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                'backgroundColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                'fill': False
            }]
        }
        ctx = {
            'type': 'pie',
            'data': data,
            'options': {
                #  'legend': {'display': True},
                'title': {
                    'display': True,
                    'text': 'SPEND by HH_SIZE'
                },
            },
            'canvas_id': 'id_spend_by_hshd_size'
        }
        return ctx

    def get_spend_by_chldrn_hshd_size(self, df):
        dataset = df.groupby(['hshd_num__children', 'hshd_num__hshd_size'])['spend'].sum().reset_index().to_dict('records')
        dataset.sort(key=lambda x: x['hshd_num__children'])
        #  print(dataset)
        data = {'labels': set(), 'datasets': []}

        # First Way
        marital_status = {x['hshd_num__children'] for x in dataset}
        marital_status_colors = {x: next(self.COLORS_CYCLE) for x in marital_status}
        data = {
            'labels': [x['hshd_num__hshd_size'] for x in dataset],
            'datasets': [{
                'label': "Spend",
                'data': [x['spend'] for x in dataset],
                #  'borderColor': [next(self.COLORS_CYCLE) for x in range(len(dataset))],
                'backgroundColor': [marital_status_colors[x['hshd_num__children']] for x in dataset],
            }]
        }

        ctx = {
            'type': 'doughnut',
            'data': data,
            'options': {
                #  'legend': {'display': False},
                'title': {
                    'display': True,
                    'text': 'SPEND by CHILDREN and HH_SIZE'
                },
                #  'responsive': False,
                #  'maintainAspectRatio': True
            },
            'canvas_id': 'id_spend_by_chldrn_hshd_size'
        }
        return ctx
