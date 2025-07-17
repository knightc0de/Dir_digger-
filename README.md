# 🔍Dir_digger
![](/media_0.png)

# About
### A lightweight, fast,  **Directory Buster** written in Python — designed for CTFs, network assessments.

---

##  Features
-  Fast Directory enumeration with HTTP/HTTPS fallback
-  Verbose mode 
-  Clean output with color-coded statuses:
  > 200 → Green

  > 403 → Red

  > 301/302 → Cyan
-  [option] for saving output in  files 
-  Works platform (tested on Linux, Windows, Arch VM)
---
##  Requirements

- Python 3.x
- [`termcolor`]
- [`requests`]
- [`colorama`]
## Install dependencies
```
pip3 install requests termcolor colorama

```
##  Installation
> 1. Clone the repository:
   ```bash
   git clone https://github.com/knightc0de/Dir_digger-.git
   cd Dir_digger
  ```

## Usages
> python dir_digger.py [target] -w [wordlist] -t [threads] -v --output [filename]

```bash
   python3 Dir_digger.py example.com -w dirb_.txt -t 200 -v --output found.txt
```

# 👨‍💻Author 
### @Knightc0de
