from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import font as tkfont
import datetime
from PIL import Image, ImageTk
import bcrypt

from Backend.createtables import CreateTables
from Backend.employee import EmployeeDB

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        width = 1280
        height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.resizable(False,False)

        self.frames = {}
        for F in (Login, Register, AdminDashboard, EmployeeDashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="#FF80ED")
        self.controller = controller

        CreateTables()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        lblFrame = tk.LabelFrame(self,bg="#FF80ED")
        lblFrame.place(x=490,y=160,width=340, height=450)

        img1=Image.open("images/login.png").resize((100,100), Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=tk.Label(lblFrame,image=self.photoimage1,bg="#FF80ED", borderwidth=0)
        lblimg1.place(x=122, y=10, width=100,height=100)

        lblLogin=tk.Label(lblFrame,text="Login", font=("times new roman",20,"bold"),fg="black",bg="#FF80ED")
        lblLogin.place(x=130,y=120)

        # label
        lblusername=tk.Label(lblFrame,text="Username",font=("times new roman",15,"bold"),fg="black",bg="#FF80ED")
        lblusername.place(x=60,y=175)

        self.txtuser=ttk.Entry(lblFrame, textvariable=self.username,font=("times new roman",15,"bold"))
        self.txtuser.place(x=35,y=200,width=270)

        lblpassword=tk.Label(lblFrame,text="Password",font=("times new roman",15,"bold"),fg="black",bg="#FF80ED")
        lblpassword.place(x=60,y=245)

        self.txtpass=ttk.Entry(lblFrame, textvariable=self.password,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=35,y=270,width=270)

        # Icon Images
        img2=Image.open("images/login.png").resize((25,25), Image.ANTIALIAS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg2=tk.Label(lblFrame,image=self.photoimage2, bg="#FF80ED", borderwidth=0)
        lblimg2.place(x=35, y=173, width=25,height=25)

        img3=Image.open("images/lock.png").resize((25,25), Image.ANTIALIAS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg3=tk.Label(lblFrame,image=self.photoimage3, bg="#FF80ED", borderwidth=0)
        lblimg3.place(x=35, y=242, width=25,height=25)

        # Login Button
        btnLogin=tk.Button(lblFrame,text="Login",font=("times new roman",15,"bold"),bd=3,relief="ridge",fg="black",bg="#FF80ED", activeforeground="black",activebackground="#FF80ED",command=self.login)
        btnLogin.place(x=110,y=310,width=120,height=35)

        # Register Button
        btnRegist=tk.Button(lblFrame,text="New User Register",font=("times new roman",10,"bold"),borderwidth=0,fg="black",bg="#FF80ED", activeforeground="black",activebackground="#FF80ED",command=lambda: controller.show_frame("Register"))
        btnRegist.place(x=15,y=370,width=160)

        # Forget password Button
        btnForgetpw=tk.Button(lblFrame,text="Forget Password",font=("times new roman",10,"bold"),borderwidth=0,fg="black",bg="#FF80ED", activeforeground="black",activebackground="#FF80ED")
        btnForgetpw.place(x=10,y=390,width=160)

    def login(self):
        userfetch = (self.username.get())
        try:
            if self.username.get()=="":
                messagebox.showwarning("Warning","Username missing!.")
            elif self.password.get()=="":
                messagebox.showwarning("Warning","Password missing!.")
            elif self.username.get() and self.password.get():
                if EmployeeDB().fetch(userfetch) == None:
                    messagebox.showerror("Error","Invalid username or password. Please try again.")
                else:
                    if EmployeeDB().fetch(userfetch)[7] == 1:
                        messagebox.showerror("Error","Invalid username or password. Please try again.")
                    elif EmployeeDB().fetch(userfetch)[6] == 2:
                        messagebox.showerror("Error","Your account is pending.")
                    elif EmployeeDB().fetch(userfetch)[6] == 3:
                        messagebox.showerror("Error","Your account is locked.")
                    elif EmployeeDB().fetch(userfetch)[6] == 1 and EmployeeDB().fetch(userfetch)[5] == 1:
                        if bcrypt.checkpw(self.password.get().encode('utf8'), EmployeeDB().fetch(userfetch)[2].encode('utf8')):
                            self.controller.show_frame("AdminDashboard")
                            self.clear()
                        else:
                            messagebox.showerror("Error","Invalid username or password. Please try again.")
                    elif EmployeeDB().fetch(userfetch)[6] == 1 and EmployeeDB().fetch(userfetch)[5] == 2:
                        if bcrypt.checkpw(self.password.get().encode('utf8'), EmployeeDB().fetch(userfetch)[2].encode('utf8')):
                            self.controller.show_frame("EmployeeDashboard")
                            self.clear()
                        else:
                            messagebox.showerror("Error","Invalid username or password. Please try again.")

        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def clear(self):
        self.username.set("")
        self.password.set("")
class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="#FF80ED")

        # Set Variables
        self.firstname = tk.StringVar()
        self.lastname = tk.StringVar()
        self.phone = tk.StringVar()
        self.email = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.CFpassword = tk.StringVar()
        self.SQ = tk.StringVar()
        self.SA = tk.StringVar()

        # left image
        bg1=Image.open("images/Nailwall.jpg").resize((470,610), Image.ANTIALIAS)
        self.lblbg1=ImageTk.PhotoImage(bg1)
        lblLeft=tk.Label(self, image=self.lblbg1)
        lblLeft.place(x=50,y=50,width=470,height=610)

        # main Frame
        frame=tk.Frame(self,bg="white")
        frame.place(x=520,y=50,width=710,height=610)

        lblregist=tk.Label(frame,text="REGISTER HERE",font=("times new roman",25,"bold"),fg="darkgreen",bg="white")
        lblregist.place(x=20,y=20)

        # label and entry

        # =============Row1=============
        lblFname=tk.Label(frame,text="First Name",font=("times new roman",15,"bold"),bg="white")
        lblFname.place(x=50,y=100)

        txtFname=ttk.Entry(frame,textvariable=self.firstname,font=("times new roman",15))
        txtFname.place(x=50,y=130,width=250)

        lblLname=tk.Label(frame,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblLname.place(x=370,y=100)

        txtLname=ttk.Entry(frame,textvariable=self.lastname,font=("times new roman",15))
        txtLname.place(x=370,y=130,width=250)

        # =============Row2=============
        lblContact=tk.Label(frame,text="Contact No",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblContact.place(x=50,y=170)

        txtContact=ttk.Entry(frame,textvariable=self.phone,font=("times new roman",15))
        txtContact.place(x=50,y=200,width=250)

        lblEmail=tk.Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblEmail.place(x=370,y=170)

        txtEmail=ttk.Entry(frame,textvariable=self.email,font=("times new roman",15))
        txtEmail.place(x=370,y=200,width=250)

        # =============Row3=============
        lblDOB=tk.Label(frame,text="DOB",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblDOB.place(x=50,y=240)

        self.txtDOB=DateEntry(frame,selectmode='day',font=("times new roman",15),date_pattern='mm/dd/y')
        self.txtDOB.pack()
        self.txtDOB.place(x=50,y=270,width=250)

        lblAddress=tk.Label(frame,text="Address",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblAddress.place(x=370,y=240)

        self.txtAddress=tk.Text(frame,font=("times new roman",15),bg="lightyellow")
        self.txtAddress.place(x=370,y=270,width=250,height=97)

        lblUsername=tk.Label(frame,text="Username",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblUsername.place(x=50,y=310)

        txtUsername=ttk.Entry(frame,textvariable=self.username,font=("times new roman",15))
        txtUsername.place(x=50,y=340,width=250)

        # =============Row4=============
        def show():
            txtPassword.config(show="")
            txtConfirmPw.config(show="")
            
        def hide():
            txtPassword.config(show="*")
            txtConfirmPw.config(show="*")

        lblPassword=tk.Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblPassword.place(x=50,y=380)

        txtPassword=ttk.Entry(frame,textvariable=self.password,font=("times new roman",15),show="*")
        txtPassword.place(x=50,y=410,width=250)

        lblConfirmPw=tk.Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblConfirmPw.place(x=370,y=380)

        txtConfirmPw=ttk.Entry(frame,textvariable=self.CFpassword,font=("times new roman",15),show="*")
        txtConfirmPw.place(x=370,y=410,width=250)

        imgVisible=Image.open("images/visible.png").resize((35,35),Image.ANTIALIAS)
        self.photoimageVisible=ImageTk.PhotoImage(imgVisible)
        toggle_btn = tk.Button(frame,image=self.photoimageVisible,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="white",activebackground="white")
        toggle_btn.place(x=625,y=405)
        toggle_btn.bind("<ButtonPress>", lambda event:show())
        toggle_btn.bind("<ButtonRelease>", lambda event:hide())

        # =============Row5=============
        lblSecurityQ=tk.Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblSecurityQ.place(x=50,y=450)

        self.txtSecurityQ=ttk.Combobox(frame,textvariable=self.SQ,font=("times new roman",15,"bold"),state="readonly",justify="center")
        self.txtSecurityQ["values"]=("Select","Your Birth Place","Your Girlfriend name","Your Pet Name")
        self.txtSecurityQ.place(x=50,y=480,width=250)
        self.txtSecurityQ.current(0)

        lblSecurityA=tk.Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblSecurityA.place(x=370,y=450)

        txtSecurityA=ttk.Entry(frame,textvariable=self.SA,font=("times new roman",15))
        txtSecurityA.place(x=370,y=480,width=250)

        # =============Row6=============
        imgRegist=Image.open("images/Registerbtn.png").resize((200,55),Image.ANTIALIAS)
        self.photoimageRegist=ImageTk.PhotoImage(imgRegist)
        Registerbtn=tk.Button(frame, image=self.photoimageRegist,command=self.add,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="white",activebackground="white")
        Registerbtn.place(x=70,y=540,width=210)

        imgLogin=Image.open("images/Loginbtn.png").resize((200,60),Image.ANTIALIAS)
        self.photoimageLogin=ImageTk.PhotoImage(imgLogin)
        Registerbtn=tk.Button(frame, image=self.photoimageLogin,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="white",activebackground="white",command=lambda: controller.show_frame("Login"))
        Registerbtn.place(x=400,y=537,width=210,height=60)

    def add(self):
        userfetch = (self.username.get())
        role_id = 2
        account_status_id = 2
        activeAccount = 0

        employee_status_id = 1
        activeEmployee = 0
 
        try:
            if self.firstname.get()=="" \
                or self.lastname.get()=="" \
                or self.phone.get()=="" \
                or self.email.get()=="" \
                or self.txtDOB.get_date()=="" \
                or len(self.txtAddress.get("1.0",END))==1 \
                or self.username.get()=="" \
                or self.password.get()=="" \
                or self.CFpassword.get()=="" \
                or self.SQ.get()=="Select" \
                or self.SA.get()=="" :
                messagebox.showerror("Error","All Asterisks are required.")
            elif self.phone.get().isnumeric() == False:
                messagebox.showerror("Error","Contact contains numbers only.")
            elif self.txtDOB.get_date() == datetime.datetime.now().date():
                messagebox.showerror("Error","Invalid Date of Birth")
            elif self.password.get() != self.CFpassword.get():
                messagebox.showerror("Error","Your password and confirmation password do not match.")
            elif self.username.get() and self.firstname.get() and self.lastname.get():
                if EmployeeDB().fetch(userfetch)!=None:
                    messagebox.showwarning("Warning","User Already Exists")
                else:
                    password=self.password.get().encode('utf8')
                    hashedpassword=bcrypt.hashpw(password, bcrypt.gensalt())
                    secret_answer=self.SA.get().encode('utf8')
                    SAhased=bcrypt.hashpw(secret_answer, bcrypt.gensalt())
                    account=(self.username.get(),hashedpassword,self.SQ.get(),SAhased,role_id,account_status_id,activeAccount)
                    EmployeeDB().insertAccount(account)

                    account_id=EmployeeDB().fetch(userfetch)
                    employee=(self.firstname.get(),self.lastname.get(),self.txtDOB.get_date(),self.phone.get(),self.email.get(),self.txtAddress.get("1.0",END),employee_status_id,account_id[0],activeEmployee)
                    EmployeeDB().insertEmployee(employee)
                    
                    op=messagebox.showinfo("Success","Register Successfully!")
                    self.clear()
                    
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def clear(self):
        self.firstname.set("")
        self.lastname.set("")
        self.phone.set("")
        self.email.set("")
        self.txtDOB.set_date(datetime.datetime.now().date())
        self.txtAddress.delete("1.0",END)
        self.username.set("")
        self.password.set("")
        self.CFpassword.set("")
        self.txtSecurityQ.current(0)
        self.SA.set("")

class AdminDashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="#FF80ED")

class EmployeeDashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="yellow")

if __name__ == "__main__":
    app = App()
    app.mainloop()