from django.shortcuts import render
import tmdbsimple as tmdb

tmdb.API_KEY = '13866daf0372e25d15b0d1f2d35a2d28'


def search(request):
    search_data = tmdb.Search()
    search_query = request.GET.get("q")
    response = search_data.multi(query=search_query)
    search_data.results = format_title(search_data.results)
    return render(request, 'search/search.html', {'search': search_data.results})


def format_title(list_items):
    for item in list_items:
        if item['media_type'] == 'movie':
            if len(item['title']) > 20:
                item['title'] = item['title'][:20] + '...'
        elif item['media_type'] == 'tv':
            if len(item['name']) > 20:
                item['name'] = item['name'][:20] + '...'
    return list_items
