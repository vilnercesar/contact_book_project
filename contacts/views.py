from django.shortcuts import render

from .models import Contact

# Create your views here.


def index(request):

    contacts = Contact.objects.all()

    return render(request, 'contacts/pages/index.html', context={
        'contacts': contacts}

    )


def contact(request, id):

    contact = Contact.objects.filter(id=id).first()

    return render(request, 'contacts/pages/details.html', context={
        'contact': contact}

    )
