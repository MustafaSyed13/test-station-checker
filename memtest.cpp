// this will write numbers into memeory read them back and check if they match
#include <iostream> //like system.out.println
#include <vector> // this is like a arry list lib 
#include<cstdlib> //Includes functions like atoi, which converts text to an integer.

int main(int argc,char* argv[]){
    int size = (argc>1) ? atoi (argv[1]):1000;
    std::vector<int>memory(size);

    for(int i = 0; i< size ;i++)//write to the memeory 
        memory[i] = i*7;

    int errors = 0;
    for (int i=0; i<size; i++)//reads from the memory 
        if(memory[i] != i*7)
            errors++;
    
    
    if (errors == 0){
        std::cout<<"PASS"<<std::endl;
        return 0;
    }
    std::cout<<"FAIL"<<std::endl;
    return 1;
}
