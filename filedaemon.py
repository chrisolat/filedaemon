import os
import sys, time, logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import subprocess
import _thread

#potential dangerous file extentions
ext = [".bat", ".cmd", ".vb", ".vbs", ".js", ".ws", ".wsf", ".wsc", ".wsh", ".wsc",
 ".ps1", ".ps1xml", ".ps2", ".msh", ".scf", ".lnk", ".inf"]

def validate(event):
	s = event.src_path.split("\\")

	file = s[-1]
	
	for i in ext:
		if file.endswith(i):
			os.system("start C:\\Users\\User\\alert.txt") # alert.txt is opened when a dangerous file is found
			print("DANGER!!!. Potential Virus Found!. Do you want to delete this file? ")
			print(event.src_path)
			ans = input("Enter Y/N \n")
			if(ans == "y" or ans == "Y"):
				print("deleting... press CTRL + C to cancel")
				time.sleep(3)
				try:
					os.remove(event.src_path)
					
				except FileNotFoundError:
					print("File was not found")
			else:
				pass

def on_created(event): # file is created
	logging.info("Created - " + event.src_path)
	validate(event) # check if file is safe
	
def on_deleted(event): # file is deleted
	logging.info("Deleted - " + event.src_path)
	
def on_modified(event): # file is changed or modified
	logging.info("Modified - " + event.src_path)
	validate(event) # check if file is safe
	
def on_moved(event): # file is copied or moved
	logging.info("Moved - " + event.src_path)
	validate(event) # check if file is safe

def watcher():
	os.system("color 3")
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
	

	
watcher()
# def child(tid):
	# print("hello from thread ", tid)
	
# def parent():
	# i = 0
	# while True:
		# i += 1
		# _thread.start_new_thread(child, (12,))
		# if input() == "q": break
		
# parent()