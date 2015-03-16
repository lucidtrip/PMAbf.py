# PHPMyAdmin-Bruteforcer.py

Multithreading PHPMyAdmin Bruteforcer written in python


## Usage
```
                         ®          ®
                           8       8
               $$            8   8            $$
                $??$????$     88     $????$??$
                  $?????$$$$  88  $$$$?????$
                    $?????$$$$88$$$$?????$
                    $$?????$ .888 .$?????$$
                      $$??? $$8jr8$$ ???$$
                        $??$  88  $??$
                      $$???$  88  $???$$
                       s$$?$  88  $?$$s
                        s$$        $$s
+--------------------------------------------------------------+
|                  PHPMyAdmin-Bruteforcer 0.2                  |
|                             ***                              |
| Greetz fly out to:                                           |
|  DDR, B2R, BWC, ECB, MLC                                     |
|  maro, coder, airy, fr0sty, syncop, tenti, Serengeti,        |
|  knusi, ische, Buster, smurfy, saint, peak                   |
|                               and all i foget :D             |
|                                                              |
|  special thanks to whyned for the threading pattern! ♥       |
|                                                              |
|                                             author: _bop     |
|                                             date: 15.03.2015 |
+--------------------------------------------------------------+

usage: pmabf-0.2.py [-h] [-u USER] [-t THREADS] [-T TIMEOUT] [-o OUTPUT]
                    [-v {0,1,2}]
                    FILE WORDLIST

positional arguments:
  FILE                  the file with the pma urls
  WORDLIST              the wordlist file with the potential passwords

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  the PMA user (default=root)
  -t THREADS, --threads THREADS
                        the threads of coincident bruteforce (default=5)
  -T TIMEOUT, --timeout TIMEOUT
                        the connection timeout (default=15)
  -o OUTPUT, --output OUTPUT
                        save the valid logins to output file
                        (default=pmabf-0.2.log)
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity

```

## Exampels
`python pmabf.py -u root -t 150 -T 10 -o pmabf.log -v 1 pma.pot wordlist.dic`

## Tested
* Linux 2.6.32-042stab103.6 x86_64 GNU/Linux
  * Python 2.7.3
* Linux 2.6.32-042stab079.6 x86_64
  * Python 2.7.3


## Todo
* - [ ] id="select_server" deteceter
* - [x] ~~add argparse~~


## Support
You can support me for more useful tools and scripts with a litte donation
* Bitcoin: coming soon
