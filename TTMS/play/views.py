import datetime
import json
import os

import jsonlines
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from surprise import Reader, Dataset, KNNBaseline

from TTMS.settings import IMG_PATH, MOVIE_PATH
from account.models import Account
from order.models import Order
from play.models import Play
from schedule.models import Schedule
from system.views import is_login, is_auth
from type.models import Type


@is_login
def list(request):
    plays = Play.objects.all()
    PageObj = Paginator(plays, per_page=5)
    page = request.GET.get('page', 1)
    account_id = request.session.get('user_id', None)
    account = get_object_or_404(Account, id=account_id)
    likes = account.likes.all()
    like_ids = []
    for like in likes:
        like_ids.append(like.id)
    #     print(item.id)
    # print(if 2 in likes)
    # for i in list(likes):
    #     print(likes)
    try:
        playsPageObj = PageObj.page(page)
        plays = playsPageObj.object_list
    except:
        playsPageObj = PageObj.page(1)
        plays = playsPageObj.object_list
        # playsPageObj=None
    return render(request, 'play/list.html', context={
        'plays': plays,
        'playsPageObj': playsPageObj,
        'likes': like_ids
    })

@is_login
@is_auth
def add(request):
    types = Type.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        play_time = request.POST['play_time']
        length = request.POST['length']
        director = request.POST['director']
        actors = request.POST['actors']
        area = request.POST['area']
        types = request.POST.getlist('types')
        desc = request.POST['desc']
        print(type(play_time),'--------')
        play = Play(name=name, play_time=play_time, length=length, director=director, actors=actors, area=area,
                    desc=desc)
        print(type(play.play_time),'--------')

        # play.types.create

        # play.save()

        # for type in types:
        #     play.types.add(int(type))
        # play.save()

        return redirect(reverse('play_list'))
    return render(request, 'play/add.html', context={
        'types': types
    })

@is_login
def init_data(request):

    with open(MOVIE_PATH) as f:
        for line in jsonlines.Reader(f):
            name = line['name']
            score = float(line['score']) if line['score'] else 0.0
            director = ','.join(line['director'])
            actor = ','.join(line['actor'])
            area = line['area']
            length = line['length']
            # print(length)
            length = int(length.split('分钟')[0]) if length else 0
            brief = line['brief']
            img = IMG_PATH + name + '.jpg'
            release_date = line['release_date'].split('(')[0]
            release_date = datetime.date(*map(int, release_date.split('-')))
            types = line['type']

            if not Play.objects.filter(name=name):

                play = Play(name=name, play_time=release_date, length=length, desc=brief,
                            director=director, actors=actor, area=area, img=img, score=score)
                play.save()
                for type_name in types:
                    # print(type_name)
                    play_type = Type.objects.filter(name=type_name).first()
                    # print(play_type)
                    if play_type:
                        play.types.add(play_type.id)
                    else:
                        type_new = Type(name=type_name)
                        type_new.save()
                        play.types.add(type_new.id)
                play.save()
    return redirect(reverse('play_list'))

@is_login
@is_auth
def delete(request, id):
    play = get_object_or_404(Play, id=id)
    play.status = 0
    play.save()
    schedules = play.schedule_set.all()
    for schedule in schedules:
        schedule.status = 0
        schedule.save()

    orders = Order.objects.filter(schedule__play=play).all()
    for order in orders:
        order.status = -1
        order.save()

    return redirect(reverse('play_list'))


def search(request,):
    name = request.GET['search']
    plays = Play.objects.filter(name__icontains=name).all()
    PageObj = Paginator(plays, per_page=5)
    page = request.GET.get('page', 1)
    account_id = request.session.get('user_id', None)
    account = get_object_or_404(Account, id=account_id)
    likes = account.likes.all()
    like_ids = []
    for like in likes:
        like_ids.append(like.id)
    try:
        playsPageObj = PageObj.page(page)
        plays = playsPageObj.object_list
    except:
        playsPageObj = PageObj.page(1)
        plays = playsPageObj.object_list
        # playsPageObj=None
    return render(request, 'play/search.html', context={
        'plays': plays,
        'playsPageObj': playsPageObj,
        'likes': like_ids
    })


@is_login
def up(request, id):
    play = get_object_or_404(Play, id=id)
    play.status = 1
    play.save()
    # schedules = play.schedule_set.all()
    # for schedule in schedules:
    #     schedule.status = 1
    #     schedule.save()

    return redirect(reverse('play_list'))


@is_login
@is_auth
def edit(request, id):
    play = get_object_or_404(Play, id=id)

    types = Type.objects.all()
    if request.method == 'POST':
        play.name = request.POST['name']
        play.play_time = request.POST['play_time']
        play.length = request.POST['length']
        play.director = request.POST['director']
        play.actors = request.POST['actors']
        play.area = request.POST['area']
        types = request.POST.getlist('types')
        play.desc = request.POST['desc']

        # play.update(name=name,play_time=play_time,length=length,director=director,actors=actors,area=area,desc=desc)
        play.save()
        play.types.clear()
        for type in types:
            play.types.add(int(type))
        play.save()

        return redirect(reverse('play_list'))

    return render(request, 'play/edit.html', context={
        'play': play,
        'types': types
    })


def like(request, id):
    try:
        account_id = request.session.get('user_id', None)
        account = get_object_or_404(Account, id=account_id)
        account.likes.add(int(id))
        account.save()
        messages.info(request, "加入我喜欢的成功！")
    except Exception as e:
        messages.error(request, "加入我喜欢的失败！")

    return redirect(reverse('play_list'))

def like_cancel(request, id):
    try:
        account_id = request.session.get('user_id', None)
        account = get_object_or_404(Account, id=account_id)
        account.likes.remove(int(id))
        account.save()
        messages.info(request, "取消我喜欢的成功！")
    except Exception as e:
        messages.error(request, "取消我喜欢的失败！")

    return redirect(reverse('play_list'))

def get_data(request):
    data = {
        'name': 'jkhj'
    }
    if request.is_ajax():
        print('111')

        return JsonResponse(data)
    return JsonResponse(data)

# def make_data(request):
#     # dir_path = os.path.dirname(os.path.abspath(__file__))
#     # print(dir_path)
#     # file_path = dir_path + '/home/kiosk/PycharmProjects/Project/TTMS/recmmond_data.txt'
#     # print(file_path)
#     file_path = '/home/kiosk/PycharmProjects/Project/TTMS/recmmond_data.txt'
#
#     reader = Reader(line_format='user item rating', sep='\t')
#     data = Dataset.load_from_file(file_path, reader=reader)
#
#     trainset = data.build_full_trainset()
#     sim_options = {'name': 'pearson_baseline', 'user_based': False}
#
#     algo = KNNBaseline(sim_options=sim_options)
#     algo.fit(trainset)
#
#     # cur_playlist_name = list(name_id_dict.keys())[29]
#     # print(cur_playlist_name, '===========')
#     cur_play_id = '7'
#     cur_play_inner_id = algo.trainset.to_inner_uid(cur_play_id)
#     cur_play_neighbors = algo.get_neighbors(cur_play_inner_id, k=1)
#     # print(cur_play_neighbors)
#     cur_play_neighbors = (algo.trainset.to_raw_uid(inner_id) for inner_id in cur_play_neighbors)
#
#     # cur_play_neighbors = (id_name_dict[raw_id] for raw_id in cur_play_neighbors)
#
#     # print("和歌单 《", cur_playlist_name, "》 最接近的10个歌单为：")
#     for playlist_name in cur_play_neighbors:
#         print(playlist_name, '----------')
#     return JsonResponse(data)
#
#
#     # cur_song_id = list(song_id_name_dic.keys())[0]
#     # print(cur_song_id)
#     # cur_song_name = song_id_name_dic[cur_song_id]
#     # print(cur_song_name)
#     # cur_song_inner_id = algo.trainset.to_inner_iid(cur_song_id)
#     # print(cur_song_inner_id)
#     # user_id = algo.trainset.to_inner_uid('423245641')
#     # song_id = algo.trainset.to_inner_iid('414691355')
#     # user_rating = trainset.ur[user_id]
#     # print(user_rating)
#     # items = map(lambda x:x[0], user_rating)
#     # for song in items:
#     # print(algo.predict('423245641', '414691355', r_ui=80))
