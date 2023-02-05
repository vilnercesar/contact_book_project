from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render

from .models import Contact

# Create your views here.


def index(request):

    contacts = Contact.objects.filter(is_publish=True).order_by('-id')
    paginator = Paginator(contacts, 5)
    page = request.GET.get('p')
    contacts = paginator.get_page(page)
    return render(request, 'contacts/pages/index.html', context={
        'contacts': contacts}

    )


def contact(request, id):

    contact = get_object_or_404(Contact, id=id, is_publish=True)

    return render(request, 'contacts/pages/details.html', context={
        'contact': contact}

    )


def search(request):
    term = request.GET.get('term')

    fake_fields = Concat('first_name', Value(
        ''), 'last_name')

    if term is None or not term:
        messages.add_message(request, messages.ERROR,
                             'O campo busca não pode ficar vazio')
        return redirect('index')

    contacts = Contact.objects.annotate(
        full_name=fake_fields
    ).filter(Q(full_name__icontains=term) | Q(cell_phone__icontains=term),
             is_publish=True)
    if not contacts:
        messages.add_message(request, messages.ERROR, 'Nenhum paramêtro encontrado')  # noqa: E501

    paginator = Paginator(contacts, 3)
    page = request.GET.get('p')
    contacts = paginator.get_page(page)
    return render(request, 'contacts/pages/search.html', context={
        'contacts': contacts}

    )
