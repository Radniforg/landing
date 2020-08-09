from collections import Counter

from django.shortcuts import render
from django.shortcuts import HttpResponse

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    page_type = request.GET.get('from-landing')
    if page_type == 'original':
        counter_click['original'] += 1
    elif page_type == 'test':
        counter_click['test'] += 1
    else:
        pass
    return render(request, 'index.html')


def landing(request):
    page_type = request.GET.get('ab-test-arg')
    if page_type == 'original':
        counter_show['original'] += 1
        url = 'landing.html'
    elif page_type == 'test':
        counter_show['test'] += 1
        url = 'landing_alternate.html'
    else:
        url = 'landing.html'
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    return render(request, url)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    try:
        test_conversion = counter_click['test']/counter_show['test']
    except ZeroDivisionError:
        test_conversion = 0
    try:
        original_conversion = counter_click['original']/counter_show['original']
    except ZeroDivisionError:
        original_conversion = 0
    return render(request, 'stats.html', context={
        'test_conversion': round(test_conversion, 2),
        'original_conversion': round(original_conversion, 2),
    })
