from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import csv
import os

class Converter:

    calc_value = 0.0
    div_trigger = False
    mult_trigger = False
    sub_trigger = False
    add_trigger = False

    def quit(self):
        root.quit()

    def tbr_converter(self):
        files=filedialog.askopenfilenames()
        temp_list=[]
        num_files=len(files)
        file_names=''
        name = ''
        file_list=[]
        filename=''
        count=0
        while count<num_files:
            if count==0:
                file_list=[files[count]]
                file_names = os.path.basename(files[count])
            else:
                file_list.append(files[count])
                file_names = file_names + ', '+os.path.basename(files[count])
            count+=1
        count=0
        self.number_entry.delete(0, "end")
        self.number_entry.insert(0, "Here are the Time base files: "+file_names)

        while count<num_files:
            filename=file_list[count]
            with open(filename, "r") as fOpen:
                csv_reader = csv.reader(fOpen)
                i = 0
                while i < 19:
                    next(csv_reader)
                    i += 1

                for row in csv_reader:
                    if len(row) == 2:
                        name = row[1]
                    else:
                        if row[0] == '2':
                            pass
                        else:
                            firstIn = row[1] + ' ' + row[6]
                            lastOut = row[1] + ' ' + row[5]
                            hrsWrk = row[1] + ' ' + row[3]
                            hrsInZone = row[1] + ' ' + row[6]

                            if '-' in firstIn:
                                if len(firstIn) > 24:
                                    firstIn = firstIn[:11] + ' ' + firstIn[24:]
                                else:
                                    firstIn = firstIn[:11] + ' -' + firstIn[11:19]
                            if '-' in lastOut:
                                if len(lastOut) > 24:
                                    lastOut = lastOut[13:]
                                else:
                                    lastOut = lastOut[:11] + ' -' + lastOut[11:19]
                            if '-' in hrsWrk:
                                if len(hrsWrk) > 24:
                                    hrsWrk = hrsWrk[13:]
                                else:
                                    hrsWrk = hrsWrk[:11] + ' -' + hrsWrk[11:19]
                            if '-' in hrsInZone:
                                if len(hrsInZone) > 24:
                                    hrsInZone = hrsInZone[13:]
                                else:
                                    hrsInZone = hrsInZone[:11] + ' -' + hrsInZone[11:19]
                            self.Files.append([name, firstIn, 'In'])
                            self.Files.append([name, lastOut, 'Out'])
                            self.Files.append([name, hrsWrk, 'HWK'])
                            self.Files.append([name, hrsInZone, 'HZ'])
                            temp_list.append([name, firstIn, 'In'])
                            temp_list.append([name, lastOut, 'Out'])
                            temp_list.append([name, hrsWrk, 'HWK'])
                            temp_list.append([name, hrsInZone, 'HZ'])
            count+=1

        fOpen.close()
        with open('TBR Converter.csv', "w", newline='') as fWrite:
            temp = csv.writer(fWrite)
            for row in temp_list:
                line_new = row
                temp.writerow(line_new)


    def tr_converter(self):
        files = filedialog.askopenfilenames()
        num_files = len(files)
        file_names = ''
        file_list = []
        count = 0
        temp_list=[]
        while count < num_files:
            if count == 0:
                file_list = [files[count]]
                file_names = os.path.basename(files[count])
            else:
                file_list.append(files[count])
                file_names = file_names + ', ' + os.path.basename(files[count])
            count += 1
        self.trnumber_entry.delete(0, "end")
        self.trnumber_entry.insert(0, "Here are the Time base files: " + file_names)

        count = 0
        while count < num_files:
            filename=file_list[count]
            with open(filename, "r") as fOpen:
                csvreader = csv.reader(fOpen)
                i = 0
                while i < 13:
                    next(csvreader)
                    i += 1

                for row in csvreader:
                    if len(row) > 2:
                        if row[2] == 'Denied APB In':
                            pass
                        elif row[2] == 'Denied APB Out':
                            pass
                        elif row[2] == 'Allowed Normal In':
                            dateconvert = row[0].replace('-', '/')
                            self.Files.append([row[1], dateconvert, 'In'])
                            temp_list.append([row[1], dateconvert, 'In'])
                        elif row[2] == 'Allowed Normal Out':
                            dateconvert = row[0].replace('-', '/')
                            self.Files.append([row[1], dateconvert, 'Out'])
                            temp_list.append([row[1], dateconvert, 'Out'])
                        else:
                            pass
                fOpen.close()
            count+=1
            with open('TR Converter.csv', "w", newline='') as fWrite:
                temp = csv.writer(fWrite)
                for row in temp_list:
                    line_new = row
                    temp.writerow(line_new)
        self.tr_Check=True


    def process(self):
        new_list = []
        with open('TempFile1.csv', "w", newline='') as fWrite:
            hourFile = csv.writer(fWrite)
            hourFile.writerow(['Name', 'Punch', 'Type'])
            for row in self.Files:
                line = row
                hourFile.writerow(line)
        fWrite.close()
        #breaks Date and Time
        with open('TempFile1.csv', "r") as fOpen:
            csvreader = csv.reader(fOpen)
            next(csvreader)
            for row in csvreader:
                new_line = [row[0], row[1][:10], row[1][11:], row[2]]
                new_list.append(new_line)
        with open('TempFile2.csv', "w", newline='') as fWrite:
            ReOrg = csv.writer(fWrite)
            ReOrg.writerow(['Name', 'Date', 'Punch', 'Type'])
            for row in new_list:
                line = row
                ReOrg.writerow(line)
        fWrite.close()
        fOpen.close()
        # -----------------Sorts and Organize the file->
        comb = pd.read_csv('TempFile2.csv')
        comb.sort_values(['Name', 'Date', 'Punch'], axis=0, ascending=True, inplace=True)
        comb.drop_duplicates(keep='first', inplace=True)
        comb.reset_index(drop=True, inplace=True)
        #comb.to_csv('ReOrganized.csv', index=None)
        # ---- Creates a list of names-->
        final_name = comb.loc[0, 'Name']
        final_date = comb.loc[0, 'Date']
        Tlist = []
        punch = []
        hz = ''
        hwk = ''
        for index, row in comb.iterrows():
            if final_name == row[0] and final_date == row[1] and (row[3] == "In" or row[3] == "Out"):
                punch.append(row[2])
            elif final_name == row[0] and final_date == row[1] and row[3] == "HWK":
                hwk = str(row[2]) + ' hwk'
            elif final_name == row[0] and final_date == row[1] and row[3] == "HZ":
                hz = str(row[2]) + ' Hz'
            else:
                TempList = [final_name]
                TempList.append(final_date)
                TempList.append(hwk)
                TempList.append(hz)
                for x in punch:
                    TempList.append(x)
                Tlist.append(TempList)
                TempList = []
                punch = []
                final_name = row[0]
                final_date = row[1]

        with open('Output.csv', "w", newline='') as fWrite:
            ReOrg2 = csv.writer(fWrite)
            for row in Tlist:
                if '/' in row[1]:

                    line_new = row
                    ReOrg2.writerow(line_new)
        fWrite.close
        print('Cleaning Up Temp Files')
        if os.path.exists('TempFile1.csv'):
            os.remove('TempFile1.csv')
        if os.path.exists('TempFile2.csv'):
            os.remove('TempFile2.csv')
        if os.path.exists('TBR Converter.csv'):
            os.remove('TBR Converter.csv')
        if os.path.exists('TR Converter.csv'):
            os.remove('TR Converter.csv')
        print('Clean up Complete')
        self.trnumber_entry.delete(0, "end")
        self.trnumber_entry.insert(0, "Process Completed!!")
        self.number_entry.delete(0, "end")
        self.number_entry.insert(0, "Process Completed!")


    def __init__(self, root):
        self.entry_value = StringVar(root, value="None Selected")
        self.tr_entry_value = StringVar(root, value="None Selected")
        self.Files=[]
        self.tbr_Check=False
        self.tr_Check = False

        root.title("Converter")
        root.geometry('1000x300')
        root.resizable(width=False, height=False)
        style= ttk.Style()
        style.configure("TButton",
                        font="Serif 15",
                        padding=10,
                        width=25
                        )
        style.configure("TEntry",font="Serif 18",padding=14)

        self.tbr_label = ttk.Label(root, text="Please select your Time Based Files :",font="Serif 18").grid(row=0,columnspan=4)
        self.number_entry = ttk.Entry(root, textvariable=self.entry_value, width=100)
        self.number_entry.grid(row=1, columnspan=4, padx=2)
        self.tbrbutton = ttk.Button(root, text="Time Based Files", command=lambda: self.tbr_converter()).grid(row=1, column=5)

        self.tr_label = ttk.Label(root, text="Please select your Transaction Files :", font="Serif 18").grid(row=2,columnspan=4)
        self.trnumber_entry = ttk.Entry(root, textvariable=self.tr_entry_value, width=100)
        self.trnumber_entry.grid(row=3, columnspan=4, padx=2)
        self.tbrbutton = ttk.Button(root, text="Transaction Files", command=lambda: self.tr_converter()).grid(row=3,column=5)
        self.tbrbutton = ttk.Button(root, text="Process Files", command=lambda: self.process()).grid(row=4,column=5)
        self.tbrbutton = ttk.Button(root, text="Quit", command=lambda: self.quit()).grid(row=5, column=5)

root= Tk()

convert = Converter(root)

root.mainloop()
