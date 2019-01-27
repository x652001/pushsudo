from SudoFile import SudoFile
from PushSudo import PushSudo
from GetTime import GetTime
import sys

class Main:
    def __init__(self):
        self.sudofile = SudoFile()
        self.log = []
        self.need_to_delete = []
        self.admin_user = 'root'
        self.admin_pwd = ''

    def menu(self):
        print("""
            #########################
            # Auto Deploy Sudo File #
            #########################
            Author : Sam 
            Version: v1.0 2018/11/4""")
        while True:
            print("""
            1. Print the sudoers Table
            2. Add sudoers
            3. Del sudoers
            4. Run PushSudo
            5. Edit Admin
            6. Save & Exit
            """)
            choice = input("Select : ")
            if choice == "1":
                self.sudofile.data_print()
            elif choice == "2":
                self.sudofile.data_add()
            elif choice == "3":
                self.sudofile.data_del()
            elif choice == "4":
                self.run()
            elif choice == "5":
                self.set_admin()
            elif choice == "6":
                self.sudofile.file_write()
                sys.exit(0)

    # Push or delete the sudoers file into host
    def run(self):
        sudodata = self.sudofile.data_get()
        now = GetTime.get_nowtime_timestamp()

        # Starting Push Sudoers in sudolist
        for line in sudodata:
            try:
                # Get the Start & End Time
                host_start = GetTime.get_timestamp(line['StartTime'])
                host_end = GetTime.get_timestamp(line['EndTime'])
            except IndexError:
                self.log.append("Host=%s,Account=%s:Time Syntax Wrong" % (line['Host'],line['Account']))
                break

            # Check the Time in sudofile are available or not
            if host_end >= now >= host_start:
                host_state = True
            else:
                host_state = False
                self.need_to_delete.append(line)

            # host_state = True --> make sudofile & host_state = False --> remove sudofile
            host = PushSudo(line['Host'], self.admin_user, self.admin_pwd, line['Account'], host_state)
            self.log.append(str(GetTime.get_nowtime())+" : "+str(line)+" host_state="+str(host_state)+host.check_sudoer())

        # Delete the overdue sudoers
        self.delete()
        # write log in pushsudo.log
        self.write_log()
        self.sudofile.file_write()

    # Delete Data if the sudo user was overdue
    def delete(self):
        for line in self.need_to_delete:
            self.sudofile.data_del_direct(line)
        self.need_to_delete = []

    # Write log into pushsudo.log
    def write_log(self):
        with open('pushsudo.log','a') as f:
            for line in self.log:
                f.write(line+'\n')
            f.close()
        self.log = []

    # Edit Admin username & pwd
    def set_admin(self):
        self.admin_user = input("Admin Username:")
        self.admin_pwd = input("Admin Password: ")


if __name__ == "__main__":
    start = Main()
    try:
        user_select = sys.argv[1]
    except IndexError:
        user_select = None

    if user_select == '-f':
        start.run()
    else:
        start.menu()

