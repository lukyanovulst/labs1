from django.shortcuts import render

def index(request):
    return render(request, 'cardapp/index.html')

def about(request):
    context = {
        'age': 22,
        'university': 'УЛГТУ',
        'course': 2,
        'specialty': 'Информационные системы и технологии',
        'hobbies': [
            'Программирование на Python',
            'Изучение новых технологий',
            'Фотография',
            'Игра на гитаре',
            'Просмотр фильмов и сериалов'
        ]
    }
    return render(request, 'cardapp/about.html', context)

def contacts(request):
    context = {
        'vk_url': 'https://vk.com/id244095997',
        'email': 'LukyanovS@ulstu.ru',
    }
    return render(request, 'cardapp/contacts.html', context)
