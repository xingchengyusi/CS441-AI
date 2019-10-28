# Dajun Gu
# CS441 Homework 1
# 10/21/2019

import random
import time
from copy import deepcopy
import math
import sys

def input(file_name) -> (int, list):
  with open(file_name+'.txt', 'r') as f:
    people_num = int(f.readline())
    person_like = []
    while len(person_like) < people_num:
      person_like.append([int(x) for x in f.readline().split(" ")])

  return (people_num, person_like)

class Table:
  def __init__(self, people_num = 0, person_like = [[]]):
    self.people_num = people_num
    self.score = -999
    self.person_like = person_like
    self.table_present = []
    self.start = time.time()

  # common function
  def hgidentify(self, a, b) -> bool:
    half = self.people_num /2
    return True if ((a < half and b >= half) or (a >= half and b < half-1)) else False

  def compute_score(self, target_table) -> int:
    score = 0
    half = int(self.people_num /2)
    for i in range(0, half):
      score = score + self.person_like[target_table[i]][target_table[i+half]] + self.person_like[target_table[i+half]][target_table[i]]
      score += 2 if self.hgidentify(target_table[i], target_table[i+half]) else 0
      if i != half-1:
        score += 1 if self.hgidentify(target_table[i], target_table[i+1]) else 0
        score += 1 if self.hgidentify(target_table[i+half], target_table[i+1+half]) else 0
        score = score + self.person_like[target_table[i]][target_table[i+1]] + self.person_like[target_table[i+1]][target_table[i]]
        score = score + self.person_like[target_table[i+half]][target_table[i+1+half]] + self.person_like[target_table[i+half+1]][target_table[i+half]]
    
    return score

  def print_table(self, file_name):
    # file output
    with open('hw1-sol' + file_name[-1] + '.txt', 'w+') as f:
      f.writelines(str(self.score) + '\n')
      for i in range(0, self.people_num):
        f.writelines(str(self.table_present[i]) + ' ' + str(i+1) + '\n')
    
    # command line output
    print(self.score)
    for i in range(0, self.people_num):
      print(str(self.table_present[i]) + ' ' + str(i+1))

  def analyres(self):
    # [0] is 100-91 and so on
    res = [0, 0, 0, 0]
    for i in range(0, 100):
      s.simulated_annealing()
      # print(self.score)
      if self.score > 90:
        res[0] += 1
      elif self.score > 80 and self.score <= 90:
        res[1] += 1
      elif self.score > 70 and self.score <= 80:
        res[2] += 1
      else:
        res[3] += 1

    print(res)

  # simulated annealing
  def sa_choosetemp(self) -> int:
    min = 999
    max = -999
    table = [x for x in range(0, self.people_num)]
    for i in range(0, 1000):
      random.shuffle(table)
      score = self.compute_score(table)
      if score > max:
        max = score
      if score < min:
        min = score

    # print(max, min, max-min, (max-min)*2)
    return (max - min) *2

  def sa_exchange(self) -> list:
    a = random.randint(0, self.people_num-1)
    b = random.randint(0, self.people_num-1)
    new_table = deepcopy(self.table_present)
    # exchange a and b
    newa = new_table[a]
    new_table[a] = new_table[b]
    new_table[b] = newa
    return new_table

  def sa_accept_score(self, newscore, sa_temp) -> bool:
    cha = newscore - self.score
    if cha >= 0 or math.exp(cha / sa_temp) > random.random():
      self.score = newscore
      return True
    else:
      return False

  def simulated_annealing(self):
    # argument
    sa_temp = self.sa_choosetemp()
    sa_r = 0.995
    # random set initial table
    self.table_present = [x for x in range(0, self.people_num)]
    random.shuffle(self.table_present)

    # loop until 60 seconds
    while (time.time() - self.start) <= 60:
      sa_temp *= sa_r
      newtable = self.sa_exchange()
      succ = self.sa_accept_score(self.compute_score(newtable), sa_temp)
      if succ == True:
        self.table_present = newtable
      # if sa_temp < 0.000001:
        # break

  # stochastic beam search
  def stochastic_beam(self):
    # initial
    k = 3
    # in this method, the score an table should be list.
    self.score = [-999 for x in range(k)]
    while len(self.table_present) < k:
      self.table_present.append([random.shuffle([x for x in range(0, self.people_num)])])

    # 

  # genetic algorithms
  def g_selection(self, tableset) -> list:
    a = random.choices(tableset, [self.compute_score(x) for x in tableset], k = 1)
    return a[0]

  def genetic(self):
    tableset = []
    newtableset = []
    k = 10
    for i in range(0, k):
      b = [x for x in range(0, self.people_num)]
      random.shuffle(b)
      # print(b)
      tableset.append(b)

    half = int(self.people_num/2)
    while (time.time() - self.start) <= 60:
      newtableset = []
      for j in range(0, k):
        x = self.g_selection(tableset)
        y = self.g_selection(tableset)
        res = random.randint(0, half)
        child = x[:res] + y[res:half] + x[half:res] + y[res:]
        newtableset.append(child)

      tableset = newtableset

    self.table_present = max(tableset, key=self.compute_score)
    self.score = self.compute_score(self.table_present)

if __name__ == "__main__":
  file_name = sys.argv[1]
  (people_num, person_like) = input(file_name)
  s = Table(people_num, person_like)
  # s.genetic()
  s.simulated_annealing()
  # s.analyres()
  s.print_table(file_name)
  pass