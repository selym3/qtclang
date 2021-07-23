#include <iostream>
#include "include/hello.hpp"
#include "include/world.hpp"
#include "include/sub/test.hpp"

int main(void)
{
    hello();
    world();
    test();
    return 0;
}