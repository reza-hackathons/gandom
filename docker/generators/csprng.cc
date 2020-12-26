#include <string.h>
#include <iostream>
#include <sodium.h>
#include <string>

using namespace std;

int main(int argc, char *argv[]) {
  if(argc != 2){
    cout<<"USAGE: csprng length \ne.g. 'csprng 1024' generates '1024' random bytes.\n";
    return -1;
  }
  int length = stoi(argv[1]);
  if(sodium_init() < 0){
    cout<<"Initialization of libsodium failed, quitting.\n";
    return -1;
  }
  string bytes;
  bytes.reserve(length);
  for (int i = 0; i < length; i++ ){
    unsigned char c;
    randombytes_buf(&c, 1);
    bytes.push_back(c);    
  }
  cout<<bytes;
  return 0;
}