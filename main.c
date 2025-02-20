#include <stdio.h>
#include <ctype.h>

#define EXPR_SIZE 1024

int num_stack[EXPR_SIZE];
int op_stack[EXPR_SIZE];

int num_top = -1;
int op_top = -1;

int priority(char op)
{
   if (op == '+' || op == '-')
   {
      return 1;
   }
   if (op == '*' || op == '/')
   {
      return 2;
   }

   return 0;
}

void apply_op()
{
   if (num_top < 1 || op_top < 0)
   {
      return;
   }

   int b = num_stack[num_top];
   num_top--;

   int a = num_stack[num_top];
   num_top--;

   char op = op_stack[op_top];
   op_top--;

   switch (op)
   {
      case '+':
      {
         num_top++;
         num_stack[num_top] = a + b;

         break;
      }
      case '-':
      {
         num_top++;
         num_stack[num_top] = a - b;

         break;
      }
      case '*':
      {
         num_top++;
         num_stack[num_top] = a * b;

         break;
      }
      case '/':
      {
         num_top++;
         num_stack[num_top] = a / b;

         break;
      }
   }
}

int parser (const char *expr)
{
   int num = 0;

   while (*expr)
   {
      if (isspace(*expr))
      {
         expr++;
         continue;
      }
      if (isdigit(*expr))
      {
         num = 0;

         while (isdigit(*expr))
         {
            num = num * 10 + (*expr - '0');
            expr++;
         }

         num_top++;
         num_stack[num_top] = num;
         expr--;
      }
      else if (*expr == '(')
      {
         op_top++;
         op_stack[op_top] = *expr;
      }
      else if (*expr == ')')
      {
         while (op_top >= 0 && op_stack[op_top] != ('('))
         {
            apply_op();
         }

         op_top--;
      }
      else if (*expr == '+' || *expr == '-' || *expr == '*' || *expr == '/')
      {
         while (op_top >= 0  && priority(op_stack[op_top]) >= priority(*expr))
         {
            apply_op();
         }

         op_top++;
         op_stack[op_top] = *expr;
      }

      expr++;
   }

   while (op_top >= 0)
   {
      apply_op();
   }

   return num_stack[num_top];
}


int main()
{
   char expr[EXPR_SIZE];
   fgets(expr, EXPR_SIZE, stdin);
   printf("%d", parser(expr));
   return 0;
}