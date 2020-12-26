#include <string>
#include <iostream>
#include <chaos.h>

using namespace std;

int main(int argc, char *argv[]) {
  if(argc != 2){
    cout<<"USAGE: chaos_prng length \ne.g. 'chaos_prng 1024' generates '1024' random bytes.\n";
    return -1;
  }
  int length = stoi(argv[1]);
  chaos::truely<CHAOS_MACHINE_XORRING64, random_device> generator;
  string bytes;
  bytes.reserve(length);
  for (int i = 0; i < length; i++ ){
    bytes.push_back(generator());    
  }
  cout<<bytes;
  return 0;
}
