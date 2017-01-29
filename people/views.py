from django.shortcuts import render, get_object_or_404
import tmdbsimple as tmdb


tmdb.API_KEY = '13866daf0372e25d15b0d1f2d35a2d28'


def index(request):
    popular_people = tmdb.People()
    response = popular_people.popular()
    return render(request, 'people/index.html', {'popular_people': popular_people.results})


def people_detail(request, people_id):
    people = tmdb.People(people_id)
    info = people.info()
    images = people.images()['profiles']
    movie_credits = people.movie_credits()
    tv_credits = people.tv_credits()
    movie_credits_cast = sort(movie_credits['cast'], 'release_date')
    tv_credits_cast = sort(tv_credits['cast'], 'first_air_date')
    movie_credits_cast.reverse()
    tv_credits_cast.reverse()
    movie_credits_cast = format_dates(movie_credits_cast, 'release_date')
    tv_credits_cast = format_dates(tv_credits_cast, 'first_air_date')
    movie_credits_crew = sort(movie_credits['crew'], 'release_date')
    tv_credits_crew = sort(tv_credits['crew'], 'first_air_date')
    movie_credits_crew.reverse()
    tv_credits_crew.reverse()
    movie_credits_crew = format_dates(movie_credits_crew, 'release_date')
    tv_credits_crew = format_dates(tv_credits_crew, 'first_air_date')
    return render(request, 'people/people_detail.html', {'people': info, 'images': images,
                                                         'movie_credits_cast': movie_credits_cast,
                                                         'tv_credits_cast': tv_credits_cast,
                                                         'movie_credits_crew': movie_credits_crew,
                                                         'tv_credits_crew': tv_credits_crew})


def format_dates(list_items, date_name):
    for item in list_items:
        if item[date_name]:
            item[date_name] = item[date_name][:4]
    return list_items


def sort(credits_people, date):
        less = []
        equal = []
        greater = []
        if len(credits_people) > 1:
            for credit in credits_people:
                if credit[date]:
                    pivot = int(credit[date][:4])
                    break
            for x in credits_people:
                if x[date]:
                    if int(x[date][:4]) < pivot:
                        less.append(x)
                    if int(x[date][:4]) == pivot:
                        equal.append(x)
                    if int(x[date][:4]) > pivot:
                        greater.append(x)
            return sort(less, date) + equal + sort(greater, date)
        else:
            return credits_people


# Function whose goal is to find all the department occupied by an actor for a movie or tv show
def get_departments(all_values):
    departments = ['Acting']
    exist = False
    for item in all_values:
        for department in departments:
            if item['department'] == department:
                exist = True
        if not exist:
            departments.append(item['department'])
        exist = False
    return departments
