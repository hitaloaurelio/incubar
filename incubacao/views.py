from django.shortcuts import render

# Create your views here.


from django.views.generic import UpdateView

from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .models import Lote, EggType
from .forms import LoteForm

class LoteListView(ListView):
    model = Lote
    template_name = 'lote_list.html'
    context_object_name = 'lotes'
    ordering = ['-id']

class LoteCreateView(CreateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lote_form.html'
    success_url = reverse_lazy('incubacao:lote_lista')

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, 'Lote cadastrado com sucesso!')
        # opcional: gerar checklist básico
       
        return resp

   
class LoteDetailView(DetailView):
    model = Lote
    template_name = 'lote_detail.html'
    context_object_name = 'lote'


class LoteUpdateView(UpdateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lote_form.html'
    success_url = reverse_lazy('incubacao:lote_lista')  # Redireciona para a lista após sucesso

    def form_valid(self, form):
        # Mensagem de sucesso ao editar o lote
        messages.success(self.request, 'Lote atualizado com sucesso!')
        return super().form_valid(form)    
    

from django.views.generic import DeleteView

class LoteDeleteView(DeleteView):
    model = Lote
    template_name = 'lote_confirm_delete.html'  # Página de confirmação de exclusão
    success_url = reverse_lazy('incubacao:lote_lista')  # Redireciona para a lista de lotes

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Lote deletado com sucesso!')
        return super().delete(request, *args, **kwargs)