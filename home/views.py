from django.shortcuts import render
from django.http import HttpResponse
from .models import Member, Problem
from .algorithms import update_members, convert_dict, num_solved_each_problem
from .algorithms import calculate_score_members, get_lst_str_progress
from .algorithms import get_lst_str_score, get_lst_str_rank_delta
# Create your views here.

def index(request):
    Data = {}
    if request.method == "POST":
        data_dict = request.POST.dict()
        mem_a_id = int(data_dict['select_a'])
        mem_b_id = int(data_dict['select_b'])
        # x.readlines
    else:
        mem_a_id = 2
        mem_b_id = 2
    lst_mem = Member.objects.all()
    mem_a = Member.objects.get(id=mem_a_id)
    mem_b = Member.objects.get(id=mem_b_id)
    if mem_a_id != mem_b_id:
        mem_a = Member.objects.get(id=mem_a_id)
        mem_b = Member.objects.get(id=mem_b_id)
    else:
        mem_a = mem_b = Member.objects.get(id=mem_a_id)
    Data['mem_a'] = mem_a
    Data['mem_b'] = mem_b
    lst_unsolved_a, lst_unsolved_b = mem_a.get_list_exclude(mem_b)
    lst_2d_unsolved_a = Member.reshape_list(lst_unsolved_a, col_per_row=4)
    lst_2d_unsolved_b = Member.reshape_list(lst_unsolved_b, col_per_row=4)
    Data['lst_solved_a'] = lst_2d_unsolved_a
    Data['lst_solved_b'] = lst_2d_unsolved_b
    Data['unsolved_a_num'] = len(lst_unsolved_a)
    Data['unsolved_b_num'] = len(lst_unsolved_b)
    Data['lst_members'] = lst_mem
    return render(request, 'pages/home.html', Data)

def statistics(request):
    Data = {}
    mem_id = 2
    reverse_flag_score = True
    reverse_flag_racer = True
    if request.method == "POST":
        mem_id = int(request.POST.dict()['selected_mem'])
        
        post_flag_score = request.POST.dict()['select_order_score']
        post_flag_racer = request.POST.dict()['select_order_racer']
        if post_flag_score == "1":
            reverse_flag_score = True
        if post_flag_score == "2":
            reverse_flag_score = False
        if post_flag_racer == "1":
            reverse_flag_racer = True
        if post_flag_racer == "2":
            reverse_flag_racer = False
    selected_mem = Member.objects.get(id=mem_id)
    
    lst_probs = Problem.objects.all()
    dict_probs = {}
    for prob in lst_probs:
        dict_probs[prob.code] = prob.score

    data = convert_dict(num_solved_each_problem(lst_probs, Member.objects.all()), selected_mem, reverse=reverse_flag_racer)
    Data['lst_racer'] = data
    Data['lst_score'] = convert_dict(dict_probs, selected_mem, reverse=reverse_flag_score)
    Data['lst_members'] = Member.objects.all()
    Data['selected_mem'] = selected_mem
    return render(request, 'pages/statistics.html', Data)


def ranking(request):
    Data = {}
    lst_members = Member.objects.all()
    calculate_score_members(lst_members)
    lst_members = sorted(lst_members, reverse=True)
    Data['lst_mem'] = lst_members
    Data['lst_progress'] = get_lst_str_progress(lst_members)
    Data['lst_score'] = get_lst_str_score(lst_members)
    Data['lst_delta_rank'] = get_lst_str_rank_delta(lst_members)
    return render(request, 'pages/ranking.html', Data)

def update_database_all_member(request):
    lst_members = Member.objects.all()
    update_members(lst_members)
    return HttpResponse(content="OK")
