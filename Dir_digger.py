from argparse import ArgumentParser,FileType
from threading  import Thread,Lock 
from requests import get,exceptions
from termcolor  import colored
from colorama import Fore,Style,init
import time 

from colorama import Fore, Style, init

dir_list = []

class Dir_digger():
      init(autoreset=True)
      def __init__(self,domain,wordlist,threads=int,verbose=False,output=None):
          self.domain  = domain.rstrip('/')
          self.wordlist = iter(wordlist.read().split())
          self.threads = threads 
          self.verbose = verbose
          self.lock = Lock()            
          self.output = output

      def banner(self):
          print(Fore.RED + Style.BRIGHT + r"""
 
           _____    _   _____                 _   _                               
          |  __ \  (_) |  __ \               | | (_)                              
          | |  | |  _  | |__) |            __| |  _    __ _    __ _    ___   _ __ 
          | |  | | | | |  _  /            / _` | | |  / _` |  / _` |  / _ \ | '__|
          | |__| | | | | | \ \           | (_| | | | | (_| | | (_| | |  __/ | |   
          |_____/  |_| |_|  \_\           \__,_| |_|  \__, |  \__, |  \___| |_|   
                                 ______                __/ |   __/ |              
                                |______|              |___/   |___/               

          """ + Fore.RED + Style.BRIGHT +
          f" Author     : knightc0de\n \t" +
          f" User-Agent : Dir_digger/5.0\n \t" +
          f" Tool    :  WEB Directory Bruteforcer\n")
          
          color = "red"
          print(colored(f"[-] Scanning .... ",color))
          
      def thread_handling(self):
          proc_start_time = time.time()
          thread_list = []
          for _ in  range(self.threads):
             thread_list.append(Thread(target=self.digger_))
          for thread in thread_list:
              thread.start()
          for thread in thread_list:
              thread.join()
         
          
          proc_end_time = time.time()
          print(f"Scan Complete in {proc_end_time - proc_start_time :.2f} seconds")
     
      def digger_(self):
          global dir_list
          while True:
            try:
                with self.lock:
                  word = next(self.wordlist).strip('/')
            except StopIteration:
                break
            url_https = f"https://{self.domain}/{word}"
            url_http = f"http://{self.domain}/{word}"
            headers = {"User-Agent": "Dir_digger/5.0"}
            try:
                
                response = get(
                          url_https,
                          headers=headers,
                          timeout=5,
                          allow_redirects=True,
                          )

                if response.status_code in [200, 301, 302, 403]:  
                   dir_list.append((word, response.status_code, url_https))
                   with self.lock:
                    if self.verbose:
                       color = "green"
                       print(colored(f"[+] Found - {url_https}",color)) 
                       continue
            except (exceptions.RequestException,exceptions.Timeout):
                pass

            try:
               
               response = get(
                        url_http,
                        headers=headers,
                        timeout=5,
                        allow_redirects=True,
                        )

               if response.status_code in [200,301,302,403]:
                  dir_list.append((word, response.status_code, url_http))             
                  with self.lock:
                     if self.verbose:
                         color = "green"
                         print(colored(f"[+] Found - \t {response.status_code} {url_http}",color))
            except (exceptions.RequestException, exceptions.Timeout):
                   pass 

if __name__ == "__main__":
    parser = ArgumentParser(description="Directory Busting Tool" , epilog="%(prog)s 10.1.1.10 -w common.txt -t 500 -v" ) 
    parser.add_argument(metavar="domian/ip", help=" target domian/ip " , dest="domain")
    parser.add_argument("-w",help="wordlist",dest="wordlist",type=FileType('r'),default="dirb_.txt")
    parser.add_argument("-t",help=" No of Threads " , dest="threads",type=int,default=500)
    parser.add_argument("--output", help="Save output to file", dest="output")
    parser.add_argument("-v",help="verbose",dest="verbose",action="store_true")
    args = parser.parse_args()
 
    
    dig = Dir_digger(args.domain, args.wordlist, args.threads, args.verbose)
    dig.banner()
    dig.thread_handling()

    
    print("\n[+] Directories Found:")
    
    if args.output:
        with open(args.output, 'w') as out_file:
            for word, status, url in dir_list:
                out_file.write(f"{word}\t[{status}] {url}\n")
                print(f"/{word}\t[{status}] {url}")
                color = "green"
        print(colored(f"\n[+] Output saved to: {args.output}",color))
    
    else:
        for word, status, url in dir_list:
            color = "green"
            if (status == 403):
                 color = "red"
            elif status in [301,302]:
                 color = "cyan"
            print(colored(f"/{word} \t  \t [{status}] {url}",color))
  


            



               
            

