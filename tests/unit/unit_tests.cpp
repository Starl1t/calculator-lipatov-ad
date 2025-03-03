#include <gtest/gtest.h>

extern "C" {
#include "../../src/main.c"
}

TEST(PriorityTest, HandlesBasicOperators)
{
    EXPECT_EQ(priority('+'), 1);
    EXPECT_EQ(priority('-'), 1);
    EXPECT_EQ(priority('*'), 2);
    EXPECT_EQ(priority('/'), 2);
    EXPECT_EQ(priority('('), 0);
}

TEST(ApplyOpTest, HandlesIntDivide)
{
    num_stack[0].l = 7;
    num_stack[1].l = 2;
    num_top = 1;
    op_stack[0] = '/';
    op_top = 0;
    apply_op();
    EXPECT_EQ(num_stack[0].l, 3);
}

TEST(ApplyOpTest, HandlesFloatDivide)
{
    float_mode = 1;
    num_stack[0].d = 7;
    num_stack[1].d = 2;
    num_top = 1;
    op_stack[0] = '/';
    op_top = 0;
    apply_op();
    EXPECT_EQ(num_stack[0].d, 3.5);
}

TEST(ParserTest, HandlesExpression)
{
    const char* expr = "3 + 2*(6/2)";
    ld_num result = parser(expr);
    EXPECT_EQ(result.l, 9);
}
