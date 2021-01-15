from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from .utils import get_ipgeodata, get_geodata, get_distance, update_map_location, get_zoom_value
import folium


def calculate_distance_view(request):
    # obj = get_object_or_404(Measurement, id=3)
    obj = Measurement.objects.all().reverse()
    form = MeasurementModelForm(request.POST or None)

    # get current location
    mylocation = get_ipgeodata()
    location_geodata = get_geodata(mylocation)
    # get point A coords
    pointA = (location_geodata.latitude, location_geodata.longitude)

    # initial folium map
    m = folium.Map(width=800, height=500, location=pointA)

    # add point A marker
    folium.Marker(location=pointA, tooltip='click for more', popup=location_geodata, icon=folium.Icon(color='purple')).add_to(m)
    
    if form.is_valid():
        instance = form.save(commit=False)
        
        # get destination
        destination = form.cleaned_data.get('destination')
        destination_geodata = get_geodata(destination) 
        
        # get point B coords
        pointB = (destination_geodata.latitude, destination_geodata.longitude)
        
        # calculate distance between two points
        distance = get_distance(pointA, pointB)

        # update map location
        m.location = update_map_location(pointA, pointB)
        m.fit_bounds([pointA, pointB])

        # add point B marker
        folium.Marker(location=pointB, tooltip='click for more', popup=destination_geodata, icon=folium.Icon(color='red')).add_to(m)

        # save data to database
        instance.location = location_geodata
        instance.destination = destination_geodata
        instance.distance = distance
        instance.save()
    
    # html representation of the map object
    m = m._repr_html_()

    context = {
        'distance': obj,
        'form': form,
        'map': m,
    }

    return render(request, 'measurements/main.html', context)
