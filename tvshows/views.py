from django.shortcuts import render, get_object_or_404
import tmdbsimple as tmdb


tmdb.API_KEY = '13866daf0372e25d15b0d1f2d35a2d28'


def index(request):
    popular = tmdb.TV()
    response_popular = popular.popular()
    popular.results = format_date(popular.results[:6])
    popular.results = format_name(popular.results[:6])
    top_rated = tmdb.TV()
    response_top_rated = top_rated.top_rated()
    top_rated.results = format_date(top_rated.results[:6])
    top_rated.results = format_name(top_rated.results[:6])
    on_the_air = tmdb.TV()
    response_on_the_air = on_the_air.on_the_air()
    on_the_air.results = format_date(on_the_air.results[:6])
    on_the_air.results = format_name(on_the_air.results[:6])
    airing_today = tmdb.TV()
    response_airing_today = airing_today.airing_today()
    airing_today.results = format_date(airing_today.results[:6])
    airing_today.results = format_name(airing_today.results[:6])
    return render(request, 'tvshows/index.html', {'popular': popular.results, 'top_rated': top_rated.results,
                                                  'on_the_air': on_the_air.results,
                                                  'airing_today': airing_today.results})


def tvshow_detail(request, tvshow_id):
    tvshow = tmdb.TV(tvshow_id)
    info = tvshow.info()
    images = tvshow.images()
    video = tvshow.videos()['results'][:1]
    if len(video) > 0:
        video_key = video[0]['key']
    else:
        video_key = False
    if len(images['backdrops']) >= 3:
        backdrops = images['backdrops'][:3]
    else:
        backdrops = images['backdrops'][:len(images['backdrops'])]
    cast = tvshow.credits()['cast'][:6]
    directors = []
    return render(request, 'tvshows/details.html', {'tv_show': info, 'images': images, 'video_key': video_key,
                                                    'backdrops': backdrops, 'directors': directors, 'cast': cast})


def cast(request, tvshow_id):
    tvshow = tmdb.TV(tvshow_id)
    response = tvshow.info()
    castandcrew = tvshow.credits()
    cast = castandcrew['cast']
    crew = castandcrew['crew']
    departments = []
    exist = False
    castNoPicture = []
    for member in cast:
        if not member['profile_path']:
            castNoPicture.append(member)
            cast.remove(member)
    for member in crew:
        for department in departments:
            if department == member['department']:
                exist = True
        if not exist:
            departments.append(member['department'])
        exist = False
    return render(request, 'tvshows/cast&crew.html', {'cast': cast, 'crew': crew, 'departments': departments,
                                                     'castNoPicture': castNoPicture})


def popular(request):
    popular_shows = tmdb.TV()
    response = popular_shows.popular()
    popular_shows.results = format_overview(popular_shows.results)
    return render(request, 'tvshows/popular.html', {'popular': popular_shows.results})


def top_rated(request):
    top_rated= tmdb.TV()
    response = top_rated.top_rated()
    top_rated.results = format_overview(top_rated.results)
    return render(request, 'tvshows/top_rated.html', {'top_rated': top_rated.results})


def on_the_air(request):
    on_the_air= tmdb.TV()
    response = on_the_air.on_the_air()
    on_the_air.results = format_overview(on_the_air.results)
    return render(request, 'tvshows/on_the_air.html', {'on_the_air': on_the_air.results})


def airing_today(request):
    airing_today= tmdb.TV()
    response = airing_today.airing_today()
    airing_today.results = format_overview(airing_today.results)
    return render(request, 'tvshows/airing_today.html', {'airing_today': airing_today.results})


def videos(request, tvshow_id):
    tv_show = tmdb.TV(tvshow_id)
    response = tv_show.videos()
    types = []
    exist = False
    for video in tv_show.results:
        for type in types:
            if type == video['type']:
                exist = True
        if not exist:
            types.append(video['type'])
        exist = False
    return render(request, 'tvshows/videos.html', {'videos': tv_show.results, 'types': types})


def backdrops(request, tvshow_id):
    tv_show = tmdb.TV(tvshow_id)
    response = tv_show.images()
    backdrops = response['backdrops']
    return render(request, 'tvshows/backdrops.html', {'backdrops': backdrops})


def posters(request, tvshow_id):
    tv_show = tmdb.TV(tvshow_id)
    response = tv_show.images()
    posters = response['posters']
    return render(request, 'tvshows/posters.html', {'posters': posters})


def format_date(list_items):
    for item in list_items:
        item['first_air_date'] = item['first_air_date'][:4]
    return list_items


def format_overview(list_items):
    for item in list_items:
        item['overview'] = item['overview'][:200] + '...'
    return list_items


def format_name(list_items):
    for item in list_items:
        if len(item['name']) > 20:
            item['name'] = item['name'][:20] + '...'
    return list_items
