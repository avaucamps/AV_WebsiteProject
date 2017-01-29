import datetime

from django.shortcuts import render, get_object_or_404
import tmdbsimple as tmdb


tmdb.API_KEY = '13866daf0372e25d15b0d1f2d35a2d28'


def movies(request):
    popular = tmdb.Movies()
    response_popular = popular.popular()
    popular.results = format_date(popular.results[:6])
    popular.results = format_title(popular.results[:6])
    top_rated = tmdb.Movies()
    response_top_rated = top_rated.top_rated()
    top_rated.results = format_date(top_rated.results[:6])
    top_rated.results = format_title(top_rated.results[:6])
    now_playing = tmdb.Movies()
    response_now_playing = now_playing.now_playing()
    now_playing.results = format_date(now_playing.results[:6])
    now_playing.results = format_title(now_playing.results[:6])
    upcoming = tmdb.Movies()
    response_upcoming = upcoming.upcoming()
    upcoming.results = format_title(upcoming.results[:6])
    return render(request, 'movies/index.html', {'popular_movies': popular.results,
                                                  'top_rated_movies': top_rated.results,
                                                  'now_playing_movies': now_playing.results,
                                                  'upcoming_movies': upcoming.results})


def movie_detail(request, movie_id):
    # Gather and parse basic movie information
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    runtime = movie.runtime
    hours = int(runtime / 60)
    minutes = runtime % 60
    str_minutes = str(minutes)
    if minutes < 10:
        str_minutes = '0' + str(minutes)
    runtime = str(hours) + 'h' + str_minutes
    date = movie.release_date
    genres = ''
    for genre in movie.genres:
        if genres == '':
            genres = genres + genre['name']
        else:
            genres = genres + ', ' + genre['name']
    movie_information = {'id': movie_id, 'title': movie.title, 'runtime': runtime, 'release_date': date, 'overview': movie.overview,
                         'genres': genres, 'poster': movie.poster_path}
    # Get Crew and Cast information
    cast_information = movie.credits()['cast'][:6]
    directors = []
    for member in movie.credits()['crew']:
        if member['job'] == 'Director':
            directors.append(member)
    # Get video, poster and backdrops
    video = movie.videos()['results'][:1]
    if len(video) > 0:
        video_key = video[0]['key']
    else:
        video_key = False
    images = movie.images()
    if len(images['backdrops']) >= 3:
        backdrops = images['backdrops'][:3]
    else:
        backdrops = images['backdrops'][:len(images['backdrops'])]
    # Return information
    return render(request, 'movies/details.html', {'movie_information': movie_information, 'cast': cast_information,
                                                   'crew': directors, 'video_key': video_key, 'backdrops': backdrops})


def movie_cast(request, movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    castandcrew = movie.credits()
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
    return render(request, 'movies/castncrew.html', {'cast': cast, 'crew': crew, 'departments': departments,
                                                     'castNoPicture': castNoPicture})


def movie_videos(request, movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.videos()
    types = []
    exist = False
    for video in movie.results:
        for type in types:
            if type == video['type']:
                exist = True
        if not exist:
            types.append(video['type'])
        exist = False
    return render(request, 'movies/videos.html', {'videos': movie.results, 'types': types})


def movie_backdrops(request, movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.images()
    backdrops = response['backdrops']
    return render(request, 'movies/backdrops.html', {'backdrops': backdrops})


def movie_posters(request, movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.images()
    posters = response['posters']
    return render(request, 'movies/posters.html', {'posters': posters, 'movie_id': movie_id})


def popular_movies(request):
    popular = tmdb.Movies()
    response_popular = popular.popular()
    popular.results = format_date(popular.results)
    popular.results = format_overview(popular.results)
    return render(request, 'movies/popular_movies.html', {'popular_movies': popular.results})


def top_rated_movies(request):
    top_rated = tmdb.Movies()
    response_top_rated = top_rated.top_rated()
    top_rated.results = format_date(top_rated.results)
    top_rated.results = format_overview(top_rated.results)
    return render(request, 'movies/top_rated_movies.html', {'top_rated_movies': top_rated.results})


def now_playing_movies(request):
    now_playing = tmdb.Movies()
    response_now_playing = now_playing.now_playing()
    now_playing.results = format_date(now_playing.results)
    now_playing.results = format_overview(now_playing.results)
    return render(request, 'movies/now_playing_movies.html', {'now_playing_movies': now_playing.results})


def upcoming_movies(request):
    upcoming = tmdb.Movies()
    response_upcoming = upcoming.upcoming()
    upcoming.results = format_overview(upcoming.results)
    return render(request, 'movies/upcoming_movies.html', {'upcoming_movies': upcoming.results})


def format_date(list_items):
    for item in list_items:
        item['release_date'] = item['release_date'][:4]
    return list_items


def format_overview(list_items):
    for item in list_items:
        item['overview'] = item['overview'][:250] + '...'
    return list_items


def format_title(list_items):
    for item in list_items:
        if len(item['title']) > 20:
            item['title'] = item['title'][:20] + '...'
    return list_items
