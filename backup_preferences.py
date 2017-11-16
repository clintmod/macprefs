import config
from utils import execute_shell


def backup():
    domains = execute_shell(["defaults", "domains"])
    domains = domains.split("\n")[0].split(", ")
    domains = ["NSGlobalDomain"] + domains

    for domain in domains:
        filepath = config.get_backup_file_path(domain)
        print "Backing up: " + domain + " to " + filepath
        execute_shell(["defaults", "export", domain, filepath])


if __name__ == '__main__':
    backup()
