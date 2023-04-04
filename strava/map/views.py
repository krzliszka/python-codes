from django.shortcuts import render
import folium

# Create your views here.
def base_map(request):
    """
    Creating own map object
    """
    main_map = folium.Map(location=[43.45, -80.476], zoom_start = 12)
    main_map_html = main_map.repr_html_()

    context = {
        "main_map": main_map_html
    }

    return render(request, 'index.html', context)