from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.shortcuts import render
import random

def index(request):
    legal_latin_quotes = [
        "Fiat iustitia, ruat caelum - Нека се извърши правосъдие, дори небесата да се сринат.",
        "Ignorantia legis non excusat - Незнанието на закона не е извинение.",
        "Dura lex, sed lex - Законът е строг, но е закон.",
        "Nemo plus iuris ad alium transferre potest quam ipse habet - Никой не може да прехвърли повече права, отколкото сам притежава.",
        "Ubi societas, ibi ius - Където има общество, там има закон.",
        "Audi alteram partem - Чуйте и другата страна.",
        "Lex retro non agit - Законът няма обратно действие.",
        "Pacta sunt servanda - Договорите трябва да бъдат спазвани.",
        "Nemo debet bis vexari pro eadem causa - Никой не може да бъде съден два пъти за едно и също.",
        "Cessante ratione legis, cessat ipsa lex - Когато причината за закона изчезне, законът сам престава да действа.",
    ]
    quote = random.choice(legal_latin_quotes)  # Избира случайна поговорка
    return render(request, 'index.html', {'quote': quote})

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def contact_view(request):
    return render(request, 'contact.html')

def password_reset_view(request):
    return render(request, 'password-reset.html')

def error_404_view(request, exception=None):
    return render(request, '404.html')

