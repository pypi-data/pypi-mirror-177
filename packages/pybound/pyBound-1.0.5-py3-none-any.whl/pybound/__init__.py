__version__ = '1.0.5'
import sys, os
from time import sleep

def delete_line(num = 1):
  CURSOR_UP_ONE = '\x1b[1A' 
  ERASE_LINE = '\x1b[2K'
  for i in range(num):
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE)
    sys.stdout.flush()
    
def clear():
	os.system('clear')
  
def slow_print(*strings, time = 0.045, sep = ' ', end = '\n'):	
  num = len(strings)
  for string in strings:
    string = str(string)
    for character in string:
      sys.stdout.write(character)
      if string.startswith("\033") == False and string.startswith("\x1b") == False:
        sys.stdout.flush()
        sleep(time)  
    num -= 1
    if num != 0 and str(strings[len(strings)-num-1]).startswith("\033") == False and str(strings[len(strings)-num-1]).startswith("\x1b") == False:
      sys.stdout.write(sep)
      sys.stdout.flush()	
  sys.stdout.flush()
  sys.stdout.write(end)
  sys.stdout.flush()
  
def wait(time = 1):
	sleep(time)
  
def rgb_fore(r, g, b):
		return f'\033[38;2;{r};{g};{b}m'
	
def rgb_back(r, g, b):
    return f'\033[48;2;{r};{g};{b}m'
  
def end():
  return "\033[0m"	
  
def bold():
  return "\033[1m" 
  
def faint():
  return "\033[2m"
  
def italic():
  return "\033[3m" 
  
def underline():
  return "\033[4m" 
  
def blink_slow():
	return "\033[5m"
  
def blink_fast():
	return "\033[6m"
  
def negative():
	return "\033[7m"
  
def conceal():
  return "\033[8m"
  
def crossed():
	return "\033[9m"

def cursor_up(num = 1):
	sys.stdout.write(f'\x1b[{num}A')
	sys.stdout.flush()

def cursor_down(num = 1):
	sys.stdout.write(f'\x1b[{num}B')
	sys.stdout.flush()

def cursor_forward(num = 1):
	sys.stdout.write(f'\x1b[{num}C')
	sys.stdout.flush()

def cursor_back(num = 1):
	sys.stdout.write(f'\x1b[{num}D')
	sys.stdout.flush()

def cursor_next_line(num = 1):
	sys.stdout.write(f'\x1b[{num}E')
	sys.stdout.flush()

def cursor_prev_line(num = 1):
	sys.stdout.write(f'\x1b[{num}F')
	sys.stdout.flush()

def cursor_horiz_abs_pos(col = 1):
	sys.stdout.write(f'\x1b[{col}G')
	sys.stdout.flush()

def cursor_pos(row = 1, col = 1):
	sys.stdout.write(f'\x1b[{row};{col}H')
	sys.stdout.flush()
  
def cursor_indent(num = 1):
	sys.stdout.write(f'\x1b[{num}I')
	sys.stdout.flush()

def erase_in_display(mode = "entirescreen"):
	if mode.lower().strip(' ').strip('-').strip('_') == "cursortoend":
		mode = 0
	elif mode.lower().strip(' ').strip('-').strip('_') == "starttocursor":
		mode = 1
	elif mode.lower().strip(' ').strip('-').strip('_') == "entirescreen":
		mode = 2
	elif mode.lower().strip(' ').strip('-').strip('_') == "scrollback":
		mode = 3
	else:
		sys.exit("Error: mode value does not exist\nCheck documentation for modes at https://pypi.org/pybound/#description.")
	sys.stdout.write(f'\x1b[{mode}J') # 0 - 3
	sys.stdout.flush()

def erase_in_line(mode = "entireline"):
	if mode.lower().strip(' ').strip('-').strip('_') == "cursortoend":
		mode = 0
	elif mode.lower().strip(' ').strip('-').strip('_') == "starttocursor":
		mode = 1
	elif mode.lower().strip(' ').strip('-').strip('_') == "entireline":
		mode = 2
	else:
		sys.exit("Error: mode value does not exist\nCheck documentation for modes at https://pypi.org/pybound/#description.")
	sys.stdout.write(f'\x1b[{mode}K') # 0 - 2
	sys.stdout.flush()

def scroll_up(num = 1):
	sys.stdout.write(f'\x1b[{num}S')
	sys.stdout.flush()

def scroll_down(num = 1):
	sys.stdout.write(f'\x1b[{num}T')
	sys.stdout.flush()

def cursor_save_pos():
	sys.stdout.write('\x1b[s')
	sys.stdout.flush()

def cursor_restore_pos():
	sys.stdout.write('\x1b[u')
	sys.stdout.flush()

def cursor_invisible():
	sys.stdout.write('\x1b[?25l')
	sys.stdout.flush()

def cursor_visible():
	sys.stdout.write('\x1b[?25h')
	sys.stdout.flush()