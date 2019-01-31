from django.db import models
import numpy as np
import math
# Create your models here.
class Member(models.Model):
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    grade = models.CharField(max_length=5)
    num_solved = models.IntegerField()
    lst_solved = models.CharField(max_length=15000)
    lastrank = models.IntegerField(default=1)
    
    def parse_lst_solved(self, col_per_row=4):
        lst_str_solved = self.lst_solved.__str__().split(' ')
        return Member.reshape_list(lst_str_solved, col_per_row=col_per_row)

    def get_set_solved(self):
        return set(self.lst_solved.__str__().split(' '))

    def get_list_exclude(self, other):
        self_set_str_solved = set(self.lst_solved.__str__().split(' '))
        other_set_str_solved = set(other.lst_solved.__str__().split(' '))
        self_res = []
        other_res = []
        for ele in self_set_str_solved:
            if ele not in other_set_str_solved:
                self_res.append(ele)
        for ele in other_set_str_solved:
            if ele not in self_set_str_solved:
                other_res.append(ele)
        return (self_res, other_res)

    @staticmethod
    def reshape_list(lst_str_solved, col_per_row=3):
        num_row = math.ceil(len(lst_str_solved)/col_per_row)
        res = []
        c_id = 0
        for i in range(num_row):
            tmp = []
            for j in range(col_per_row):
                tmp.append((lst_str_solved[c_id], "https://www.spoj.com/PTIT/problems/{}/".format(lst_str_solved[c_id])))
                if c_id == len(lst_str_solved)-1 :
                    break
                c_id += 1
            res.append(tmp)
        return res
    
    def __eq__(self, other):
        if self.username == other.username:
            return True
        return False
    
    def __gt__(self, other):
        if self.num_solved != other.num_solved:
            return self.num_solved > other.num_solved
        return self.username > other.username
    
    def __lt__(self, other):
        if self.num_solved != other.num_solved:
            return self.num_solved < other.num_solved
        return self.username < other.username


class Topic(models.Model):
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "Topic[name:{} - url:{}]".format(self.name, self.url)

    def get_arr_name_columns(self):
        return ["name", "url"]

    def get_name_columns(self):
        arr = self.get_arr_name_columns()
        rs = ""
        for i in range(len(arr)):
            rs += arr[i]
            if i != len(arr)-1:
                rs += ", "
        return rs
    
    def get_refer(self):
        return "%s, %s"

    def get_value(self):
        return (self.name, self.url)


class Problem(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    score = models.FloatField()
