from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Contact

# Create your views here.


def index(request):

    contacts = Contact.objects.filter(is_publish=True).order_by('-id')
    paginator = Paginator(contacts, 3)
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

    if term is None:
        raise Http404()

    contacts = Contact.objects.annotate(
        full_name=fake_fields
    ).filter(Q(full_name__icontains=term) | Q(cell_phone__icontains=term),
             is_publish=True)

    paginator = Paginator(contacts, 3)
    page = request.GET.get('p')
    contacts = paginator.get_page(page)
    return render(request, 'contacts/pages/search.html', context={
        'contacts': contacts}

    )
