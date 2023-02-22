//test.c
#include <ncurses.h>
#include <locale.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define UP 1
#define DOWN -1
#define LEFT 2
#define RIGHT -2


struct Snake
{
   int hang;
   int lie;
   struct Snake *next;
};

struct Snake *head = NULL;
struct Snake *tail = NULL;
int key;
int dir;

struct Snake food;

void initFood()
{
   int x = rand()%19+1;
   int y = rand()%19+1;

   food.hang = x;
   food.lie = y;

}

int hasSnakeNode(int i, int j)
{
   struct Snake *p;
   p = head;
   while(p != NULL){
      
      if(i == p->hang && j == p->lie){
      return 1;
      }
      p = p->next;
   }

   return 0;

}

int hasFood(int i, int j)
{
   if(food.hang == i && food.lie == j){
   return 1;
   }

   return 0;

}

void initNcurse()
{
   initscr();
   keypad(stdscr,1);
   noecho();
}

int gamePic(int len)
{
   int hang;
   int lie;

   move(0,0);

   for(hang=0; hang<len; hang++){
      if(hang==0 || hang==len-1){
         for(lie=0; lie<len; lie++){
            printw("**");
         }
      }
      else{
         for(lie=0; lie<len; lie++){
            if(lie==0 || lie==len-1){
               printw("**");
            }
            else if(hasSnakeNode(hang, lie)){
               printw("[]");
            }
            else if(hasFood(hang, lie)){
               printw("##");
            }
            else{
               printw("  ");
            }
         }
      }
      printw("\n");
   }
   printw("by ztc,key=%d\n", key);

}

void addNode()
{
   struct Snake *new = (struct Snake *)malloc(sizeof(struct Snake));
   
   new->next = NULL;

   switch(dir){
      case UP:
         new->hang = tail->hang-1;
         new->lie = tail->lie;
         break;
      case DOWN:
         new->hang = tail->hang+1;
         new->lie = tail->lie;
         break;
      case LEFT:
         new->hang = tail->hang;
         new->lie = tail->lie-1;
         break;
      case RIGHT:
         new->hang = tail->hang;
         new->lie = tail->lie+1;
         break;
   }

   tail->next = new;
   tail = new;

}

void initSnake()
{

   struct Snake *p;
   
   dir = RIGHT;

   while(head!=NULL){
      p = head;
      head = head->next;
      free(p);
   }

   initFood();
   head = (struct Snake *)malloc(sizeof(struct Snake));
   head->hang = 2;
   head->lie = 2;
   head->next = NULL;

   tail = head;

   addNode();
   addNode();
   addNode();
}

void deleNode()
{
   struct Snake *p;
   p = head;
   head = head->next;

   free(p);
}

int ifSnakeDie()
{
   struct Snake *p;
   p = head;

   if(tail->hang==0 || tail->lie==0 || tail->hang==20 || tail->lie==20){
      return 1;
   }
   while(p->next!=NULL){
      if(p->hang == tail->hang && p->lie == tail->lie){
         return 1;
      }
      p = p->next;
   }
   return 0;
}

void moveSnake()
{

   addNode();
   if(hasFood(tail->hang, tail->lie)){
      initFood();
   }
   else{
      deleNode();
   }
   if(ifSnakeDie()){
      initSnake();
   }

}

void* refreshJiemian()
{
   while(1){
      moveSnake();
      gamePic(20);
      refresh();
      usleep(100000);
   }
}

void turn(int direction)
{
   if(abs(dir) != abs(direction)){
      dir = direction;
   }
}


void* changeDir()
{

   while(1){
      key = getch();
      switch(key){
         case KEY_DOWN:
            turn(DOWN);
            break;
         case KEY_UP:
            turn(UP);
            break;
         case KEY_LEFT:
            turn(LEFT);
            break;
         case KEY_RIGHT:
            turn(RIGHT);
            break;
      }
   }
}

int main()
{

   pthread_t t1;
   pthread_t t2;

   initNcurse();
   initSnake();

   gamePic(20);

   pthread_create(&t1, NULL, refreshJiemian, NULL);
   pthread_create(&t2, NULL, changeDir, NULL);

   while(1);

   getch();
   endwin();
   return 0;

}
