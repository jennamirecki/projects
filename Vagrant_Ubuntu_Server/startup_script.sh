#!/bin/bash
#Exit immediately if script fails
set -e
#Pipeline commands will fail if pipeline fails
set -o pipefail
set -x
#Redirect stdout and stderr to file and prints them to terminal
exec > >(tee -a "/var/log/sys_setup.log") 2>&1
#Prints line number and command if it fails
trap 'echo "ERROR at line $LINENO: $BASH_COMMAND"' ERR

#Update system and install packages
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get dist-upgrade -y
apt-get install -y build-essential dkms linux-headers-generic
#apt-get install -y build-essential dkms linux-headers-$(uname -r)
packages=(net-tools tcpdump apache2 openssh-server netplan.io ufw rsyslog logrotate sqlite3)

#Install services
apt-get install -y "${packages[@]}"

#Enable services
services=(apache2 ssh rsyslog ufw)
function config_services() {
    
    for service in "${services[@]}"; do
        echo "Enabling $service"
        systemctl enable "${service}"
        systemctl start "${service}"
        
       
    done
}
config_services



#Create user with password and put it in sudo group
USERNAME="jenna"
PASSWORD="jr123"

#create user then verify
if ! id $USERNAME &>/dev/null; then
    useradd -m -s /bin/bash $USERNAME
    echo "$USERNAME:$PASSWORD"| chpasswd
    echo "User $USERNAME was created"
else
    echo "User $USERNAME already exists"
fi


#Configure sqlite and create database
db_path="/home/$USERNAME/mydb.db"
mkdir -p "/home/$USERNAME"
chown "$USERNAME:$USERNAME" "/home/$USERNAME"

sudo -u $USERNAME sqlite3 "$db_path" <<SQL
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
);
INSERT OR IGNORE INTO users (username, password) VALUES ('$USERNAME', '$PASSWORD');
SQL
chown -R "$USERNAME":"$USERNAME" "/home/$USERNAME"  
chmod 600 "$db_path"

#Configure the OpenSSH server to enable password authentication
sed -i -E "s/^(#\s*)?PasswordAuthentication\s+.* yes/PasswordAuthentication yes/" /etc/ssh/sshd_config


#Attempt SSH connection to server from localhost
if systemctl is-active --quiet ssh; then
    echo "SSH is running"
else
    echo "SSH server is not running"
fi

#Configure firewall (ufw)
ufw_status=$( ufw status)
if echo "$ufw_status" | grep -q "Status:active"; then
    echo "UFW is running"
else 
    
    echo "Failed to start UFW"
    

fi
#Deny telnet, allow OpenSSH, HTTP/S, MySQL ports
ufw deny 23
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3306/tcp
ufw enable 
ufw logging on
ufw default deny incoming
ufw default allow outgoing
echo "---------------Firewall Rules-----------------"

#Verify syslog
systemctl enable rsyslog
systemctl start rsyslog

#Filter Log messages based on level, keyword, or date
logger -p user.error "This is a test error message from a Bash script"
logger -p user.info "This is a test info message from a Bash script"
logger -p user.warning "This is a test warning message from a Bash script"



#Configure SSH log rotation
#Create new ssh log rotation file with following settings
tee /etc/logrotate.d/ssh-rotate >/dev/null << EOF
/var/log/auth.log {
    daily 
    rotate 7
    compress
    missingok
    notifempty
}
EOF








