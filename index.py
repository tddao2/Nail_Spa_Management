from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkinter import font as tkfont
import datetime
import time
from PIL import Image, ImageTk
import bcrypt
import phonenumbers
import re

from Backend.createtables import CreateTables
from Backend.admin import AdminDB
from Backend.feedback import FeedbackDB
from Backend.Database.employee import EmployeeDB
# from Backend.Database.feedback import FeedbackDB

# Database context
# employeeDB = EmployeeDB()
# feedbackDB = FeedbackDB()

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("KT Nails Spa")

        # Reference: https://blog.teclado.com/side-values-in-tkinters-pack-geometry-manager/
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        width = 1350  # 1280
        height = 720

        # Return screen width and height in pixels.
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
        self.resizable(False, False)

        # Initializing an empty frame array.
        self.frames = {}
        for F in (Login, Register, Feedback, AdminDashboard, EmployeeDashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Display the current page
        self.show_frame("Login")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="#e2479c")
        self.controller = controller

        CreateTables()

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        lblFrame = tk.LabelFrame(self,bg="#e2479c")
        lblFrame.place(x=525,y=160,width=340, height=450)

        img1=Image.open("images/login.png").resize((100,100), Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        lblimg1=tk.Label(lblFrame,image=self.photoimage1,bg="#e2479c", borderwidth=0)
        lblimg1.place(x=122, y=10, width=100,height=100)

        lblLogin=tk.Label(lblFrame,text="Login", font=("times new roman",20,"bold"),fg="black",bg="#e2479c")
        lblLogin.place(x=130,y=120)

        # label
        lblusername=tk.Label(lblFrame,text="Username",font=("times new roman",15,"bold"),fg="black",bg="#e2479c")
        lblusername.place(x=60,y=175)

        self.txtuser=ttk.Entry(lblFrame, textvariable=self.username,font=("times new roman",15,"bold"))
        self.txtuser.place(x=35,y=200,width=270)

        lblpassword=tk.Label(lblFrame,text="Password",font=("times new roman",15,"bold"),fg="black",bg="#e2479c")
        lblpassword.place(x=60,y=245)

        self.txtpass=ttk.Entry(lblFrame, textvariable=self.password,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=35,y=270,width=270)

        # Icon Images
        img2=Image.open("images/login.png").resize((25,25), Image.ANTIALIAS)
        self.photoimage2=ImageTk.PhotoImage(img2)
        lblimg2=tk.Label(lblFrame,image=self.photoimage2, bg="#e2479c", borderwidth=0)
        lblimg2.place(x=35, y=173, width=25,height=25)

        img3=Image.open("images/lock.png").resize((25,25), Image.ANTIALIAS)
        self.photoimage3=ImageTk.PhotoImage(img3)
        lblimg3=tk.Label(lblFrame,image=self.photoimage3, bg="#e2479c", borderwidth=0)
        lblimg3.place(x=35, y=242, width=25,height=25)

        # Login Button
        btnLogin=tk.Button(lblFrame,text="Login",font=("times new roman",15,"bold"),bd=3,relief="ridge",fg="black",bg="#e2479c", activeforeground="black",activebackground="#e2479c",command=self.login)
        btnLogin.place(x=110,y=310,width=120,height=35)

        # Register Button
        btnRegist=tk.Button(lblFrame,text="New User Register",font=("times new roman",10,"bold"),borderwidth=0,fg="black",bg="#e2479c", activeforeground="black",activebackground="#e2479c",command=lambda: controller.show_frame("Register"))
        btnRegist.place(x=15,y=370,width=160)

        # Forget password Button
        btnForgetpw=tk.Button(lblFrame,text="Forget Password",font=("times new roman",10,"bold"),borderwidth=0,fg="black",bg="#e2479c", activeforeground="black",activebackground="#e2479c")
        btnForgetpw.place(x=10,y=390,width=160)

        # Feedback Button
        btnFeedback = tk.Button(lblFrame, text="Feedback", font=("times new roman",10,"bold"), borderwidth=0, fg="black", bg="#FF80ED", activeforeground="black",activebackground="#e2479c", command=lambda: controller.show_frame("Feedback"))
        btnFeedback.place(x=15, y=420, width=160)

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
        self.config(bg="#e2479c")

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
        lblLeft.place(x=85,y=50,width=470,height=610)

        # main Frame
        frame=tk.Frame(self,bg="white")
        frame.place(x=555,y=50,width=710,height=610)

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
        self.config(bg="#e2479c")

        AMframe=tk.Frame(self,bg="#e2479c")
        AMframe.place(x=0,y=0,width=1350,height=720)

        LeftFrame=tk.Frame(AMframe,bg="#e2479c",relief=RIDGE)
        LeftFrame.place(x=0,y=0,width=100,height=720)

        imageHome = Image.open("images/home.png").resize((100,100))
        self.imageHome=ImageTk.PhotoImage(imageHome)
        HomeBtn=tk.Button(LeftFrame, image=self.imageHome,borderwidth=0,activebackground="#e2479c",bg="#e2479c")
        HomeBtn.grid(row=0,column=1)

        imageEmployee = Image.open("images/employee.png").resize((100,100))
        self.imageEmployee=ImageTk.PhotoImage(imageEmployee)
        EmployeeBtn=tk.Button(LeftFrame, image=self.imageEmployee,borderwidth=0,activebackground="#e2479c",bg="#e2479c",command=self.employee)
        EmployeeBtn.grid(row=1,column=1)

        imageCustomer = Image.open("images/client.png").resize((100,100))
        self.imageCustomer=ImageTk.PhotoImage(imageCustomer)
        CustomerBtn=tk.Button(LeftFrame, image=self.imageCustomer,borderwidth=0,activebackground="#e2479c",bg="#e2479c",command=self.client)
        CustomerBtn.grid(row=2,column=1)

        imageSale = Image.open("images/sale.png").resize((100,100))
        self.imageSale=ImageTk.PhotoImage(imageSale)
        SaleBtn=tk.Button(LeftFrame, image=self.imageSale,borderwidth=0,activebackground="#e2479c",bg="#e2479c",command=self.sale)
        SaleBtn.grid(row=3,column=1)

        imageReport = Image.open("images/Report.png").resize((100,100))
        self.imageReport=ImageTk.PhotoImage(imageReport)
        ReportBtn=tk.Button(LeftFrame, image=self.imageReport,borderwidth=0,activebackground="#e2479c",bg="#e2479c")
        ReportBtn.grid(row=4,column=1)

        imageFeedback = Image.open("images/feedback.png").resize((100,100))
        self.imageFeedback=ImageTk.PhotoImage(imageFeedback)
        FeedbackBtn=tk.Button(LeftFrame, image=self.imageFeedback,borderwidth=0,activebackground="#e2479c",bg="#e2479c")
        FeedbackBtn.grid(row=5,column=1)

        # imagelogout = Image.open("images/logout.png").resize((100,100))
        # self.imagelogout=ImageTk.PhotoImage(imagelogout)
        # logoutBtn=tk.Button(LeftFrame, image=self.imagelogout,borderwidth=0,activebackground="#e2479c",bg="#e2479c")
        # logoutBtn.grid(row=6,column=1)

        imageusers = Image.open("images/users.png").resize((100,100))
        self.imageusers=ImageTk.PhotoImage(imageusers)
        usersBtn=tk.Button(LeftFrame, image=self.imageusers,borderwidth=0,activebackground="#e2479c",bg="#e2479c",command=self.user)
        usersBtn.grid(row=6,column=1)

        def clock():
            hour=time.strftime("%I")
            minute=time.strftime("%M")
            second=time.strftime("%S")
            locale=time.strftime("%p")

            abbDay=time.strftime("%a")
            day=time.strftime("%d")
            month=time.strftime("%b")
            year=time.strftime("%Y")
            lbl_clock.config(text="Welcome to Nail & Spa Management System\t\t Date: "+abbDay+", "+day+" "+month+" "+year+"\t\t Time: "+hour+":"+minute+":"+second+" "+locale)
            lbl_clock.after(1000,clock)
        lbl_clock=tk.Label(AMframe, text="",font=("times new roman",15),bg="#e2479c",fg="white")
        lbl_clock.place(x=100,y=0,relwidth=1,height=30)
        clock()

        self.EmpFrame=tk.Frame(self,relief=RIDGE,bd=1,bg="#e2479c")
        self.ClientFrame=tk.Frame(self,relief=RIDGE,bd=1 ,bg="red")
        self.SaleFrame=tk.Frame(self,relief=RIDGE,bd=1 ,bg="yellow")
        self.UserFrame=tk.Frame(self,relief=RIDGE,bd=1,bg="#e2479c")

    def employee(self):
        self.hide_all_frames()
        self.EmpFrame.place(x=100,y=30,width=1251,height=690)

        style = ttk.Style()
        # style.theme_use('clam')
        style.configure('Treeview.Heading',font=("times new roman",15,"bold"),foreground="black")
        style.map('Treeview',background=[('selected','#e2479c')])

        self.var_searchby=tk.StringVar()
        self.var_searchtxt=tk.StringVar()

        self.var_emp_id=tk.StringVar()
        self.var_fname=tk.StringVar()
        self.var_lname=tk.StringVar()
        self.var_contact=tk.StringVar()
        self.var_status=tk.StringVar()
        self.var_email=tk.StringVar()

        # =============Left Frame=============
        LeftFrame=tk.LabelFrame(self.EmpFrame,text="Employee Details",relief=RIDGE,font=("times new roman",15),bd=1,bg="#e2479c",fg="white")
        LeftFrame.place(x=0,y=0,width=370,height=690)

        lblEmpId=tk.Label(LeftFrame,text="Emp ID",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblEmpId.place(x=15,y=20)

        txtEmpId=ttk.Entry(LeftFrame,textvariable=self.var_emp_id,font=("times new roman",18),state=DISABLED) # ,state=DISABLED
        txtEmpId.place(x=140,y=20,width=200)

        lblFname=tk.Label(LeftFrame,text="First Name",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblFname.place(x=15,y=80)

        txtFname=ttk.Entry(LeftFrame,textvariable=self.var_fname,font=("times new roman",18))
        txtFname.place(x=140,y=80,width=200)

        lblLname=tk.Label(LeftFrame,text="Last Name",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblLname.place(x=15,y=140)

        txtLname=ttk.Entry(LeftFrame,textvariable=self.var_lname,font=("times new roman",18))
        txtLname.place(x=140,y=140,width=200)

        lblDOB=tk.Label(LeftFrame,text="DOB",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblDOB.place(x=15,y=200)

        self.txtDOB=DateEntry(LeftFrame,selectmode='day',font=("times new roman",18),date_pattern='mm/dd/y')
        # self.txtDOB.pack()
        self.txtDOB.place(x=140,y=200,width=200)

        lblEmail=tk.Label(LeftFrame,text="Email",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblEmail.place(x=15,y=260)

        txtEmail=ttk.Entry(LeftFrame,textvariable=self.var_email,font=("times new roman",14))
        txtEmail.place(x=140,y=260,width=200,height=33)

        lblPhone=tk.Label(LeftFrame,text="Phone",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblPhone.place(x=15,y=320)

        txtPhone=ttk.Entry(LeftFrame,textvariable=self.var_contact,font=("times new roman",18))
        txtPhone.place(x=140,y=320,width=200)

        lblStatus=tk.Label(LeftFrame,text="Status",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblStatus.place(x=15,y=380)

        self.txtStatus=ttk.Combobox(LeftFrame,textvariable=self.var_status,font=("times new roman",18,"bold"),state="readonly",justify="center")
        self.txtStatus["values"]=("Select","New","Current","Pass")
        self.txtStatus.place(x=140,y=380,width=200)
        self.txtStatus.current(0)

        lblAddress=tk.Label(LeftFrame,text="Address",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblAddress.place(x=15,y=440)

        self.txtAddress=tk.Text(LeftFrame,font=("times new roman",14),bg="white")
        self.txtAddress.place(x=140,y=440,width=200,height=100)

        imgUpdate=Image.open("images/update.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageUpdate=ImageTk.PhotoImage(imgUpdate)
        Updatebtn=tk.Button(LeftFrame, image=self.photoimageUpdate,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.EmpUpdate)
        Updatebtn.place(x=20,y=575,width=80)

        imgDelete=Image.open("images/delete.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageDelete=ImageTk.PhotoImage(imgDelete)
        Deletebtn=tk.Button(LeftFrame, image=self.photoimageDelete,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.EmpDelete)
        Deletebtn.place(x=148,y=575,width=80)

        imgRefresh=Image.open("images/refresh.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageRefresh=ImageTk.PhotoImage(imgRefresh)
        Refreshbtn=tk.Button(LeftFrame, image=self.photoimageRefresh,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.EmpClear)
        Refreshbtn.place(x=275,y=575,width=80)

        # ==========================================================Right Frame=============================================================
        RightFrame=tk.LabelFrame(self.EmpFrame,relief=RIDGE,bd=1,bg="#e2479c")
        RightFrame.place(x=370,y=12,width=880,height=678)

        # =============Top Right Frame=============
        SearchFrame=tk.LabelFrame(RightFrame,text="Search Employee",relief=RIDGE,font=("times new roman",15),bd=4,bg="#e2479c",fg="white")
        SearchFrame.place(x=100,width=680,height=71) #550

        self.cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,state="readonly",justify=CENTER,font=("times new roman",18))
        self.cmb_search["values"]=("Select","first_name","last_name","birthday","phone")
        self.cmb_search.place(x=15,y=2,width=180)
        self.cmb_search.current(0)

        txt_search=tk.Entry(SearchFrame,textvariable=self.var_searchtxt,font=("times new roman",18),bg="white")
        txt_search.place(x=215,y=2) #10

        imgSearch=Image.open("images/search.png").resize((38,38),Image.ANTIALIAS)
        self.photoimageSearch=ImageTk.PhotoImage(imgSearch)
        # Searchbtn=tk.Button(LeftFrame, image=self.photoimageSearch,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        # Searchbtn.place(x=275,y=580,width=80)
        btn_search=tk.Button(SearchFrame,image=self.photoimageSearch,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.EmpSearch)
        btn_search.place(x=465)

        btn_showHistory=tk.Button(SearchFrame,text="History Records",relief=RIDGE,font=("times new roman",14,"bold"),bd=2,cursor="hand2",bg="#e2479c",fg="white",activebackground="#e2479c",activeforeground="white",command=self.EmpHistory)
        btn_showHistory.place(x=510,width=150)

        
        # =============Bottom Right Frame=============
        EmpTableFrame=tk.LabelFrame(RightFrame,relief=RIDGE,bd=1,bg="white")
        EmpTableFrame.place(y=72,width=879,height=604) #608

        scrollx=tk.Scrollbar(EmpTableFrame,orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM,fill=X)

        scrolly=tk.Scrollbar(EmpTableFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.EmployeeTable=ttk.Treeview(EmpTableFrame,columns=("ID","fname","lname","dob","email","contact","address","status"),
                                        yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,
                                        show='headings')

        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("ID",text="ID")
        self.EmployeeTable.heading("fname",text="First Name")
        self.EmployeeTable.heading("lname",text="Last Name")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("status",text="Status")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("ID",anchor=CENTER)
        self.EmployeeTable.column("fname",anchor=CENTER)
        self.EmployeeTable.column("lname",anchor=CENTER)
        self.EmployeeTable.column("dob",anchor=CENTER)
        self.EmployeeTable.column("email",anchor=CENTER)
        self.EmployeeTable.column("contact",anchor=CENTER)
        self.EmployeeTable.column("address",anchor=CENTER)
        self.EmployeeTable.column("status",anchor=CENTER)

        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.EmpGetdata)

        self.EmpShow()
      
    def client(self):
        self.hide_all_frames()
        self.ClientFrame.place(x=200,y=30,width=1250,height=690)

    def sale(self):
        self.hide_all_frames()
        self.SaleFrame.place(x=250,y=30,width=1250,height=690)
    
    def user(self):
        self.hide_all_frames()
        self.UserFrame.place(x=100,y=30,width=1251,height=690)

        style = ttk.Style()
        # style.theme_use('clam')
        style.configure('Treeview.Heading',font=("times new roman",15,"bold"),foreground="black")
        style.map('Treeview',background=[('selected','#e2479c')])

        self.var_Acctsearchby=tk.StringVar()
        self.var_Acctsearchtxt=tk.StringVar()

        self.var_acct_id=tk.StringVar()
        self.var_username=tk.StringVar()
        self.var_rolename=tk.StringVar()
        self.var_Acctstatus=tk.StringVar()

        # =============Left Frame=============
        LeftFrame=tk.LabelFrame(self.UserFrame,text="Account Details",relief=RIDGE,font=("times new roman",15),bd=1,bg="#e2479c",fg="white")
        LeftFrame.place(x=0,y=0,width=370,height=689)

        lblAcctId=tk.Label(LeftFrame,text="Account ID",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblAcctId.place(x=15,y=20)

        txtAcctId=ttk.Entry(LeftFrame,textvariable=self.var_acct_id,font=("times new roman",18),state=DISABLED) # ,state=DISABLED
        txtAcctId.place(x=140,y=20,width=200)

        lblUsername=tk.Label(LeftFrame,text="User Name",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblUsername.place(x=15,y=80)

        txtUsername=ttk.Entry(LeftFrame,textvariable=self.var_username,font=("times new roman",18),state=DISABLED)
        txtUsername.place(x=140,y=80,width=200)

        lblRoleName=tk.Label(LeftFrame,text="Role",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblRoleName.place(x=15,y=140)

        self.txtRoleName=ttk.Combobox(LeftFrame,textvariable=self.var_rolename,font=("times new roman",18,"bold"),state="readonly",justify="center")
        self.txtRoleName["values"]=("Select","Admin","User")
        self.txtRoleName.place(x=140,y=140,width=200)
        self.txtRoleName.current(0)

        lblAcctStatus=tk.Label(LeftFrame,text="Status",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblAcctStatus.place(x=15,y=200)

        self.txtAcctStatus=ttk.Combobox(LeftFrame,textvariable=self.var_Acctstatus,font=("times new roman",18,"bold"),state="readonly",justify="center")
        self.txtAcctStatus["values"]=("Select","active","inactive","pending")
        self.txtAcctStatus.place(x=140,y=200,width=200)
        self.txtAcctStatus.current(0)

        imgAcctUpdate=Image.open("images/update.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageAcctUpdate=ImageTk.PhotoImage(imgAcctUpdate)
        AcctUpdatebtn=tk.Button(LeftFrame, image=self.photoimageAcctUpdate,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.AcctUpdate)
        AcctUpdatebtn.place(x=20,y=575,width=80)

        # imgAcctDelete=Image.open("images/delete.png").resize((80,80),Image.ANTIALIAS)
        # self.photoimageAcctDelete=ImageTk.PhotoImage(imgAcctDelete)
        # AcctDeletebtn=tk.Button(LeftFrame, image=self.photoimageAcctDelete,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        # AcctDeletebtn.place(x=148,y=575,width=80)

        imgAcctRefresh=Image.open("images/refresh.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageAcctRefresh=ImageTk.PhotoImage(imgAcctRefresh)
        AcctRefreshbtn=tk.Button(LeftFrame, image=self.photoimageAcctRefresh,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.AcctClear)
        AcctRefreshbtn.place(x=275,y=575,width=80)

        # ==========================================================Right Frame=============================================================
        RightFrame=tk.Frame(self.UserFrame,relief=RIDGE,bd=1,bg="#e2479c")
        RightFrame.place(x=370,y=12,width=880,height=678)

        # =============Top Right Frame=============
        SearchFrame=tk.LabelFrame(RightFrame,text="Search Account",relief=RIDGE,font=("times new roman",15),bd=4,bg="#e2479c",fg="white")
        SearchFrame.place(x=100,width=680,height=71) #550

        self.Acctcmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_Acctsearchby,state="readonly",justify=CENTER,font=("times new roman",18))
        self.Acctcmb_search["values"]=("Select","first_name","last_name","username","acct_status")
        self.Acctcmb_search.place(x=15,y=2,width=180)
        self.Acctcmb_search.current(0)

        txt_Acctsearch=tk.Entry(SearchFrame,textvariable=self.var_Acctsearchtxt,font=("times new roman",18),bg="white")
        txt_Acctsearch.place(x=215,y=2) #10

        imgSearch=Image.open("images/search.png").resize((38,38),Image.ANTIALIAS)
        self.photoimageSearch=ImageTk.PhotoImage(imgSearch)
        btn_search=tk.Button(SearchFrame,image=self.photoimageSearch,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.AcctSearch)
        btn_search.place(x=465)

        btn_showHistory=tk.Button(SearchFrame,text="Show All",relief=RIDGE,font=("times new roman",14,"bold"),bd=2,cursor="hand2",bg="#e2479c",fg="white",activebackground="#e2479c",activeforeground="white",command=self.AcctShowAll)
        btn_showHistory.place(x=510,width=150)

        # =============Bottom Right Frame=============
        AcctTableFrame=tk.LabelFrame(RightFrame,relief=RIDGE,bd=1,bg="white")
        AcctTableFrame.place(y=72,width=879,height=604) #608

        scrollx=tk.Scrollbar(AcctTableFrame,orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM,fill=X)

        scrolly=tk.Scrollbar(AcctTableFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.AccountTable=ttk.Treeview(AcctTableFrame,columns=("ID","Full name","username","role","status"),
                                        yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,
                                        show='headings')

        scrollx.config(command=self.AccountTable.xview)
        scrolly.config(command=self.AccountTable.yview)

        self.AccountTable.heading("ID",text="ID")
        self.AccountTable.heading("Full name",text="Full name")
        self.AccountTable.heading("username",text="User name")
        self.AccountTable.heading("role",text="Role")
        self.AccountTable.heading("status",text="Status")
        

        self.AccountTable["show"]="headings"

        self.AccountTable.column("ID",anchor=CENTER)
        self.AccountTable.column("Full name",anchor=CENTER)
        self.AccountTable.column("username",anchor=CENTER)
        self.AccountTable.column("role",anchor=CENTER)
        self.AccountTable.column("status",anchor=CENTER)
        

        self.AccountTable.pack(fill=BOTH,expand=1)
        self.AccountTable.bind("<ButtonRelease-1>",self.AcctGetdata)

        self.AcctShow()

    def hide_all_frames(self):
        self.EmpFrame.place_forget()
        self.ClientFrame.place_forget()
        self.SaleFrame.place_forget()
        self.UserFrame.place_forget()

    def EmpUpdate(self):
        emp_status_New = 1
        emp_status_Current = 2
        emp_status_Pass = 3
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","No employee info selected")
            elif self.var_fname.get()=="":
                messagebox.showerror("Error","First Name missing")
            elif self.var_lname.get()=="":
                messagebox.showerror("Error","Last Name missing")
            elif self.var_lname.get()=="":
                messagebox.showerror("Error","Last Name missing")
            elif self.txtDOB.get_date()==datetime.datetime.now().date():
                messagebox.showerror("Error","Invalid Date of Birth")
            # elif self.var_email.get()=="":
            #     messagebox.showerror("Error","Email missing")
            elif self.var_contact.get()=="":
                messagebox.showerror("Error","Phone missing")
            elif self.var_status.get()=="Select":
                messagebox.showerror("Error","Status missing")
            elif len(self.txtAddress.get("1.0",END))==1:
                messagebox.showerror("Error","Address missing")
            else:
                if self.var_status.get()=="New":
                    FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.var_contact.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                    data=(self.var_fname.get(),self.var_lname.get(),self.txtDOB.get_date(),self.var_email.get(),FormatedPhone,self.txtAddress.get("1.0",END),emp_status_New,self.var_emp_id.get())
                    AdminDB().EmpUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.EmpClear()
                elif self.var_status.get()=="Current":
                    FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.var_contact.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                    data=(self.var_fname.get(),self.var_lname.get(),self.txtDOB.get_date(),self.var_email.get(),FormatedPhone,self.txtAddress.get("1.0",END),emp_status_Current,self.var_emp_id.get())
                    AdminDB().EmpUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.EmpClear()
                elif self.var_status.get()=="Pass":
                    FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.var_contact.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                    data=(self.var_fname.get(),self.var_lname.get(),self.txtDOB.get_date(),self.var_email.get(),FormatedPhone,self.txtAddress.get("1.0",END),emp_status_Pass,self.var_emp_id.get())
                    AdminDB().EmpUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.EmpClear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")
    
    def EmpDelete(self):
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","No employee info selected")
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?")
                if op==True:
                    data = self.var_emp_id.get()
                    AdminDB().EmpDelete(data)
                    messagebox.showinfo("Success","Delete Successfully!")
                    self.EmpClear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")
    
    def EmpSearch(self):
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select search by option")
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input is required")
            elif self.var_searchby.get()=="phone" and self.var_searchtxt.get():
                FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.var_searchtxt.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                data=(self.var_searchby.get(),FormatedPhone)
                rows = AdminDB().EmpSearch(data)
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found.")
            else:
                data=(self.var_searchby.get(),self.var_searchtxt.get())
                rows = AdminDB().EmpSearch(data)
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found.")
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def EmpHistory(self):
        try:
            rows = AdminDB().EmpFetchHistory()
            if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert("",END,values=row)
            else:
                messagebox.showerror("Error","No record found.")
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def EmpClear(self):
        self.var_emp_id.set("")
        self.var_fname.set("")
        self.var_lname.set("")
        self.txtDOB.set_date(datetime.datetime.now().date())
        self.var_email.set("")
        self.var_contact.set("")
        self.txtAddress.delete("1.0",END)
        self.txtStatus.current(0)
        self.cmb_search.current(0)
        self.var_searchtxt.set("")

        self.EmpShow()

    def EmpShow(self):
        self.EmployeeTable.delete(*self.EmployeeTable.get_children())
        try:
            if not AdminDB().EmpFetch():
                messagebox.showerror("Error", "No records found.")
            else:
                for row in AdminDB().EmpFetch():
                    self.EmployeeTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def EmpGetdata(self,event):
        f=self.EmployeeTable.focus()
        curItem=(self.EmployeeTable.item(f))
        row=curItem['values']

        try:
            self.var_emp_id.set(row[0])
            self.var_fname.set(row[1])
            self.var_lname.set(row[2])
            self.txtDOB.set_date(datetime.datetime.strptime(str(row[3]), '%Y-%m-%d').strftime('%m/%d/%Y'))
            self.var_email.set(row[4])
            # self.var_contact.set(row[5])
            self.var_contact.set(re.sub('[^A-Za-z0-9]+', '', str(row[5])))
            self.txtAddress.delete("1.0",END)
            self.txtAddress.insert(END,row[6])
            self.txtStatus.set(row[7])
        except:
            pass

    def AcctUpdate(self):
        Role_Admin = 1
        Role_User = 2
        Acct_Status_active = 1
        Acct_Status_pending = 2
        Acct_Status_inactive = 3
        try:
            if self.var_acct_id.get()=="":
                messagebox.showerror("Error","No account info selected")
            elif self.var_rolename.get()=="Select":
                messagebox.showerror("Error","Role is missing")
            elif self.var_Acctstatus.get()=="Select":
                messagebox.showerror("Error","Status is missing")
            else:
                if self.var_rolename.get()=="User" and self.var_Acctstatus.get()=="active":
                    data=(Role_User, Acct_Status_active, self.var_acct_id.get())
                    AdminDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="User" and self.var_Acctstatus.get()=="pending":
                    data=(Role_User, Acct_Status_pending, self.var_acct_id.get())
                    AdminDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="User" and self.var_Acctstatus.get()=="inactive":
                    data=(Role_User, Acct_Status_inactive, self.var_acct_id.get())
                    AdminDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="Admin" and self.var_Acctstatus.get()=="active":
                    data=(Role_Admin, Acct_Status_active, self.var_acct_id.get())
                    AdminDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="Admin" and self.var_Acctstatus.get()=="pending":
                    data=(Role_Admin, Acct_Status_pending, self.var_acct_id.get())
                    AdminDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="Admin" and self.var_Acctstatus.get()=="inactive":
                    data=(Role_Admin, Acct_Status_inactive, self.var_acct_id.get())
                    AdminDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def AcctSearch(self):
        try:
            if self.var_Acctsearchby.get()=="Select":
                messagebox.showerror("Error","Select search by option")
            elif self.var_Acctsearchtxt.get()=="":
                messagebox.showerror("Error","Search input is required")
            else:
                data=(self.var_Acctsearchby.get(),self.var_Acctsearchtxt.get())
                rows = AdminDB().AcctSearch(data)
                if len(rows)!=0:
                    self.AccountTable.delete(*self.AccountTable.get_children())
                    for row in rows:
                        self.AccountTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found.")
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def AcctClear(self):
        self.var_acct_id.set("")
        self.var_username.set("")
        self.txtRoleName.current(0)
        self.txtAcctStatus.current(0)

        self.AcctShow()

    def AcctShow(self):
        self.AccountTable.delete(*self.AccountTable.get_children())
        try:
            if not AdminDB().AcctFetch():
                messagebox.showerror("Error", "No records found.")
            else:
                for row in AdminDB().AcctFetch():
                    self.AccountTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def AcctShowAll(self):
        self.AccountTable.delete(*self.AccountTable.get_children())
        try:
            if not AdminDB().AcctFetchAll():
                messagebox.showerror("Error", "No records found.")
            else:
                for row in AdminDB().AcctFetchAll():
                    self.AccountTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def AcctGetdata(self,event):
        f=self.AccountTable.focus()
        curItem=(self.AccountTable.item(f))
        row=curItem['values']

        try:
            self.var_acct_id.set(row[0])
            self.var_username.set(row[2])
            self.var_rolename.set(row[3])
            self.var_Acctstatus.set(row[4])
        except:
            pass

class EmployeeDashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="yellow")

# Feedback Window
class Feedback(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Background color
        self.config(bg="#e2479c")

        # Create widgets
        self.create_widgets(controller)


    def create_widgets(self, controller):

        # self.employeeName = tk.StringVar()
        # self.performanceScore = tk.IntVar()
        # self.description = tk.StringVar()

        # Main Frame
        frame = tk.Frame(self, bg="white")
        frame.place(x=435, y=50, width=480, height=620)  # x=400

        # Header
        header = tk.Label(frame, text="Customer Feedback", font=("Segoe UI", 25, "bold"),bg="white")
        header.place(x=20, y=20)

        # Employee Name
        self.employeeNameLabel = tk.Label(frame, text="Employee Name:", font=("Segoe UI", 14, "bold"),bg="white")
        self.employeeNameLabel.place(x=20, y=160)

        self.employeeId = []
        def run_sql(event):
            index = employeeNameEntry.current()
            row = FeedbackDB().EmpfetchAll()[index]
            
            self.employeeId.clear()
            self.employeeId.append(row[0])
            
        employeeNameEntry = ttk.Combobox(frame,font=("Segoe UI", 14),state="readonly",justify="center")
        employeeNameEntry["values"] = [row[1] for row in FeedbackDB().EmpfetchAll()]
        employeeNameEntry.place(x=190, y=160)
        employeeNameEntry.bind("<<ComboboxSelected>>", run_sql)

        # Performance Score
        performanceScoreLabel = tk.Label(frame, text="Performance Score:", font=("Segoe UI", 14, "bold"),bg="white")
        performanceScoreLabel.place(x=20, y=220)

        self.scale = tk.Scale(frame,orient=tk.HORIZONTAL,length=390,width=20,sliderlength=15,from_=0,to=10,tickinterval=1)
        self.scale.place(x=20, y=250)

        # Description
        descriptionLabel = tk.Label(frame, text="Description:", font=("Segoe UI", 14, "bold"),bg="white")
        descriptionLabel.place(x=20,y=330)

        self.descriptionEntry = tk.Text(frame, font=("Segoe UI", 14, "bold"), bg="#EBECF0", borderwidth=2)
        self.descriptionEntry.place(x=20, y=360, width=400, height=150)
       
        # Back Button (To Login Page)
        imgBack=Image.open("images/back.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageBack=ImageTk.PhotoImage(imgBack)
        backButton = tk.Button(frame, image=self.photoimageBack,borderwidth=0,bg="white",activebackground="white",command=lambda: controller.show_frame("Login"))
        backButton.place(x=40,y=530)

        # Submit Button
        imgSubmit=Image.open("images/save.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageSubmit=ImageTk.PhotoImage(imgSubmit)
        submitButton = tk.Button(frame,image=self.photoimageSubmit,borderwidth=0,bg="white",activebackground="white",command=lambda: self.retrieve_input())
        submitButton.place(x=140,y=530)

    def retrieve_input(self):
        try:
            if not self.employeeId:
                messagebox.showerror("Error","Please select an employee")
            elif self.scale.get()==0:
                op=messagebox.askyesno("Confirm","Are you sure to evaluate 0?")
                if op==True:
                    pass
                else:
                    return
            # elif len(self.descriptionEntry.get("1.0",'end-1c'))==0:
            #     messagebox.showerror("Error","Please leave some comments")
            else:
                data=(self.employeeId[0],self.scale.get(),self.descriptionEntry.get("1.0",'end-1c'),datetime.datetime.now())
                FeedbackDB().AddFB(data)
                messagebox.showinfo("Success","Record Successfully!")
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

if __name__ == "__main__":
    app = App()
    app.mainloop()