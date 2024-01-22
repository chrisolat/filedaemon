import os
import sys, time, logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import multiprocessing
import asyncio
import tkinter as tk
from tkinter import messagebox

#potential dangerous file extentions
ext = [".bat", ".cmd", ".vb", ".vbs", ".js", ".ws", ".wsf", ".wsc", ".wsh", ".wsc",
 ".ps1", ".ps1xml", ".ps2", ".msh", ".scf", ".lnk", ".inf"]

async def validate(event):
	s = event.src_path.split("\\")

	file = s[-1]
	print(file)
	for i in ext:
		if file.endswith(i):
			# await show_popup()
			print("DANGER!!!. Potential Virus Found!")
			print(event.src_path)
			

def on_created(event): # file is created
	logging.info("Created - " + event.src_path)
	asyncio.run(validate(event)) # check if file is safe
	
def on_deleted(event): # file is deleted
	logging.info("Deleted - " + event.src_path)
	
def on_modified(event): # file is changed or modified
	logging.info("Modified - " + event.src_path)
	asyncio.run(validate(event)) # check if file is safe
	
def on_moved(event): # file is copied or moved
	logging.info("Moved - " + event.src_path)
	asyncio.run(validate(event)) # check if file is safe

async def show_popup():
	messagebox.showinfo("Alert", "Potential virus found",parent=tk.Toplevel())

def watcher():
	os.system("color 3")
	create_pid_file(os.getpid())
	logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(message)s", 
	datefmt = "%Y-%m-%d  %H:%M:%S")
	
	# default directory is downloads. can be changed by specifying in sys.argv
	path = sys.argv[1] if len(sys.argv) > 1 else "E:\\User\\Downloads"
	event_handler = LoggingEventHandler()
	
	file_event = FileSystemEventHandler()
	file_event.on_created = on_created
	file_event.on_deleted = on_deleted
	file_event.on_modified = on_modified
	file_event.on_moved = on_moved
	observer = Observer()
	observer.schedule(file_event, path, recursive=True)
	
	observer.start()
	
	try:
		while True:
			time.sleep(1)
			#print(logging.LogRecord.getMessage(event_handler))
	except KeyboardInterrupt:
		observer.stop()
	observer.join

def create_pid_file(pid):
	with open("filedaemon_pid.txt", 'w') as file:
		file.writelines(str(pid))

def create_thread():
	detached_process = multiprocessing.Process(target=watcher)
	detached_process.start()

if __name__ == '__main__':
	create_thread()