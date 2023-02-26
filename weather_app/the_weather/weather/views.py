from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index (request):
    try:
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=cd863b9b9203e81134f9111cdef8f337'

        City.objects.all().delete()

        if request.method == 'POST':
            form = CityForm(request.POST)
            form.save()
        else:
            x = City(name='New York')
            x.save()

        form = CityForm()

        cities = City.objects.all()
        weather_data = []

        r = requests.get(url.format(cities[0])).json()
        print(r)

        city_weather = {
            'city': cities[0],
            'country' : r['sys']['country'],
            'temperature' : int(round(r['main']['temp'], 0)),
            'description': (r['weather'][0]['description']).capitalize(),
            'icon': r['weather'][0]['icon'],
            'humidity' : r['main']['humidity'],
            'wind' : (round(r['wind']['speed'], 2)),
            'real_feel' : int(round(r['main']['feels_like'],0))
        }

        weather_data.append(city_weather)


        
        context = {'weather_data' : weather_data, 'form' : form}
        return render(request, 'weather/weather.html', context)
    except KeyError:
        return render(request, "weather/404.html")
