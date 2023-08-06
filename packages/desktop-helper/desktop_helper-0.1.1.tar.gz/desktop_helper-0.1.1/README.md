# desktop-helper
## Overall
A simple desktop helper for various kinds of tedious jobs on your desktop. Previously, supported modules includes:
- Process Manager

Support platform:
- Windows
## Usage
### Install
```
python3 -m pip install desktop_helper
```
or
```
git clone https://github.com/BARaphael/desktop-helper.git
cd desktop-helper
python3 -m pip install .
```
### Quick Start
```
python3 -m desktop_helper.helper
```
## Process Manager
You may write plenty of python scripts for different kinds of work. Process manager allows centralized management of your scripts in a single location.    
### What can you do?
- You can start, stop, restart your scripts. 
- When your scripts are running, you can monitor their status via a table. Scripts' health (whether an error occurs), start time, running time, etc. are shown.
- You can view output of your scripts by double-clicking corresponding row of the process manager table.
- You can save your process manager table, and load it after next launch. You can also set them to be autostarted.
### Q & A
1.  Q: Why can't I see my scripts' output in real-time?  
    A: This maybe because you didn't flush your stdout. Set flush = True when using Python's built-in print function. For example, 
    ```
    print("something", flush=True)
    ```
2.  Q: Why my script meets an error, but process manager still says that my script doesn't have one?  
    A: Currently, only error goes into stderr can be recognized. Notice that errors in try-except block don't go into stderr. So, if you don't raise it again, no error will be noticed.