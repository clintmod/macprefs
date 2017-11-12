import os
from config import BACKUP_DIR
from utils import executeShell

domains = executeShell(["defaults", "domains"])
domains = domains.split("\n")[0].split(", ")
domains = ["NSGlobalDomain"] + domains

for domain in domains:
	filepath = BACKUP_DIR + domain + ".plist");
	print "Backing up: " + domain + " to " + filepath
	executeShell(["defaults", "export", domain, filepath])