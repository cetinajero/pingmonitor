from subprocess import check_output
from yaml import safe_load
from lib.mail import sendgrid_mail

def read_config():
    with open('config.yml', 'r') as f:
        doc = safe_load(f)
    return doc

def check_hdd():
    config = read_config()
    for hdd in range(len(config["hdd"]["partitions"])):
        partitions = config["hdd"]["partitions"][hdd]
        available_space_col = config["hdd"]["available_space"]["column"]
        porcentage = config ["hdd"]["porcentage_space"]
        hdd_usage = int(check_output("df -h | grep %s | awk \'{ print $%s }\' | sed -e \'s/.$//g\' | tr -d \'\n\' " % (partitions, available_space_col), shell=True))
        if hdd_usage >= porcentage:
            print("[WARN]", "HDD usage", hdd_usage, "%")
            sendgrid_mail('hdd', partitions, hdd_usage)
        else:
            print("[ OK ]", "The partition", partitions, "has", hdd_usage, "% of disk usage")
