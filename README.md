
<h1 align="center">Tap on Golem's randomness ocean</h1>

## Rational
A single computer's entropy allowance is a stub. This project tries to extract random streams from the distributed network of computers provided by [Golem](https://golem.network). The idea is to have a rest API sitting on some address that when invoked, asks Golem nodes for their random data. Each node runs some special software that employ a variaty of PRNGs to provide the requested randomness. At the moment, there are two PRNGs, one based on [Chaos machines](https://github.com/maciejczyzewski/libchaos) and the other that makes use of [Sodium](https://libsodium.org/).  

### Invocation
first off please head to Golem handbook and learn how to setup a [requestor workflow](https://handbook.golem.network/requestor-tutorials/flash-tutorial-of-requestor-development).  
Simply run the `script.sh` file via your shell and wait for the output. The output you receive depends on the length and number sources you pass to the script.  
Example:  
`~$ ./script.sh -s 8 -l 16` asks for 16 bytes of random data from 8 sources.
The output would be:  
<pre>
{
  "csprng": {
    "xored": "2NyHU/7UtXf5q0kZsi9C5g==",
    "streams": [
      "F4wOs1o/9K0CaxYpBnrgNQ==",
      "B+ID7aLtBYWicr5bdSV00w==",
      "IpY6WCP3LcsnBOnq4HXWQA==",
      "JawP1hOK6EqWHfFZ8KarIg==",
      "FH5XJRJ7VkDbly6vV7mrCw==",
      "oF9yoBlzqsTASyl4YOCQRA=="
    ]
  },
  "chaos": {
    "xored": "NKMedZrCXZZsaYCAyZoiyg==",
    "streams": [
      "pwzGJczOkP6KQuQUySiuNg==",
      "tE8AgO7SFzp2gHz6WNx+Xg==",
      "CNBMpcYIJnTwwSgRXKqvTA==",
      "mC+wQN7sDpDPCWB4TtqhgA==",
      "OgCY3WKKRJrsboyegWAivA==",
      "rKfiPKBYglTdZ5CAzBKloA=="
    ]
  }
}
</pre>
If sources are > 2, two are choosen in random, removed from the list and xored. This is done to enrich the outcome. 

## Caveat
Note that this API is just an experiment and still in development. So, please employ extreme caution in using it in real applications.

## TODO
- Make sure the sources are distinct
- Cryptographically secure tests & benchmarks
- Hook a public REST API for smart contract consumers

## Some presentation
[https://siasky.net/BACpmQBkTw5Ut1wuWFa6r3xQZcQMGlf26LhE2PmpkviVAQ](https://siasky.net/BACpmQBkTw5Ut1wuWFa6r3xQZcQMGlf26LhE2PmpkviVAQ)