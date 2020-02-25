import os

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from TTMS.settings import BASE_DIR
from account.models import Account
from order.models import Order
from play.models import Play
from schedule.models import Schedule
from seat.models import Seat
from studio.models import Studio
from system.views import is_auth, is_login


@is_login
@is_auth
def sale(request, id=None):
    # find_play()
    file = os.path.join(BASE_DIR, os.path.dirname(os.path.abspath(__file__)), 'recmmond_play_result.txt')
    with open(file) as f:
        plays_id = f.read()
    plays_id = list(map(int, plays_id.split(',')))
    print(plays_id)
    plays = Play.objects.filter(id__in=plays_id).all()
    play_id = id if id else plays[0].id
    print(play_id)
    play = get_object_or_404(Play, id=play_id)
    print(play.name)
    # schedules = Schedule.objects.all()
    schedules = Schedule.objects.filter(play_id__in=plays_id).all().order_by('-show_time')
    print(schedules)
    print('=======')
    # return render(request, 'play/test.html')
    return render(request, 'ticket/sale.html', context={
        'plays': plays,
        'play': play,
        'schedules': schedules
    })


def seat(request, id):
    schedule = get_object_or_404(Schedule, id=id)
    studio = get_object_or_404(Studio, id=schedule.studio_id)

    seats = Seat.objects.filter(studio=studio).all()
    seats_list = list(seats)
    # print([i.id for i in seats_list],'------------------********')
    # rows = [i for i in range(1, studio.seat_rows + 1)]
    # cols = [i for i in range(1, studio.seat_cols + 1)]
    # print(seats_list)
    seats = []
    for row in range(studio.seat_rows):
        seats_row = []
        for col in range(studio.seat_cols):
            seats_row.append(seats_list[row * studio.seat_cols + col])
        seats.append(seats_row)
    seat = get_object_or_404(Seat, id=id)
    # seat.ticket_set.filter(schedule)
    # print(seats,'--------')
    return render(request, 'ticket/seat.html', context={
        'schedule': schedule,
        'seats': seats
    })

def detail(request, id):

    play = get_object_or_404(Play, id=id)
    schedules = Schedule.objects.filter(play=play).order_by('-show_time')
    return render(request, 'ticket/detail.html', context={
        'play': play,
        'schedules': schedules
    })
@is_login
def buy(request, id):
    # print(request.path_info.split("/buy/")[0]+"/buy/",type(request.path_info),'------------')

    ids = request.GET['id_str']
    id_li = ids.split(" ")
    account_id = request.session.get('user_id', None)
    account = get_object_or_404(Account, id=account_id)
    schedule = get_object_or_404(Schedule, id=id)
    seats = [get_object_or_404(Seat, id=int(seat_id)) for seat_id in id_li]

    if request.method == 'POST':

        with transaction.atomic():
            save_id = transaction.savepoint()

            order = Order()
            money = len(seats) * schedule.ticket_money
            order.money = money
            order.schedule = schedule
            order.account = account

            order.save()

            for seat in seats:
                if seat.order_set.all():
                    if seat.order_set.filter(schedule=schedule):
                        # print('=-=---===========================')
                        transaction.savepoint_rollback(save_id)
                        # raise
                        # return JsonResponse({'res':5, 'errmsg':'错误'})
                        messages.info(request, "您选的座位已被购买，请重选！")
                        return redirect(reverse('ticket_seat', args=(schedule.id,)))

                # seat.status = True
                seat.save()


                schedule.ticket_counts -= 1
                schedule.save()
                order.seats.add(seat)
            order.save()
            schedule.save()

                # ticket = Ticket(schedule=schedule, seat=seat, order=order)
                # ticket.save()
            transaction.savepoint_commit(save_id)

            return render(request, 'ticket/ok.html')

    # order_time = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(tzinfo=pytz.timezone('UTC'))
    # print(order_time,'-----')
    # request.session['order_time'] = datetime.datetime.now()
    # request.session.set_expiry(60)
    return render(request, 'ticket/order.html', context={
        'schedule': schedule,
        'seats': seats,
        'ids': ids
        # 'order_time':order_time
    })




# 制作推荐电影的数据集，保存在recmmond_data.txt
def make_data(request):
    file = os.path.join(BASE_DIR, os.path.dirname(os.path.abspath(__file__)), 'recmmond_data.txt')
    recm_file = open(file, 'w')
    accounts = Account.objects.all()
    plays = Play.objects.all()

    for play in plays:
        play_accounts = play.account_set.all()
        play_accounts_id = [play_account.id for play_account in play_accounts]
        for account in accounts:
            line = str(account.id) + '\t' + str(play.id) + '\t'
            grade = 1
            if account.id in play_accounts_id:
                grade += 3
            order = Order.objects.filter(account=account, schedule__play=play).first()
            if order:
                grade += 6
            line += str(grade)
            recm_file.write(line + '\n')
    recm_file.close()

    return redirect(reverse('play_list'))


# 找到当前用户最近时间购买过的一部电影，将id保存在play_id.txt
def find_play(request):
    print('======')
    plays = Play.objects.filter(status=1).all().order_by('-score')
    plays_id = [play.id for play in plays]
    print(plays_id)
    account_id = request.session.get('user_id', None)
    account = get_object_or_404(Account, id=account_id)
    play_like = account.likes.last()
    order = account.order_set.all().order_by('-time').first()
    if play_like and play_like.id in plays_id:
        play_id = play_like.id
    elif order and order.schedule.status:
            play_id = order.schedule.play.id
    else:
        play_id = plays_id[0]
    print(play_id,'======')
    path = os.path.join(BASE_DIR, os.path.dirname(os.path.abspath(__file__)), 'play_id.txt')
    print(path)
    with open(path, 'w') as f:
        f.write(str(play_id))

