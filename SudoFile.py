import csv
from GetTime import GetTime
from prettytable import PrettyTable
import chkip

class SudoFile:
    def __init__(self):
        self.sudolist = []
        self.headname = ["Account", "Host", "StartTime", "EndTime"]
        with open('sudolist.csv', newline='') as f:
            f_csv = csv.DictReader(f)
            for row in f_csv:
                self.sudolist.append(row)

    # Load sudolist into file(csv) and close this program
    def file_write(self):
        with open('sudolist.csv', 'w', newline='') as f:
            # Clear all data in sudolist.csv
            f.truncate()
            # Write new data in sudolist.csv from sudolist
            f_csv = csv.DictWriter(f, fieldnames=self.headname)
            f_csv.writeheader()
            f_csv.writerows(self.sudolist)

    # Delete the data from sudolist
    def data_del(self):
        while True:
            self.data_print()
            count = input("Which one should be delete? (0 back to menu) :")
            if count == "0":
                break
            try:
                del self.sudolist[int(count) - 1]
            except IndexError:
                print ("Error : You need choice available number")

    def data_del_direct(self, line):
        self.sudolist.remove(line)

    # Add the data into sudolist
    def data_add(self):
        account = input("Account :")
        if account is "":
            return
        host = self.host_add()

        start_time = self.time_add("Start Time :")
        end_time = self.time_add("End Time :")

        self.sudolist.append({self.headname[0]: account, self.headname[1]: host, self.headname[2]: start_time,
                              self.headname[3]: end_time})

    # Check input date format
    @staticmethod
    def time_add(txt):
        while True:
            t = input(txt)
            if GetTime.check_time(t) is None:
                continue
            else:
                return t

    @staticmethod
    def host_add():
        while True:
            ip = input("HostIP :")
            if chkip.chk_ip(ip) is True:
                return ip
            else:
                print("Wrong Syntax, HostIP shall be xxx.xxx.xxx.xxx")
                continue

    # Return the Data to other class
    def data_get(self):
        return self.sudolist

    # Print the sudolist to User
    def data_print(self):
        x = PrettyTable(['NO']+self.headname)
        count = 1
        for line in self.sudolist:
            x.add_row([count, line["Account"], line["Host"], line["StartTime"], line["EndTime"]])
            count += 1
        print(x)

    # Modify Data,but Not in use
    def data_modify(self):
        self.data_print()
        count = input("Which one will be change?  ")
        line = self.sudolist[int(count)-1]
        line["Account"] = self.datainput("Account", line["Account"])
        line["Host"] = self.datainput("HostIP", self.sudolist[int(count)-1]["Host"])
        line["Host"] = self.datainput("HostIP", line["Host"])
        line["StartTime"] = self.datainput("StartTime", line["StartTime"])
        line["EndTime"] = self.datainput("EndTime", line["EndTime"])
        print(line)

    # Modify Data,but Not in use
    def datainput(self, text, value):
        x = input(text+"("+value+"): ")
        if x is "":
            return value
        else:
            return x



