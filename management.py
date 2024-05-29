from connection import *
from cls import *
from tkinter import *
from tkinter import ttk, messagebox
import os

repository = Repository()

class App(Frame):
    def __init__(self, screen=None):
        super().__init__(screen)
        self.master = screen
        self.CreateWidget()

    def CreateWidget(self):
        # Frame Register
        self.frmRegister = Frame(self.master, width=270, height=425, highlightbackground="gray", highlightthickness=1)
        self.frmRegister.place(x=520, y=50)

        # lables
        Label(self.frmRegister, text="فرم ثبت کاربر", font="nazanin 15 bold").place(x=90, y=0)
        Label(self.frmRegister, text=":نام", anchor="w", width=10).place(x=180, y=60)
        Label(self.frmRegister, text=":نام خانوادگی", anchor="w", width=10).place(x=180, y=90)
        Label(self.frmRegister, text=":تاریخ تولد", anchor="w", width=10).place(x=180, y=120)
        Label(self.frmRegister, text=":جنسیت", anchor="w", width=10).place(x=180, y=150)

        # Images
        self.imgsrch = PhotoImage(file="img/srch.png")
        self.imgclose = PhotoImage(file="img/close.png")
        self.imgexit = PhotoImage(file="img/exit.png")

        # var string
        self.varName = StringVar()
        self.varFamily = StringVar()
        self.varAge = StringVar()
        self.varSearch = StringVar()
        self.varSex = IntVar()
        self.varIsAdmin = IntVar()
        self.varId = StringVar()

        # Entrys
        self.txtname = Entry(self.frmRegister, justify="center", textvariable=self.varName)
        self.txtname.place(x=30, y=60)
        self.txtfamily = Entry(self.frmRegister, justify="center", textvariable=self.varFamily).place(x=30, y=90)
        self.txtid = Entry(self.frmRegister, justify="center", textvariable=self.varId).place_forget()

        # Combobox
        self.comboage = ttk.Combobox(self.frmRegister, state="readonly", textvariable=self.varAge, justify="right")
        self.comboage["values"] = self.GetComboVal()
        self.comboage.current(40)
        self.comboage.place(x=30, y=120)

        # RadioButton
        self.radio1 = Radiobutton(self.frmRegister, text="زن", variable=self.varSex, value=1).place(x=80, y=150)
        self.radio2 = Radiobutton(self.frmRegister, text="مرد", variable=self.varSex, value=0).place(x=30, y=150)

        # Checkbox
        self.chk1 = Checkbutton(self.frmRegister, text="آیا ادمین شود؟", variable=self.varIsAdmin,
                                command=self.ToggleUserPassFrame)
        self.chk1.place(x=30, y=200)

        # buttons
        # button Register
        self.btnRegister = Button(self.frmRegister, text="ثبت نام", command=self.Register)
        self.btnRegister.configure(bg="green", fg="white")
        self.btnRegister.place(x=30, y=370)
        # button Cancel
        self.btnCancel = Button(self.frmRegister, bg="gray", text="كنسل", command=self.ClickCancel)
        self.btnCancel.configure(fg="white")
        self.btnCancel.place_forget()
        # button Delete
        self.btnDelete = Button(self.frmRegister, text="حذف", command=self.ClickDelete)
        self.btnDelete.configure(bg="red", fg="white")
        self.btnDelete.place_forget()
        # button Edit
        self.btnEdit = Button(self.frmRegister, text="ویرایش", command=self.ClickEdit)
        self.btnEdit.configure(bg="#5887fc", fg="white")
        self.btnEdit.place_forget()
        # button Show Search
        self.btnShowSearch = Button(screen, text="*", command=self.ClickShowSearch, image=self.imgsrch)
        self.btnShowSearch.configure(width=25, height=25)
        self.btnShowSearch.place(x=475, y=20)

        # tbl
        self.tbl = ttk.Treeview(self.master, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show="headings", height=20)
        self.tbl.column("# 6", width=75, anchor=E)
        self.tbl.heading("# 6", text="كد كاربر")
        self.tbl.column("# 5", width=100, anchor=E)
        self.tbl.heading("# 5", text="نام")
        self.tbl.column("# 4", width=100, anchor=E)
        self.tbl.heading("# 4", text="نام خانوادگی")
        self.tbl.column("# 3", width=75, anchor=E)
        self.tbl.heading("# 3", text="تاریخ تولد")
        self.tbl.column("# 2", width=75, anchor=E)
        self.tbl.heading("# 2", text="جنسیت")
        self.tbl.column("# 1", width=75, anchor=E)
        self.tbl.heading("# 1", text="نقش کاربر")
        self.tbl.bind("<Button-1>", self.GetSelection)
        self.tbl.place(x=5, y=50)
        self.LoadTable()

        # Frame UserPass
        self.varUsername = StringVar()
        self.varPassword = StringVar()
        self.frmUserPass = Frame(self.frmRegister, width=240, height=95)
        self.frmUserPass.place_forget()
        Label(self.frmUserPass, text=":لطفا نام کاربری و پسورد را وارد کنید", anchor="w", width=25).place(x=50, y=0)
        Label(self.frmUserPass, text=":نام کاربری", anchor="w", width=10).place(x=170, y=30)
        Label(self.frmUserPass, text=":کلمه عبور", anchor="w", width=10).place(x=170, y=60)
        self.txtusername = Entry(self.frmUserPass, justify="center", textvariable=self.varUsername)
        self.txtusername.place(x=30, y=30)
        self.txtpassword = Entry(self.frmUserPass, justify="center", textvariable=self.varPassword).place(x=30, y=60)

        # Frame Search
        self.frmSearch = Frame(self.master, width=500, height=40)
        self.frmSearch.place_forget()
        Label(self.frmSearch, text=":مقدار جستجو", anchor="w", width=10).place(x=380, y=10)
        self.txtsearch = Entry(self.frmSearch, justify="center", width=49, textvariable=self.varSearch).place(x=75,
                                                                                                              y=10)
        self.btnsearch = Button(self.frmSearch, text="جستجو", command=self.Search)
        self.btnsearch.configure(height=1, width=8)
        self.btnsearch.place(x=0, y=8)
        self.btnclosefrm = Button(self.frmSearch, text="*", image=self.imgclose, width=18, height=18,
                                  command=self.ClickCloseSearch)
        self.btnclosefrm.place(x=479, y=8)
        self.btnexit = Button(self.master, text="*", image=self.imgexit, command=self.Exit)
        self.btnexit.place(x=750, y=12)

    #Event
    def GetComboVal(self):
        count = []
        for i in range(1340, 1400):
            count.append(i)
        return count

    def GetIndexAge(self, x):
        count = []
        for i in range(1340, 1400):
            count.append(i)
        return (count.index(x))

    def ToggleUserPassFrame(self):
        if self.varIsAdmin.get() == 1:
            self.frmUserPass.place(x=0, y=250)
        else:
            self.frmUserPass.place_forget()

    def Register(self):
        key = "name,family,age,sex,is_admin"
        val = " '" + self.varName.get() + "','" + self.varFamily.get() + "'," + str(self.varAge.get()) + "," + str(
            self.varSex.get()) + "," + str(self.varIsAdmin.get()) + ""
        result = repository.Insert("tbl_user", key, val)
        if result:
            messagebox.showinfo(":)", "register is ok :)")
        else:
            messagebox.showerror(":(", "register is nokey :(")
        self.ClearTable()
        self.LoadTable()
        self.ClearForm()

    def LoadTable(self):
        result = repository.SelectAll("tbl_user", "*")
        for self.item in result:
            if self.item[4] == True:
                self.gender = "زن"
            else:
                self.gender = "مرد"
            self.admin = "مدیر" if self.item[5] else ""
            self.tbl.insert('', "end",
                            values=[self.admin, self.gender, self.item[3], self.item[2], self.item[1], self.item[0]])

    def LoadSearch(self, result):
        for self.item in result:
            if self.item[4] == True:
                self.gender = "زن"
            else:
                self.gender = "مرد"
            self.admin = "مدیر" if self.item[5] else ""
            self.tbl.insert('', "end",
                            values=[self.admin, self.gender, self.item[3], self.item[2], self.item[1], self.item[0]])

    def ClearTable(self):
        for item in self.tbl.get_children():
            sel = (str(item),)
            self.tbl.delete(sel)

    def ClearForm(self):
        list = [self.varName, self.varFamily, self.varUsername, self.varPassword]
        for item in list:
            item.set("")
        self.varIsAdmin.set(False)
        self.varSex.set(0)
        self.comboage.current(40)
        self.frmUserPass.place_forget()

    def GetSelectRow(self):
        self.selectionrow = self.tbl.selection()
        if self.selectionrow != ():
            id = self.tbl.item(self.selectionrow)["values"][5]
            self.varId.set(id)
            self.record = repository.SelectById("tbl_user", "*", "id='" + str(id) + "'")
            return self.record

    def GetSelection(self, e):
        self.record = self.GetSelectRow()
        if self.record != None:
            self.btnEdit.place(x=150, y=370)
            self.btnDelete.place(x=90, y=370)
            self.btnRegister.place_forget()
            self.btnCancel.place(x=30, y=370)
            self.varName.set(self.record[1])
            self.varFamily.set(self.record[2])
            self.comboage.current(self.GetIndexAge(self.record[3]))
            if self.record[4] == True:
                self.varSex.set(1)
            else:
                self.varSex.set(0)
            if self.record[5] == True:
                self.varIsAdmin.set(True)
                self.frmUserPass.place(x=0, y=250)
                querypass = repository.SelectById("tbl_userpass", "*", "user_id='" + str(self.record[0]) + "'")
                if querypass:
                    self.varUsername.set(querypass[1])
                    self.varPassword.set(querypass[2])
                else:
                    self.varUsername.set("")
                    self.varPassword.set("")
            else:
                self.varIsAdmin.set(False)
                self.frmUserPass.place_forget()

    def ClickCancel(self):
        self.btnEdit.place_forget()
        self.btnDelete.place_forget()
        self.btnCancel.place_forget()
        self.btnRegister.place(x=30, y=370)
        self.ClearForm()

    def ClickDelete(self):
        if self.varName.get() != "":
            result = messagebox.askquestion("هشدار", "آیا مطمئن هستید که میخواهید حذف کنید؟")
            if result == "yes":
                self.record = self.GetSelectRow()
                self.Delete(self.record)

    def Delete(self, rec):
        self.record = self.GetSelectRow()
        if self.record[5] == False:
            repository.Delete("tbl_user", "id='" + self.varId.get() + "'")
        else:
            repository.Delete("tbl_userpass", "user_id='" + self.varId.get() + "'")
            repository.Delete("tbl_user", "id='" + self.varId.get() + "'")
        self.ClearTable()
        self.LoadTable()

    def ClickEdit(self):
        self.record = self.GetSelectRow()
        set_clauseuser = (f"name = '{self.varName.get()}',"
                          f" family = '{self.varFamily.get()}',"
                          f" age = '{self.varAge.get()}',"
                          f" sex = '{self.varSex.get()}',"
                          f"is_admin = '{self.varIsAdmin.get()}'")
        if not self.record:
            messagebox.showerror("خطا...", "هیچ رکوردی انتخاب نشده است.")
        else:
            if self.record[5] == True:
                if self.varIsAdmin.get() == True:
                    if ((self.varUsername.get() == '') or (self.varPassword.get() == '')):
                        messagebox.showwarning("خطا...", "نام كاربري و كلمه عبور را وارد كن")
                    else:
                        usname = self.varUsername.get()
                        uspass = self.varPassword.get()
                        self.queryusername = repository.SelectByFeild("tbl_userpass", "*",
                                                                      "username='" + usname + "'")
                        if len(self.queryusername) == 1:
                            if self.queryusername[0][3] == int(self.varId.get()):
                                print(self.queryusername[0][3], "=", self.varId.get())
                                print("male khodeshe")
                                self.set_clause = f"username = '{usname}', password = '{uspass}'"
                                b = repository.Update("tbl_userpass", self.set_clause,
                                                      f"id = '{str(self.varId.get())}'")
                                result = repository.Update("tbl_user", set_clauseuser, f"id = '{self.varId.get()}'")
                                if (b == True) and (result == True):
                                    messagebox.showinfo("ok", "update id ok1")
                                    self.ClearTable()
                                    self.LoadTable()
                                    self.ClickCancel()
                            else:
                                messagebox.showwarning("خطا...", "نام کاربری تکراری است. یدونه هست")
                        elif len(self.queryusername) > 1:
                            messagebox.showwarning("خطا...", "نام کاربری تکراری است. بیشتر از یدونه هست")
                        else:
                            self.set_clause = f"username = '{usname}', password = '{uspass}'"
                            b = repository.Update("tbl_userpass", self.set_clause, f"id = '{str(self.varId.get())}'")
                            if (b == True):
                                self.EditUser(set_clauseuser)
                else:
                    d = repository.Delete("tbl_userpass", "user_id=" + str(self.varId.get()))
                    if d:
                        self.EditUser(set_clauseuser)
                    else:
                        messagebox.showwarning("خطا...", "مشکل پیش آمده کسکم!")
            else:  # self.record[5] == False
                if self.varIsAdmin.get() == True:
                    print("admin shode karbaret")
                    usname = self.varUsername.get()
                    uspass = self.varPassword.get()
                    self.queryusername = repository.SelectByFeild("tbl_userpass", "*", "username='" + usname + "'")
                    if len(self.queryusername) >= 1:
                        messagebox.showwarning("خطا...", "نام کاربری تکراری است. aaaa")
                    else:
                        val = "'" + usname + "','" + uspass + "'," + str(self.varId.get())
                        a = repository.Insert("tbl_userpass", "username,password,user_id", val)
                        if a:
                            self.EditUser(set_clauseuser)
                        else:
                            messagebox.showwarning("خطا...", "مشکل پیش آمده کسکم!")
                else:
                    self.EditUser(set_clauseuser)

    def EditUser(self, set_clauseuser):
        result = repository.Update("tbl_user", set_clauseuser, f"id = '{self.varId.get()}'")
        if (result == True):
            messagebox.showinfo("ok", "update id ok")
            self.ClearTable()
            self.LoadTable()
            self.ClickCancel()
        else:
            messagebox.showwarning("خطا...", "مشکل پیش آمده کسکم!")

    def ClickShowSearch(self):
        self.frmSearch.place(x=5, y=10)
        self.btnShowSearch.place_forget()

    def ClickCloseSearch(self):
        self.frmSearch.place_forget()
        self.btnShowSearch.place(x=475, y=20)
        self.ClearTable()
        self.LoadTable()

    def Search(self):
        if self.varSearch.get() == "":
            self.ClearTable()
            self.LoadTable()
        else:
            q = self.varSearch.get()
            if q == "زن":
                qs = "True"
            elif q == "مرد":
                qs = "False"
            else:
                qs = ""
            if q == "مدير":
                qr = "True"
            else:
                qr = ""
            if qs != "":
                where = "sex = '" + qs + "' "
            elif qr != "":
                where = "is_admin = '" + qr + "' "
            else:
                where = "name Like '%" + q + "%' or family Like '%" + q + "%' or age Like '%" + q + "%' "
            x = repository.Search("tbl_user", "*", where)
            print(str(x))
            self.ClearTable()
            self.LoadSearch(x)

    def Exit(self):
        messagebox.showinfo("", "خدانگهدار")
        self.master.destroy()  # بستن فايل
        os.system(f"python main.py")  # انتقال


if __name__ == "__main__":
    screen = Tk()
    screen.geometry("%dx%d+%d+%d" % (800, 500, 350, 30))
    screen.resizable = (False, False)
    screen.title("User Managment")
    pageMe = App(screen)
    screen.mainloop()
    pass
