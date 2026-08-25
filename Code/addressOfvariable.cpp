#include <iostream>

using namespace std;

void foo(){
    int x = 36;
    std::cout << "Value foo: " << x << std::endl;
    std::cout << "Address foo: " << &x << std::endl;
    x = 36;
};

int main(){
    int a = 7;
    int *p = &a;
    std::cout << "Value: " << *p << std::endl;
    std::cout << "Address: " << &p << std::endl;
    std::cout << "Address: " << p << std::endl;

    return 0;
};