#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define EXPR_SIZE 1024

typedef union {
    long l;
    double d;
} ld_num;

ld_num num_stack[EXPR_SIZE];
char op_stack[EXPR_SIZE];

long num_top = -1;
long op_top = -1;

int float_mode = 0;

long priority(char op)
{
    if (op == '+' || op == '-') {
        return 1;
    }
    if (op == '*' || op == '/') {
        return 2;
    }

    return 0;
}

void apply_op()
{
    if (num_top < 1 || op_top < 0) {
        return;
    }

    ld_num b = num_stack[num_top];
    num_top--;

    ld_num a = num_stack[num_top];
    num_top--;

    char op = op_stack[op_top];
    op_top--;

    ld_num num;

    switch (op) {
    case '+': {
        num_top++;
        if (float_mode) {
            num.d = a.d + b.d;
            num_stack[num_top] = num;
        } else {
            num.l = a.l + b.l;
            num_stack[num_top] = num;
        }

        break;
    }
    case '-': {
        num_top++;
        if (float_mode) {
            num.d = a.d - b.d;
            num_stack[num_top] = num;
        } else {
            num.l = a.l - b.l;
            num_stack[num_top] = num;
        }

        break;
    }
    case '*': {
        num_top++;
        if (float_mode) {
            num.d = a.d * b.d;
            num_stack[num_top] = num;
        } else {
            num.l = a.l * b.l;
            num_stack[num_top] = num;
        }

        break;
    }
    case '/': {
        num_top++;
        if (float_mode) {
            if (fabs(b.d) < 0.0001) {
                exit(3);
            }

            num.d = a.d / b.d;
            num_stack[num_top] = num;
        } else {
            if (b.l == 0) {
                exit(3);
            }

            num.l = a.l / b.l;
            num_stack[num_top] = num;
        }

        break;
    }
    }
}

ld_num parser(const char* expr)
{

    ld_num num;
    num.l = 1;
    long expecting_number = 1;
    long open_parens = 0;

    while (*expr) {
        if (isspace(*expr)) {
            expr++;
            continue;
        }
        if (isdigit(*expr)) {
            if (float_mode) {
                num.d = 0;

                while (isdigit(*expr)) {
                    num.d = num.d * 10 + (*expr - '0');
                    expr++;
                }
            } else {
                num.l = 0;

                while (isdigit(*expr)) {
                    num.l = num.l * 10 + (*expr - '0');
                    expr++;
                }
            }

            num_top++;
            num_stack[num_top] = num;
            expr--;
            expecting_number = 0;
        } else if (*expr == '(') {
            if (!expecting_number) {
                exit(2);
            }

            op_top++;
            op_stack[op_top] = *expr;
            open_parens++;
        } else if (*expr == ')') {
            if (expecting_number) {
                exit(2);
            }

            while (op_top >= 0 && op_stack[op_top] != ('(')) {
                apply_op();
            }

            op_top--;
            open_parens--;
        } else if (*expr == '+' || *expr == '-' || *expr == '*' || *expr == '/') {
            if (expecting_number) {
                exit(2);
            }

            while (op_top >= 0 && priority(op_stack[op_top]) >= priority(*expr)) {
                apply_op();
            }

            op_top++;
            op_stack[op_top] = *expr;
            expecting_number = 1;
        } else {
            exit(1);
        }

        expr++;
    }

    if (expecting_number == 1 || open_parens != 0) {
        exit(1);
    }

    while (op_top >= 0) {
        apply_op();
    }

    return num_stack[num_top];
}

#ifndef GTEST
int main(int argc, char* argv[])
{
    char expr[EXPR_SIZE];
    long ch = 0;
    long pos = 0;

    if ((argc > 1) && (strcmp(argv[1], "--float") == 0)) {
        float_mode = 1;
    }

    while ((ch = fgetc(stdin)) != EOF) {
        expr[pos] = (char)ch;
        pos++;
    }

    if (feof(stdin) != 1) {
        exit(10);
    } else {
        expr[pos] = '\0';
    }

    ld_num result = parser(expr);

    if (float_mode) {
        printf("%.4f", result.d);
    } else {
        printf("%ld", result.l);
    }

    return 0;
}
#endif
