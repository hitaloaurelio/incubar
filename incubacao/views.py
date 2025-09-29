from django.shortcuts import render

# Create your views here.


from django.views.generic import UpdateView

from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .models import Lote, EggType,Anotacao
from .forms import LoteForm
from django.contrib.auth.mixins import LoginRequiredMixin

class LoteListView(LoginRequiredMixin,ListView):
    model = Lote
    template_name = 'lote_list.html'
    context_object_name = 'lotes'
    ordering = ['-id']

    login_url = 'login/'  # se não estiver logado, redireciona para login
    redirect_field_name = 'next'  # padrão, opcional

    def get_queryset(self):
        return Lote.objects.filter(usuario=self.request.user).order_by('-id')

class LoteCreateView(LoginRequiredMixin, CreateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lote_form.html'
    success_url = reverse_lazy('incubacao:lote_lista')
    login_url = '/login/'

    def form_valid(self, form):
        user = self.request.user

        # 🔹 Verifica limite de lotes para usuários Free
        if user.tipo == 'FREE' and user.lotes.count() >= 1:
            print("Usuário Free só pode criar 1 lote. Faça upgrade para ilimitado.")
            messages.error(
                self.request,
                'Usuário Free só pode criar 1 lote. Faça upgrade para ilimitado. '
                '<a href="https://wa.me/5599981552048?text=Ol%C3%A1%2C+quero+usar+uma+conta+paga+do+seu+Sistema+Incubar..." '
                'target="_blank" class="btn btn-success btn-sm ms-2">Fale no WhatsApp</a>'
            )
            return self.form_invalid(form)

        # 🔹 Atribui o usuário ao lote
        form.instance.usuario = user
        resp = super().form_valid(form)
        messages.success(self.request, "Lote cadastrado com sucesso!")
        return resp

   
class LoteDetailView(LoginRequiredMixin,DetailView):
    model = Lote
    template_name = 'lote_detail.html'
    context_object_name = 'lote'
    login_url = '/login/' 

from django.core.exceptions import PermissionDenied

class LoteUpdateView(LoginRequiredMixin,UpdateView):
    model = Lote
    form_class = LoteForm
    template_name = 'lote_form.html'
    success_url = reverse_lazy('incubacao:lote_lista')  # Redireciona para a lista após sucesso
    login_url = '/login/' 


    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo == "FREE":
            raise PermissionDenied("Usuário FREE não pode editar lotes.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Mensagem de sucesso ao editar o lote
        messages.success(self.request, 'Lote atualizado com sucesso!')
        return super().form_valid(form)    
    

from django.views.generic import DeleteView

class LoteDeleteView(LoginRequiredMixin,DeleteView):
    model = Lote
    template_name = 'lote_confirm_delete.html'  # Página de confirmação de exclusão
    success_url = reverse_lazy('incubacao:lote_lista')  # Redireciona para a lista de lotes
    login_url = '/login/' 

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Lote deletado com sucesso!')
        return super().delete(request, *args, **kwargs)
    
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")  # depois de cadastrar, vai para o login


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect("/login/")  # ajuste para sua URL de login
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})



def listmenu(request):
    return render(request, "listmenu.html")

def armazenamento(request):
    return render(request, "armazenamento.html")


def incubacao(request):
    return render(request, "incubacao.html")

def momemnto_incubacao(request):
    return render(request, "momento_incubacao.html")


def operacao_maquina(request):
    return render(request, "operacao_maquina.html")

def controle_temperatura(request):
    return render(request, "controle_temperatura.html")

def umidade(request):
    return render(request, "umidade.html")

def viragem(request):
    return render(request, "viragem.html")

def transferecia_ovos(request):
    return render(request, "transferecia_ovos.html")

def retirada_pintinhos(request):
    return render(request, "retirada_pintinhos.html")

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def adicionar_anotacao(request, lote_id):
    lote = get_object_or_404(Lote, pk=lote_id, usuario=request.user)
    if request.method == "POST":
        texto = request.POST.get("texto")
        if texto:
            Anotacao.objects.create(lote=lote, texto=texto)
    return redirect("incubacao:lote_detalhe", pk=lote.pk)



def anotacao_deletar(request, pk):

    anotacao = get_object_or_404(Anotacao, pk=pk)

    # Verifica se foi enviado por POST
    if request.method == "POST":
        lote = anotacao.lote  # Para redirecionar de volta
        anotacao.delete()
        messages.success(request, "Anotação excluída com sucesso.")
        return redirect("incubacao:lote_detalhe", pk=lote.pk)

    # Se não for POST, volta sem excluir
    messages.error(request, "Requisição inválida.")
    return redirect("incubacao:lote_lista")



from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Anotacao, Lote

def anotacao_editar(request, pk):
    anotacao = get_object_or_404(Anotacao, pk=pk)
    
    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            anotacao.texto = texto
            anotacao.save()
            messages.success(request, "Anotação atualizada com sucesso!")
        else:
            messages.error(request, "O texto da anotação não pode estar vazio.")
    
    # redireciona de volta para a página do lote
    return redirect("incubacao:lote_detalhe", pk=anotacao.lote.pk)
