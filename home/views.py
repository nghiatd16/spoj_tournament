from django.shortcuts import render
from django.http import HttpResponse
from .models import Member, Problem
from .algorithms import update_members, convert_dict, num_solved_each_problem
# Create your views here.

def index(request):
    Data = {}
    if request.method == "POST":
        data_dict = request.POST.dict()
        mem_a_id = int(data_dict['select_a'])
        mem_b_id = int(data_dict['select_b'])
        # x.readlines
    else:
        mem_a_id = 1
        mem_b_id = 1
    lst_mem = Member.objects.all()
    # update_members(lst_mem)
    mem_a = Member.objects.get(id=mem_a_id)
    
    Data['mem_a'] = mem_a
    mem_b = Member.objects.get(id=mem_b_id)
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
    lst_probs = Problem.objects.all()
    dict_probs = {}
    for prob in lst_probs:
        dict_probs[prob.code] = prob.score
    data = convert_dict(num_solved_each_problem(lst_probs, Member.objects.all()), reverse=True)
    Data['lst_racer'] = data[:200]
    Data['lst_score'] = convert_dict(dict_probs, reverse=True)[:200]
    return render(request, 'pages/statistics.html', Data)