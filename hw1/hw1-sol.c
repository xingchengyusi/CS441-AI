#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int people;
int relationship[100][100];

int input(void);
int compute_score(int * table);
int hgidentify(int a, int b, int half);
void print(int* table, int score);
int* create_table(int size);
int* exchange(int* table);
int* deepcopy(int* table);

static void shuffle(int* table, int size) {
  if (size > 1) {
    int j, t;
    for (int i = 0; i < size -1; i++) {
      j = i + rand() / (RAND_MAX / (size - i) + 1);
      t = table[j];
      table[j] = table[i];
      table[i] = t;
    }
  }
}

// simulated annealing
int simulated_annealing();

int main() {
  // Input data
  if(!input()) {
    printf("Input Error");
    return -1;
  }

  // basic arg
  srand((unsigned)time(0));
  int* table = create_table(people);
  shuffle(table, people);
  int score = simulated_annealing(table);
  print(table, score);

  return 0;
}

/**
 * algorithms
 * 1. simulated annealing
 */
int simulated_annealing(int* table) {
  // arg
  int sa_temp = people^2;
  double sa_r = 0.995;
  // initial
  time_t start;
  int score = -9999;
  int newscore = 0;

  // begin
  while ( - start <= 60) {
    sa_temp *= sa_r;
    int* newtable = exchange(table);
    newscore = compute_score(newtable);
    if ((newscore > score) || exp((newscore - score) / sa_temp) > (rand() / RAND_MAX))
      table = newtable;
    
    // if (sa_temp < 0.0000000001)
      // break;
  }
  return score;
}

/**
 * Normal function part
 */
int input(void) {
  scanf("%d\n", &people);

  for (int i = 0; i < people; i++) {
    for (int j = 0; j < people -1; j++)
      scanf("%d ", &relationship[i][j]);
    scanf("%d\n", &relationship[i][people-1]);
  }

  return 1;
}

int compute_score(int * table) {
  int score = 0;
  int half = people /2;

  for (int i = 0; i < half; i++) {
    score = score + relationship[table[i]][table[i+half]] + relationship[table[i+half]][table[i]];
    score += 2* hgidentify(table[i], table[i+half], half);

    if (i != half -1) {
      score += hgidentify(table[i], table[i+1], half);
      score += hgidentify(table[i+half], table[i+1+half], half);
      score = score + relationship[table[i]][table[i+1]] + relationship[table[i+1]][table[i]];
      score = score + relationship[table[i+half]][table[i+1+half]] + relationship[table[i+half+1]][table[i+half]];
    }
  }

  return score;
}

int hgidentify(int a, int b, int half) {
  if (a < 0 || b < 0 || a >= people || b >= people){
    printf("hg value error");
    exit(-1);
  }

  return ((a < half && b >= half) || (b < half && a >= half)) ? 1 : 0;
}

void print(int* table, int score) {
  // command line print
  printf("%d\n", score);
  for (int i = 0; i < people; i++)
    printf("%d %d\n", table[i], i+1);

  // file print
}

int* create_table(int size) {
  int table[size];
  for(int i = 0; i < size; i++)
    table[i] = i;
  return table;
}

int* exchange(int* table) {
  int a = rand() % people;
  int b = rand() % people;
  int* newtable = deepcopy(table);
  // exchange a and b
  int newa = newtable[a];
  newtable[a] = newtable[b];
  newtable[b] = newa;
  return newtable;
}

int* deepcopy(int* table) {
  int num = len(table);
  int* newtable[num];
  for (int i = 0; i < num; i++)
    newtable[i] = table[i];

  return newtable;
}