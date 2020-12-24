#include <string>
#include <iostream>
#include <chaos.h>

int main(int argc, char *argv[]) {
  if(argc != 2){
    printf("USAGE: gen_random length\ne.g. 'gen_random 1024' generates 1024 random bytes\n");
    return -1;
  }

  int length = std::stoi(argv[1]);
  chaos::truely<CHAOS_MACHINE_XORRING64, std::random_device> generator;
  std::string bytes;
  bytes.reserve(length);
  for (int i = 0; i < length; i++ ){
    bytes.push_back(generator());    
  }
  std::cout<<bytes;
  return 0;
}
