#!/bin/bash
echo "~~~~~Running Health Check~~~~~~"
exec > >(tee /var/log/health_check.log) 2>&1

print_all() {


    echo 
    echo "======================================================"
    echo "$1"
    echo "======================================================"
}

echo 
echo "Report generated on $(date)"

print_all "User Information"
echo "Current user: $(whoami)"
echo "Hostname    : $(hostname)"

#verify user 'jenna' was created
USERNAME=jenna
echo "Checking if user $USERNAME exists...."
if id $USERNAME &>/dev/null; then
    echo "User $USERNAME was created"
else
    echo "User $USERNAME was not created"
fi

#verify the packages were installed
print_all "Installed Packages"
packages=(net-tools tcpdump apache2 openssh-server netplan.io ufw rsyslog logrotate sqlite3)
for pkg in "${packages[@]}"; do
    if dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "install ok installed"; then
        printf "%-15s : %s\n" "$pkg" "Installed"
    else
        printf "%-15s : %s\n" "$pkg" "Not Installed"
    fi
done

#print names of the interfaces
#print second column
print_all "Network Interfaces:"
ip -o -4 link show | awk -F":" '{print $2}' | sed 's/^ * //'

print_all "SQLite Check"
#command -v sqlite3 checks if sqlite3 command exists in the system
db_path="/home/$USERNAME/mydb.db"
table_exists=$(sudo -u $USERNAME sqlite3 "$db_path" "SELECT name FROM sqlite_master WHERE type='table' AND name='users';")

if command -v sqlite3 >/dev/null 2>&1; then 
    echo "sqlite3 is installed"
    #check if db file exists
    if [ -f $db_path ] && [ -w $db_path ]; then 
        echo "Database exists at $db_path and is writable"
        if [ "$table_exists" = "users" ]; then
            echo "Table users exists"
        else    
            echo "Table users not exist"
        fi
    else    
        echo "Database does not exist at $db_path"
    fi

    
else
    echo "sqlite3 not installed"
fi

#Check services are running
print_all "Verify Apache, SSH and Syslog services are running"
services=("apache2" "ssh" "rsyslog")
function verify_services() {
    for service in "${services[@]}"; do
        if  systemctl is-active --quiet "$service"; then
            echo "$service is running" 
        else
            echo "$service is not running"
        fi
    done
}
verify_services



function filter_logs()
#"${1:-err}" 1 means first argument paseed to function otherwise use err as default.”

{    local level="${1:-err}"
    local keyword="${2:-Failed}"
    local date="${3:-$(date '+%Y-%m-%d')}"
#journlctl -p filters by priority level (numeric) -u filters by service
    echo "-----------------------------"
    echo "Here is the last syslog message for level $level and up"
    journalctl -p $level -xe -n 1
    echo "-----------------------------"
    echo "Here is the last syslog message with keyword $keyword"
    journalctl -u syslog -g "$keyword" -n 1
    echo "-----------------------------"
    echo "Here is the last syslog message since $date"
    journalctl -u syslog --since $date -n 1
    echo "-----------------------------"
}


filter_logs info login 
filter_logs warning failed
filter_logs warning SSH 2025-10-27

echo "The firewall rules are:"
ufw status verbose

#Get the current CPU and memory usage
#%-6s prints left aligned string in 6 character wide column
#N right aligns string width N
#first line prints header
# mpstat -P ALL 1 1 reports CPU usage per core
#awk NR>3 skips first 3 lines and only selects 2nd rows where 2nd row is number
print_all "CPU Usage Per Core"
if command -v mpstat >/dev/null 2>&1; then 
        
        printf "%-6s %-8s %-8s\n" "Core" "Idle%" "Used%"
        mpstat -P ALL 1 1 | awk 'NR>3 && $2 ~ /^[0-9]+$/ {
            idle=$12
            used=100-$12
            printf "%-6s %-8.1f %-8.1f\n", $2, idle, used
        }'
else        
    echo "installing mpstat...."
    apt-get install -y sysstat
fi
print_all "Memory Usage"
printf "%-10s %-10s %-10s \n" "Total" "Used" "Free"
free -m | awk '/Mem:/ {printf "%-10s %-10s %-10s\n", $2, $3, $4}'
