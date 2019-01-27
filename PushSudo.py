import paramiko


class PushSudo:
    def __init__(self, host, user, passwd,sudo_user,state):
        # SSH Login Informantion
        self.host = host
        self.user = user
        self.passwd = passwd
        # sudo user's config in sudoers.d
        self.sudo_user = sudo_user
        self.sudo_line = sudo_user + " ALL=(ALL) NOPASSWD:ALL"
        self.state = state
        # SSH Client init
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Make or Remove /etc/sudoers.d/ file
    def check_sudoer(self):
        # Login the secure shell
        try:
            self.ssh.connect(self.host, 22, self.user, self.passwd, timeout=5, key_filename='/root/.ssh/id_rsa')
        # except TimeoutError:
        except:
            log = "Can't connect Server"
            return log

        # Check the sudoers.d is exist or not.
        stdin, stdout, stderr = self.ssh.exec_command("cat /etc/sudoers.d/"+self.sudo_user)
        result = stdout.readlines()
        # unlock sudoers.d
        self.sudofile_unlock()
        # If the state == True , this user should have sudo.
        if self.state is True:
            # print("this user shall have sudo")
            if result == []:
                self.sudofile_add()
                log = " add sudoers.d file"
            else:
                ssh_sudoers_line = result[0].strip('\n')
                if ssh_sudoers_line == self.sudo_line:
                    log = " had already added sudoers.d file"
                else:
                    self.sudofile_add()
                    log = " sudoers.d file had been changed"

        else:
            # print("This user shall not have sudo")
            if result == []:
                log = " Do Nothing"
            else:
                self.sudofile_del()
                log = " sudoers.d had been delete"

        self.ssh.close()
        return log

    def sudofile_add(self):
        command = "echo " + "'" + self.sudo_line + "'" + "> /etc/sudoers.d/" + self.sudo_user
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return

    def sudofile_del(self):
        stdin, stdout, stderr = self.ssh.exec_command("rm -f /etc/sudoers.d/" + self.sudo_user)
        return

    def sudofile_unlock(self):
        stdin, stdout, stderr = self.ssh.exec_command("chattr -i /etc/sudoers.d/*" + self.sudo_user)

    def debug(self):
        print(self.host)
        print(self.passwd)
        print(self.sudo_user)








