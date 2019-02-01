from bs4 import BeautifulSoup
import requests
from .models import Member, Topic, Problem


def get_list_solved_problem(user):
    profile_url = "https://www.spoj.com/PTIT/users/{}/".format(user.username)
    r = requests.get(profile_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    done_list = soup.find_all('table')[1]
    res = []
    for ele in done_list.find_all('td'):
        prob_code = ele.find('a').text.strip()
        if len(prob_code) > 0:
            res.append(prob_code)
    return res


def get_list_unsolved_problem(user):
    profile_url = "https://www.spoj.com/PTIT/users/{}/".format(user.username)
    r = requests.get(profile_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    done_list = soup.find_all('table')[2]
    res = []
    for ele in done_list.find_all('td'):
        prob_code = ele.find('a').text.strip()
        if len(prob_code) > 0:
            res.append(prob_code)
    return res


def get_list_topic():
    r = requests.get('https://www.spoj.com/PTIT/')
    soup = BeautifulSoup(r.text, 'html.parser')
    done_list = soup.find_all('ul')[1].find('div').find_all('a')
    res = []
    for ele in done_list:
        res.append(Topic(name=ele.text.strip(), url=ele['href'].strip()))
    return res


def get_list_problem_in_topic(topic):
    r = requests.get(topic.url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        num_page = 0
        done_list = soup.find_all('table')[3].find_all('tr')[1:]
        for e in soup.find_all('table')[2].find_all('td'):
            if str.isdigit(e.text.strip()):
                num_page = max(int(e.text.strip()), num_page)
        res = []
        for ele in done_list:
            sub_ele = ele.find_all('a')[:3]
            url_prob = sub_ele[0]['href'].strip()
            prob_code = sub_ele[1].text.strip()
            solved_num = sub_ele[2].text.strip()
            res.append(Problem(code=prob_code, score=float(80/(40+solved_num))))
        index = 50
        for i in range(1, num_page):
            tmp_url = topic.url + "/sort=0,start={}".format(index)
            r = requests.get(tmp_url)
            soup = BeautifulSoup(r.text, 'html.parser')
            done_list = soup.find_all('table')[3].find_all('tr')[1:]
            for ele in done_list:
                sub_ele = ele.find_all('a')[:3]
                url_prob = sub_ele[0]['href'].strip()
                prob_code = sub_ele[1].text.strip()
                solved_num = sub_ele[2].text.strip()
                res.append(Problem(code=prob_code, score=float(80/(40+solved_num))))
            index += 50
        return res
    except:
        done_list = soup.find_all('table')[2].find_all('tr')[1:]
        res = []
        for ele in done_list:
            sub_ele = ele.find_all('a')[:3]
            url_prob = sub_ele[0]['href'].strip()
            prob_code = sub_ele[1].text.strip()
            solved_num = sub_ele[2].text.strip()
            res.append(Problem(code=prob_code, score=float(80/(40+solved_num))))
        return res
    
def num_solved_each_problem(lst_probs, lst_mems):
    final_res = {}
    lst_set_solved = []
    for mem in lst_mems:
        lst_set_solved.append(mem.get_set_solved())
    for prob in lst_probs:
        prob_code = prob.code
        final_res[prob_code] = 0
        for s in lst_set_solved:
            if prob_code in s:
                final_res[prob_code] += 1
    return final_res

def update_members(lst_members, condition=None):
    for mem in lst_members:
        if condition is not None:
            if not condition(mem):
                continue
        username = mem.username
        lst_solved = get_list_solved_problem(mem)
        str_res = ""
        for ele in lst_solved:
            str_res = str_res + ele + " "
        mem.num_solved = len(lst_solved)
        mem.lst_solved = str_res
        mem.save()
    
def convert_dict(input_dict, member, prefix_url = "https://www.spoj.com/PTIT/problems/", reverse=False):
    if prefix_url[-1] != '/':
        prefix_url += '/'
    reference_set = member.get_set_solved()
    res = []
    lst_keys = sorted(input_dict, key=input_dict.get, reverse=reverse)
    for code in lst_keys:
        if code in reference_set:
            tmp = (code, "{}{}/".format(prefix_url, code), input_dict[code], "1")
        else:
            tmp = (code, "{}{}/".format(prefix_url, code), input_dict[code], "0")
        res.append(tmp)
    return res

def calculate_score_members(lst_mems):
    for mem in lst_mems:
        set_solved = mem.get_set_solved()
        total_score = 0
        for prob_code in set_solved:
            try:
                prob_obj = Problem.objects.get(code=prob_code)
                total_score += prob_obj.score
            except Exception as e:
                print(e)
                print(prob_code, len(prob_code), mem)
        mem.score = total_score
        mem.save()

def get_lst_str_progress(lst_mems):
    res = []
    for mem in lst_mems:
        prog = round(mem.num_solved*100/mem.target, 2)
        if mem.num_solved >= mem.target:
            print(mem)
            res.append("DONE")
        else:
            res.append(str(prog) + "%")
    return res

def get_lst_str_score(lst_mems):
    res = []
    for mem in lst_mems:
        prog = round(mem.score, 2)
        res.append(str(prog))
    return res

def get_lst_str_rank_delta(lst_mems):
    res = []
    for idx, mem in enumerate(lst_mems):
        res.append(mem.lastrank-idx-1)
    return res