from django.shortcuts import render
from modules import trackers_gecko
from .forms import HomeForm
from .forms import ContactForm
from django.core.mail import send_mail


def home(request):
    context = {
        'results': None,
        'status': None,
        'searched': None,
        'delay': None,
    }

    if request.method == 'POST':
        form = HomeForm(request.POST)
        context['form'] = form

        if form.is_valid():

            context['searched'] = form.data['url_post']
            context['delay'] = int(form.data['delay'])
            process = trackers_gecko.track_light(context['searched'], context['delay'])
            context['results'] = process[0]
            context['status'] = process[1]
            context['number'] = len(process[0])

    else:
        form = HomeForm()
        context['form'] = form
    return render(request, 'track_app/home.html', context)


def about(request):
    return render(request, 'track_app/about.html', {'title': 'About'})


def contact(request):
    context = {
        'title': 'Contact',
        'ind': None
     }
    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form'] = form
        if form.is_valid():
            context['ind'] = 1
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            send_mail(
                        'Track_Light-contactform ' + sender,
                        message,
                        'trackapps2020@gmail.com',
                        ['trackapps2020@gmail.com'],
                        fail_silently=True,
                    )
    else:
        form = ContactForm()
        context['form'] = form
    return render(request, 'track_app/contact.html', context)
