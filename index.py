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
from itertools import repeat
from nameparser import HumanName

from Backend.createtables import CreateTables
from Additional_features import myentry

from Backend.Database.account import AccountDB
from Backend.Database.account_status import AccountStatusDB
from Backend.Database.appointment import AppointmentDB
from Backend.Database.customer import CustomerDB
from Backend.Database.employee_status import EmployeeStatusDB
from Backend.Database.employee import EmployeeDB
from Backend.Database.feedback import FeedbackDB
from Backend.Database.invoice_line_item import InvoiceLineItemDB
from Backend.Database.invoice import InvoiceDB
from Backend.Database.role import RoleDB
from Backend.Database.service_type import ServiceTypeDB
from Backend.Database.service import ServiceDB

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
        for F in (Login, Register, Reset, Feedback, AdminDashboard, EmployeeDashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Display the current page
        self.show_frame("EmployeeDashboard")

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
        btnRegist.place(x=15,y=360,width=160) # y=370

        # Forget password Button
        btnForgetpw=tk.Button(lblFrame,text="Forget Password",font=("times new roman",10,"bold"),borderwidth=0,fg="black",bg="#e2479c", activeforeground="black",activebackground="#e2479c",command=lambda: controller.show_frame("Reset"))
        btnForgetpw.place(x=10,y=380,width=160) # y=390

        # Feedback Button
        img3FB=Image.open("images/feedback1.png").resize((160,43), Image.ANTIALIAS)
        self.photoimage3FB=ImageTk.PhotoImage(img3FB)
        btnFeedback = tk.Button(lblFrame,image=self.photoimage3FB,borderwidth=0, bg="#e2479c",activebackground="#e2479c", command=lambda: controller.show_frame("Feedback"))
        btnFeedback.place(x=15, y=400)

    def login(self):
        userfetch = (self.username.get())
        try:
            if self.username.get()=="":
                messagebox.showwarning("Warning","Username missing!.")
            elif self.password.get()=="":
                messagebox.showwarning("Warning","Password missing!.")
            elif self.username.get() and self.password.get():
                if AccountDB().fetch(userfetch) == None:
                    messagebox.showerror("Error","Invalid username or password. Please try again.")
                else:
                    if AccountDB().fetch(userfetch)[7] == 1:
                        messagebox.showerror("Error","Invalid username or password. Please try again.")
                    elif AccountDB().fetch(userfetch)[6] == 2:
                        messagebox.showerror("Error","Your account is pending.")
                    elif AccountDB().fetch(userfetch)[6] == 3:
                        messagebox.showerror("Error","Your account is locked.")
                    elif AccountDB().fetch(userfetch)[6] == 1 and AccountDB().fetch(userfetch)[5] == 1:
                        if bcrypt.checkpw(self.password.get().encode('utf8'), AccountDB().fetch(userfetch)[2].encode('utf8')):
                            self.controller.show_frame("AdminDashboard")
                            self.clear()
                        else:
                            messagebox.showerror("Error","Invalid username or password. Please try again.")
                    elif AccountDB().fetch(userfetch)[6] == 1 and AccountDB().fetch(userfetch)[5] == 2:
                        if bcrypt.checkpw(self.password.get().encode('utf8'), AccountDB().fetch(userfetch)[2].encode('utf8')):
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
        lblLeft.place(x=85,y=50,width=470,height=610) #x=50

        # main Frame
        frame=tk.Frame(self,bg="white")
        frame.place(x=555,y=50,width=710,height=610)  #x=520

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
        Loginbtn=tk.Button(frame, image=self.photoimageLogin,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="white",activebackground="white",command=lambda: controller.show_frame("Login"))
        Loginbtn.place(x=400,y=537,width=210,height=60)

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
                if AccountDB().fetch(userfetch)!=None:
                    messagebox.showerror("Warning","User Already Exists")
                else:
                    password=self.password.get().encode('utf8')
                    hashedpassword=bcrypt.hashpw(password, bcrypt.gensalt())
                    secret_answer=self.SA.get().encode('utf8')
                    SAhased=bcrypt.hashpw(secret_answer, bcrypt.gensalt())
                    account=(self.username.get(),hashedpassword,self.SQ.get(),SAhased,role_id,account_status_id,activeAccount)
                    AccountDB().insertAccount(account)

                    account_id=AccountDB().fetch(userfetch)
                    FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.phone.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                    employee=(self.firstname.get(),self.lastname.get(),self.txtDOB.get_date(),FormatedPhone,self.email.get(),self.txtAddress.get("1.0",END),employee_status_id,account_id[0],activeEmployee)
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
        # self.config(bg="#e2479c")

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
        FeedbackBtn=tk.Button(LeftFrame, image=self.imageFeedback,borderwidth=0,activebackground="#e2479c",bg="#e2479c",command=self.survey)
        FeedbackBtn.grid(row=5,column=1)

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
        self.FeedbackFrame=tk.Frame(self,relief=RIDGE,bd=1,bg="#e2479c")


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

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.EmpGetdata)
        self.EmpShow()

      
    def client(self):
        self.hide_all_frames()
        self.ClientFrame.place(x=100, y=30, width=1251, height=690)

        style = ttk.Style()
        style.configure('Treeview.Heading', font=("Segoe UI", 15, "bold"), foreground="black")
        style.map('Treeview', background=[('selected','#e2479c')])

        self.var_customer_searchby = tk.StringVar()
        self.var_customer_searchtxt = tk.StringVar()

        self.var_customer_id = tk.StringVar()
        self.var_customer_firstname = tk.StringVar()
        self.var_customer_lastname = tk.StringVar()
        self.var_customer_phone = tk.StringVar()
        self.var_customer_email = tk.StringVar()

        # ============= LEFT FRAME ================
        LeftFrame = tk.LabelFrame(self.ClientFrame, relief=RIDGE, bd=1, bg="#e2479c")
        LeftFrame.place(x=0, y=0, width=370, height=690)

        # Header
        header = tk.Label(LeftFrame, text="Customer Details", font=("Segoe UI", 25, "bold"), bg="#e2479c", fg="black")
        header.place(x=20, y=20)

        # First Name
        lblFirstName = tk.Label(LeftFrame, text="First Name", font=("Segoe UI", 18, "bold"), bg="#e2479c", fg="white")
        lblFirstName.place(x=15, y=140)

        self.txtCustomerFirstName = ttk.Entry(LeftFrame, textvariable=self.var_customer_firstname, font=("Segoe UI", 18))
        self.txtCustomerFirstName.place(x=140, y=140, width=200)

        # Last Name
        lblLastName = tk.Label(LeftFrame, text="Last Name", font=("Segoe UI", 18, "bold"), bg="#e2479c", fg="white")
        lblLastName.place(x=15, y=200)

        self.txtCustomerLastName = ttk.Entry(LeftFrame, textvariable=self.var_customer_lastname, font=("Segoe UI", 18))
        self.txtCustomerLastName.place(x=140, y=200, width=200)

        # Phone
        lblPhone = tk.Label(LeftFrame, text="Phone", font=("Segoe UI", 18, "bold"), bg="#e2479c", fg="white")
        lblPhone.place(x=15, y=260)

        self.txtCustomerPhone = ttk.Entry(LeftFrame, textvariable=self.var_customer_phone, font=("Segoe UI", 18))
        self.txtCustomerPhone.place(x=140, y=260, width=200)

        # Email
        lblEmail = tk.Label(LeftFrame, text="Email", font=("Segoe UI", 18, "bold"), bg="#e2479c", fg="white")
        lblEmail.place(x=15, y=320)

        self.txtCustomerEmail = ttk.Entry(LeftFrame, textvariable=self.var_customer_email, font=("Segoe UI", 18))
        self.txtCustomerEmail.place(x=140, y=320, width=200)

        # Save Button
        imgSave = Image.open("images/icons8-save-close-40.png")
        self.photoIamgeSave = ImageTk.PhotoImage(imgSave)
        btnSave = tk.Button(LeftFrame, image=self.photoIamgeSave, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerAddOrUpdate)
        btnSave.place(x=170, y=380, width=50, height=50) 

        # Delete Button
        imgDelete = Image.open("images/icons8-trash-can-40.png")
        self.photoIamgeDelete = ImageTk.PhotoImage(imgDelete)
        btnDelete = tk.Button(LeftFrame, image=self.photoIamgeDelete, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerDelete)
        btnDelete.place(x=230, y=380, width=50, height=50)

        # Reset Form Button
        imgResetForm = Image.open("images/icons8-available-updates-40.png")
        self.photoIamgeResetForm = ImageTk.PhotoImage(imgResetForm)
        btnResetForm = tk.Button(LeftFrame, image=self.photoIamgeResetForm, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerClear)
        btnResetForm.place(x=290, y=380, width=50, height=50)

        # ============= RIGHT FRAME ================
        RightFrame = tk.LabelFrame(self.ClientFrame, relief=RIDGE, bd=1, bg="#e2479c")
        RightFrame.place(x=370, y=0, width=880, height=690)

        # Header
        header = tk.Label(RightFrame, text="Search Customer", font=("Segoe UI", 25, "bold"), bg="#e2479c", fg="black")
        header.place(x=20, y=20)

        # ============= RIGHT UPPER FRAME =============
        SearchFrame = tk.Frame(RightFrame, relief=RIDGE, bd=2, bg="#e2479c")
        SearchFrame.place(x=20, y=60, width=680, height=60)

        self.cmbCustomerSearch = ttk.Combobox(SearchFrame, textvariable=self.var_customer_searchby, state="readonly", justify=CENTER, font=("Segoe UI", 15))
        self.cmbCustomerSearch["values"] = ("Select", "First Name", "Last Name")
        self.cmbCustomerSearch.place(x=15, y=10, width=150)
        self.cmbCustomerSearch.current(0)

        self.txtCustomerSearch = tk.Entry(SearchFrame, textvariable=self.var_customer_searchtxt, font=("Segoe UI",15), bg="white")
        self.txtCustomerSearch.place(x=180, y=10, height=29)

        # Search Button
        imgSearch = Image.open("images/icons8-browse-folder-30.png").resize((20,20),Image.ANTIALIAS)
        self.photoImageSearch=ImageTk.PhotoImage(imgSearch)
        btnSearch = tk.Button(SearchFrame, image=self.photoImageSearch, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerSearch)
        btnSearch.place(x=385, y=10)

        # Refresh Table Button
        imgRefreshTable = Image.open("images/icons8-available-updates-30.png").resize((20,20),Image.ANTIALIAS)
        self.photoIamgeRefreshTable = ImageTk.PhotoImage(imgRefreshTable)
        btnRefreshTable = tk.Button(SearchFrame, image=self.photoIamgeRefreshTable, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerShow)
        btnRefreshTable.place(x=420, y=10)

        # ============= RIGHT LOWER FRAME =============
        TableFrame = tk.LabelFrame(RightFrame, relief=RIDGE, bd=1, bg="white")
        TableFrame.place(x=20, y=135, width=835, height=540)

        scrollX = tk.Scrollbar(TableFrame, orient=HORIZONTAL)
        scrollX.pack(side=BOTTOM, fill=X)

        scrollY = tk.Scrollbar(TableFrame, orient=VERTICAL)
        scrollY.pack(side=RIGHT, fill=Y)

        self.tblCustomer = ttk.Treeview(TableFrame, columns=("customer_id", "customer_first_name", "customer_last_name", "customer_phone", "customer_email"),
                                            xscrollcommand=scrollX.set,
                                            yscrollcommand=scrollY.set,
                                            show='headings')

        scrollX.config(command=self.tblCustomer.xview)
        scrollY.config(command=self.tblCustomer.yview)

        self.tblCustomer.heading("customer_id", text="ID")
        self.tblCustomer.heading("customer_first_name", text="First Name")
        self.tblCustomer.heading("customer_last_name", text="Last Name")
        self.tblCustomer.heading("customer_phone", text="Phone Number")
        self.tblCustomer.heading("customer_email", text="Email")

        self.tblCustomer.column("customer_id", anchor=CENTER)
        self.tblCustomer.column("customer_first_name", anchor=CENTER)
        self.tblCustomer.column("customer_last_name", anchor=CENTER)
        self.tblCustomer.column("customer_phone", anchor=CENTER)
        self.tblCustomer.column("customer_email", anchor=CENTER)

        self.tblCustomer.pack(fill=BOTH, expand=1)
        self.tblCustomer.bind("<ButtonRelease-1>", self.CustomerSelect)
        self.CustomerShow()


    def sale(self):
        self.hide_all_frames()
        self.SaleFrame.place(x=250,y=30,width=1250,height=690)

    def survey(self):
        self.hide_all_frames()
        self.FeedbackFrame.place(x=100,y=30,width=1251,height=691)

        style = ttk.Style()
        # style.theme_use('clam')
        style.configure('Treeview.Heading',font=("times new roman",15,"bold"),foreground="black")
        style.map('Treeview',background=[('selected','#e2479c')])

        self.var_SVsearchby=tk.StringVar()
        self.var_SVsearchtxt=tk.StringVar()

        self.var_SV_id=tk.StringVar()
        self.var_month=tk.StringVar()
        self.var_SV_Emp=tk.StringVar()
        # ==========================================================Left Frame=============================================================
        
        # =============Top Left Frame=============
        SVLeftTopFrame=tk.LabelFrame(self.FeedbackFrame,text="Feedback Details",relief=RIDGE,font=("times new roman",15),bd=1,bg="#e2479c",fg="white")
        SVLeftTopFrame.place(x=0,y=0,width=370,height=389) # height = 689

        lblSV_Emp=tk.Label(SVLeftTopFrame,text="Employee",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblSV_Emp.place(x=15,y=20)

        txtSV_Emp=ttk.Entry(SVLeftTopFrame,textvariable=self.var_SV_Emp,font=("times new roman",18),state=DISABLED)
        txtSV_Emp.place(x=140,y=20,width=200)

        lblSV=tk.Label(SVLeftTopFrame,text="Feedback",font=("times new roman",18,"bold"),bg="#e2479c",fg="white")
        lblSV.place(x=15,y=80)

        self.txtSV=tk.Text(SVLeftTopFrame,font=("times new roman",12))
        self.txtSV.place(x=140,y=80,width=200,height=170)

        imgSVDelete=Image.open("images/delete.png").resize((60,60),Image.ANTIALIAS)
        self.photoimageSVDelete=ImageTk.PhotoImage(imgSVDelete)
        self.SVDeletebtn=tk.Button(SVLeftTopFrame, image=self.photoimageSVDelete,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.SVDelete)
        self.SVDeletebtn.place(x=100,y=290)

        imgSVRefresh=Image.open("images/Refresh.png").resize((60,60),Image.ANTIALIAS)
        self.photoimageSVRefresh=ImageTk.PhotoImage(imgSVRefresh)
        SVRefreshbtn=tk.Button(SVLeftTopFrame, image=self.photoimageSVRefresh,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.SVClear)
        SVRefreshbtn.place(x=200,y=290)

        # =============Bottom Left Frame=============
        SVLeftBottomFrame=tk.LabelFrame(self.FeedbackFrame,text="Feedback Remove",relief=RIDGE,font=("times new roman",15),bd=1,bg="#e2479c",fg="white")
        SVLeftBottomFrame.place(y=389,width=370,height=300) 

        self.lblSV_Search=tk.Label(SVLeftBottomFrame,text="Delete by",font=("times new roman",15,"bold"),bg="#e2479c",fg="white")
        self.lblSV_Search.place(x=15,y=20)

        self.SVcmb_Delete=ttk.Combobox(SVLeftBottomFrame,state="readonly",justify=CENTER,font=("times new roman",15))
        self.SVcmb_Delete["values"]=("Select","Monthly","Period")
        self.SVcmb_Delete.place(x=140,y=20,width=200)
        self.SVcmb_Delete.current(0)
        self.SVcmb_Delete.bind("<<ComboboxSelected>>", self.DeleteOptions)

        Monthly = [
            (1, 'Janurary'),
            (2, 'February'),
            (3, 'March'),
            (4, 'April'),
            (5, 'May'),
            (6, 'June'),
            (7, 'July'),
            (8, 'August'),
            (9, 'September'),
            (10, 'October'),
            (11, 'November'),
            (12, 'December')
        ]

        def data_set(index):
            index = self.SVcmb_Monthly.current()
            self.var_month.set(Monthly[index][0])

        self.lblMonthly=tk.Label(SVLeftBottomFrame,text="Monthly",font=("times new roman",15,"bold"),bg="#e2479c",fg="white")

        self.SVcmb_Monthly=ttk.Combobox(SVLeftBottomFrame,state="readonly",justify=CENTER,font=("times new roman",15))
        self.SVcmb_Monthly["values"]=[row[1] for row in Monthly]
        self.SVcmb_Monthly.bind("<<ComboboxSelected>>", data_set)

        self.lblFrom=tk.Label(SVLeftBottomFrame,text="From",font=("times new roman",15,"bold"),bg="#e2479c",fg="white")

        self.txtFrom=DateEntry(SVLeftBottomFrame,selectmode='day',font=("times new roman",15),date_pattern='mm/dd/y')

        self.lblTo=tk.Label(SVLeftBottomFrame,text="To",font=("times new roman",15,"bold"),bg="#e2479c",fg="white")

        self.txtTo=DateEntry(SVLeftBottomFrame,selectmode='day',font=("times new roman",15),date_pattern='mm/dd/y')

        imgSVRemove=Image.open("images/delete.png").resize((60,60),Image.ANTIALIAS)
        self.photoimageSVRemove=ImageTk.PhotoImage(imgSVRemove)
        self.SVRemovebtn=tk.Button(SVLeftBottomFrame, image=self.photoimageSVRemove,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.deleteMonthly)

        imgSVRemove1=Image.open("images/delete.png").resize((60,60),Image.ANTIALIAS)
        self.photoimageSVRemove1=ImageTk.PhotoImage(imgSVRemove1)
        self.SVRemove1btn=tk.Button(SVLeftBottomFrame, image=self.photoimageSVRemove1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.deletePeriod)

        # ==========================================================Right Frame=============================================================
        SV_RightFrame=tk.Frame(self.FeedbackFrame,relief=RIDGE,bd=1,bg="#e2479c")
        SV_RightFrame.place(x=370,y=12,width=880,height=678)

        # =============Top Right Frame=============
        SV_SearchFrame=tk.LabelFrame(SV_RightFrame,text="Search Feedback",relief=RIDGE,font=("times new roman",15),bd=4,bg="#e2479c",fg="white")
        SV_SearchFrame.place(x=100,width=680,height=71) #550

        self.SVcmb_search=ttk.Combobox(SV_SearchFrame,textvariable=self.var_SVsearchby,state="readonly",justify=CENTER,font=("times new roman",18))
        self.SVcmb_search["values"]=("Select","first_name","last_name","score","month")
        self.SVcmb_search.place(x=15,y=2,width=180)
        self.SVcmb_search.current(0)

        txt_SVsearch=tk.Entry(SV_SearchFrame,textvariable=self.var_SVsearchtxt,font=("times new roman",18),bg="white")
        txt_SVsearch.place(x=215,y=2) #10

        imgSearch=Image.open("images/search.png").resize((38,38),Image.ANTIALIAS)
        self.photoimageSearch=ImageTk.PhotoImage(imgSearch)
        btn_search=tk.Button(SV_SearchFrame,image=self.photoimageSearch,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c",command=self.SV_Search)
        btn_search.place(x=465)

        btn_showHistory=tk.Button(SV_SearchFrame,text="History Records",relief=RIDGE,font=("times new roman",14,"bold"),bd=2,cursor="hand2",bg="#e2479c",fg="white",activebackground="#e2479c",activeforeground="white",command=self.SV_showAll)
        btn_showHistory.place(x=510,width=150)

        # =============Bottom Right Frame=============
        FeedbackTableFrame=tk.LabelFrame(SV_RightFrame,relief=RIDGE,bd=1,bg="white")
        FeedbackTableFrame.place(x=20,y=82,width=839,height=574)

        scrollx=tk.Scrollbar(FeedbackTableFrame,orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM,fill=X)

        scrolly=tk.Scrollbar(FeedbackTableFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.FeedbackTable=ttk.Treeview(FeedbackTableFrame,columns=("Feedback ID","Full name","Score","Feedback","Date"),
                                        yscrollcommand=scrolly.set,xscrollcommand=scrollx.set,
                                        show='headings')

        scrollx.config(command=self.FeedbackTable.xview)
        scrolly.config(command=self.FeedbackTable.yview)

        self.FeedbackTable.heading("Feedback ID",text="STT")
        self.FeedbackTable.heading("Full name",text="Full name")
        self.FeedbackTable.heading("Score",text="Score")
        self.FeedbackTable.heading("Feedback",text="Feedback")
        self.FeedbackTable.heading("Date",text="Date")

        self.FeedbackTable["show"]="headings"

        self.FeedbackTable.column("Feedback ID",anchor=CENTER)
        self.FeedbackTable.column("Full name",anchor=CENTER)
        self.FeedbackTable.column("Score",anchor=CENTER)
        self.FeedbackTable.column("Feedback",anchor=CENTER)
        self.FeedbackTable.column("Date",anchor=CENTER)

        self.FeedbackTable.pack(fill=BOTH,expand=1)
        self.FeedbackTable.bind("<ButtonRelease-1>",self.SVGetdata)

        self.SV_show()

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
        self.FeedbackFrame.place_forget()

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
                    EmployeeDB().EmpUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.EmpClear()
                elif self.var_status.get()=="Current":
                    FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.var_contact.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                    data=(self.var_fname.get(),self.var_lname.get(),self.txtDOB.get_date(),self.var_email.get(),FormatedPhone,self.txtAddress.get("1.0",END),emp_status_Current,self.var_emp_id.get())
                    EmployeeDB().EmpUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.EmpClear()
                elif self.var_status.get()=="Pass":
                    FormatedPhone=phonenumbers.format_number(phonenumbers.parse(self.var_contact.get(), 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
                    data=(self.var_fname.get(),self.var_lname.get(),self.txtDOB.get_date(),self.var_email.get(),FormatedPhone,self.txtAddress.get("1.0",END),emp_status_Pass,self.var_emp_id.get())
                    EmployeeDB().EmpUpdate(data)
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
                    EmployeeDB().EmpDelete(data)
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
                rows = EmployeeDB().EmpSearch(data)
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert("",END,values=row)
                else:
                    messagebox.showerror("Error","No record found.")
            else:
                data=(self.var_searchby.get(),self.var_searchtxt.get())
                rows = EmployeeDB().EmpSearch(data)
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
            rows = EmployeeDB().EmpFetchHistory()
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
            if not EmployeeDB().EmpFetch():
                messagebox.showerror("Error", "No records found.")
            else:
                for row in EmployeeDB().EmpFetch():
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
                    AccountDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="User" and self.var_Acctstatus.get()=="pending":
                    data=(Role_User, Acct_Status_pending, self.var_acct_id.get())
                    AccountDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="User" and self.var_Acctstatus.get()=="inactive":
                    data=(Role_User, Acct_Status_inactive, self.var_acct_id.get())
                    AccountDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="Admin" and self.var_Acctstatus.get()=="active":
                    data=(Role_Admin, Acct_Status_active, self.var_acct_id.get())
                    AccountDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="Admin" and self.var_Acctstatus.get()=="pending":
                    data=(Role_Admin, Acct_Status_pending, self.var_acct_id.get())
                    AccountDB().AcctUpdate(data)
                    messagebox.showinfo("Success","Update Successfully!")
                    self.AcctClear()
                elif self.var_rolename.get()=="Admin" and self.var_Acctstatus.get()=="inactive":
                    data=(Role_Admin, Acct_Status_inactive, self.var_acct_id.get())
                    AccountDB().AcctUpdate(data)
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
                rows = AccountDB().AcctSearch(data)
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
            if not AccountStatusDB().AcctFetch():
                messagebox.showerror("Error", "No records found.")
            else:
                for row in AccountStatusDB().AcctFetch():
                    self.AccountTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def AcctShowAll(self):
        self.AccountTable.delete(*self.AccountTable.get_children())
        try:
            if not AccountDB().AcctFetchAll():
                messagebox.showerror("Error", "No records found.")
            else:
                for row in AccountDB().AcctFetchAll():
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

    def SV_show(self):
        self.FeedbackTable.delete(*self.FeedbackTable.get_children())
        try:
            if not FeedbackDB().getAllFB():
                self.Hide_Delete_Options()
                messagebox.showerror("Error", "No Feedback records available!!!.")


            else:
                for row in FeedbackDB().getAllFB():
                    self.FeedbackTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def SVGetdata(self,event):
        f=self.FeedbackTable.focus()
        curItem=(self.FeedbackTable.item(f))
        row=curItem['values']

        try:
            self.var_SV_id.set(row[0])
            self.var_SV_Emp.set(row[1])
            self.txtSV.config(state=NORMAL)
            self.txtSV.delete("1.0",END)
            self.txtSV.insert(END,row[3])
            self.txtSV.config(state=DISABLED) 
        except:
            pass

    def SVClear(self):
        self.Show_Delete_Options()

        self.var_SV_Emp.set("")
        self.txtSV.config(state=NORMAL)
        self.txtSV.delete("1.0",END)
        self.txtSV.config(state=DISABLED) 

        self.HideDeleteOptions()
        self.SV_ClearSearch()
        self.SV_show()

    def Hide_Delete_Options(self):
        self.SVDeletebtn.place_forget()
        self.lblSV_Search.place_forget()
        self.SVcmb_Delete.place_forget()
        self.lblMonthly.place_forget()
        self.SVcmb_Monthly.place_forget()
        self.lblFrom.place_forget()
        self.txtFrom.place_forget()
        self.lblTo.place_forget()
        self.txtTo.place_forget()

        self.SVRemovebtn.place_forget()
        self.SVRemove1btn.place_forget()

    def Show_Delete_Options(self):
        self.SVDeletebtn.place(x=100,y=290)
        self.lblSV_Search.place(x=15,y=20)
        self.SVcmb_Delete.place(x=140,y=20,width=200)

    def FeedbackDetails(self):
        self.var_SV_Emp.set("")
        self.txtSV.config(state=NORMAL)
        self.txtSV.delete("1.0",END)
        self.txtSV.config(state=DISABLED)

    def SVDelete(self):
        try:
            if self.var_SV_id.get()=="":
                messagebox.showerror("Error","No feedback info selected")
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?")
                if op==True:
                    feedback_id = self.var_SV_id.get()
                    FeedbackDB().removeFeedback(feedback_id)
                    messagebox.showinfo("Success","Delete Successfully!")
                    self.SVClear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def DeleteOptions(self, event):
        self.HideDeleteOptions()
        if self.SVcmb_Delete.get()=="Monthly":
            self.HideDeleteOptions()
            self.lblMonthly.place(x=15,y=60)
            self.SVcmb_Monthly.place(x=140,y=60,width=200)
            self.SVRemovebtn.place(x=100,y=190)


        if self.SVcmb_Delete.get()=="Period":
            self.HideDeleteOptions()
            self.lblFrom.place(x=15,y=60)
            self.txtFrom.place(x=140,y=60,width=200)
            self.lblTo.place(x=15,y=100)
            self.txtTo.place(x=140,y=100,width=200)
            self.SVRemove1btn.place(x=100,y=190)

    def HideDeleteOptions(self):

        self.SVcmb_Monthly.set("")
        self.txtFrom.delete(0,"end")
        self.txtTo.delete(0,"end")

        self.lblMonthly.place_forget()
        self.SVcmb_Monthly.place_forget()
        self.lblFrom.place_forget()
        self.txtFrom.place_forget()
        self.lblTo.place_forget()
        self.txtTo.place_forget()

        self.SVRemovebtn.place_forget()
        self.SVRemove1btn.place_forget()

    def deleteMonthly(self):
        try:
            if self.var_month.get() == "":
                messagebox.showerror("Error","Month input is required.")
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?")
                if op==True:
                    month=self.var_month.get()
                    FeedbackDB().deleteMonthly(month)
                    messagebox.showinfo("Success","Delete Successfully!")
                    self.HideDeleteOptions()
                    self.SVcmb_Delete.current(0)
                    self.SVClear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def deletePeriod(self):
        try:
            if self.txtFrom.get_date() == "":
                messagebox.showerror("Error","From input is required.")
            elif self.txtTo.get_date() == "":
                messagebox.showerror("Error","To input is required.")
            elif self.txtFrom.get_date() > self.txtTo.get_date():
                messagebox.showerror("Error","Date From must be less than or equal Date To!!!")
            else:
                op=messagebox.askyesno("Confirm","Do you really want to delete?")
                if op==True:
                    period=(self.txtFrom.get_date(),self.txtTo.get_date())
                    FeedbackDB().deletePeriod(period)
                    messagebox.showinfo("Success","Delete Successfully!")
                    self.HideDeleteOptions()
                    self.SVcmb_Delete.current(0)
                    self.SVClear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def SV_Search(self):
        try:
            if self.var_SVsearchby.get()=="Select":
                messagebox.showerror("Error","Select search by option")
            elif self.var_SVsearchtxt.get()=="":
                messagebox.showerror("Error","Search input is required")
            elif self.var_SVsearchby.get()=="score" and self.var_SVsearchtxt.get().isnumeric()==False:
                messagebox.showerror("Error","Input needs to be number")
            elif self.var_SVsearchby.get()=="score" and self.var_SVsearchtxt.get().isnumeric()==True:
                score = "performance_score"
                FBoption=(score,self.var_SVsearchtxt.get())
                rows = FeedbackDB().getFBbyOption(FBoption)
                if len(rows)!=0:
                    self.FeedbackTable.delete(*self.FeedbackTable.get_children())
                    for row in rows:
                        self.FeedbackTable.insert("",END,values=row)
                    self.SV_ClearSearch()
                    self.FeedbackDetails()
                    self.HideDeleteOptions()
                else:
                    messagebox.showerror("Error","No record found.")
                    self.SV_ClearSearch()
                    self.FeedbackDetails()
                    self.HideDeleteOptions()
            elif self.var_SVsearchby.get()=="month" and self.var_SVsearchtxt.get().isnumeric()==False:
                messagebox.showerror("Error","Input needs to be number")
            elif self.var_SVsearchby.get()=="month" and self.var_SVsearchtxt.get().isnumeric()==True:
                FBmonth=(self.var_SVsearchtxt.get())
                rows = FeedbackDB().getFBbyMonth(FBmonth)
                if len(rows)!=0:
                    self.FeedbackTable.delete(*self.FeedbackTable.get_children())
                    for row in rows:
                        self.FeedbackTable.insert("",END,values=row)
                    self.SV_ClearSearch()
                    self.FeedbackDetails()
                    self.HideDeleteOptions()
                else:
                    messagebox.showerror("Error","No record found.")
                    self.SV_ClearSearch()
                    self.FeedbackDetails()
                    self.HideDeleteOptions()
            else:
                FBoption=(self.var_SVsearchby.get(),self.var_SVsearchtxt.get())
                rows = FeedbackDB().getFBbyOption(FBoption)
                if len(rows)!=0:
                    self.FeedbackTable.delete(*self.FeedbackTable.get_children())
                    for row in rows:
                        self.FeedbackTable.insert("",END,values=row)
                    self.SV_ClearSearch()
                else:
                    messagebox.showerror("Error","No record found.")
                    self.SV_ClearSearch()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def SV_ClearSearch(self):
        self.SVcmb_search.current(0)
        self.var_SVsearchtxt.set("")
        self.SVcmb_Delete.current(0)

    def SV_showAll(self):
        try:
            rows = FeedbackDB().showAllFB()
            if len(rows)!=0:
                self.FeedbackTable.delete(*self.FeedbackTable.get_children())
                for row in rows:
                    self.FeedbackTable.insert("",END,values=row)
                self.SV_ClearSearch()
                self.Hide_Delete_Options()
            else:
                messagebox.showerror("Error","No historial records available!!!.")
                self.SV_ClearSearch()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    # Customer Helper Function
    def CustomerAddOrUpdate(self):
        try:
            # Check Input Field.
            if self.var_customer_firstname.get() == '' or self.var_customer_lastname.get() == '' \
                                                       or self.var_customer_phone.get() == '' \
                                                       or self.var_customer_email.get() == '':
                messagebox.showerror("Error", "Please input all required fields.")
                return
            
            # Add Mode: Insert New Customer Info.
            if self.var_customer_id.get() == "":
                CustomerDB().addCustomer(self.var_customer_firstname.get(), self.var_customer_lastname.get(), self.var_customer_phone.get(), self.var_customer_email.get())
                messagebox.showinfo("Success", "New Customer Record is Added Successfully!")            
            
            # Update Mode: Modify existing Customer Info.
            else:              
                CustomerDB().updateCustomer(self.var_customer_id.get(), self.var_customer_firstname.get(), self.var_customer_lastname.get(), self.var_customer_phone.get(), self.var_customer_email.get())
                messagebox.showinfo("Success", "Customer Record is updated Successfully!")
                
            # Clear Input Field.
            self.CustomerClear()

            # Reload Customer Table.
            self.CustomerShow()

        except Exception as e:
            messagebox.showerror("Error", "Something went wrong")
            print(f"Error due to: {str(e)}.")


    def CustomerDelete(self):
        try:
            if self.var_customer_id.get() == "":
                messagebox.showerror("Error", "Please select the customer record that you want to delete.")
            else:
                op = messagebox.askyesno("Confirm", "Do you really want to delete this record?")
                if op == True:
                    # Delete Customer Record.
                    customerId = self.var_customer_id.get()
                    CustomerDB().removeCustomer(customerId)
                    messagebox.showinfo("Success", "Delete Successfully!")

                    # Clear Input Field.
                    self.CustomerClear()

                    # Reload Customer Table.
                    self.CustomerShow()
                else:
                    return

        except Exception as e:
            messagebox.showerror("Error", "Something went wrong")
            print(f"Error due to: {str(e)}.")


    def CustomerSearch(self):
        try:
            if self.var_customer_searchby.get() == "Select":
                messagebox.showerror("Error", "Select choose an option.")

            elif self.var_customer_searchtxt.get() == "":
                messagebox.showerror("Error", "Search keyword is required.")
            
            elif self.var_customer_searchby.get()=="First Name" and self.var_customer_searchtxt.get():
                
                # Filter by First Name.
                firstName = self.var_customer_searchtxt.get()
                rows = CustomerDB().getCustomerByFirstName(firstName)

                # Clear Existing Records.
                self.tblCustomer.delete(*self.tblCustomer.get_children())

                # Load Records.
                for row in rows:
                    self.tblCustomer.insert('', tk.END, values=row)

            elif self.var_customer_searchby.get()=="Last Name" and self.var_customer_searchtxt.get():
                
                # Filter by Last name.
                lastName = self.var_customer_searchtxt.get()
                rows = CustomerDB().getCustomerByLastName(lastName)

                # Clear existing records.
                self.tblCustomer.delete(*self.tblCustomer.get_children())

                # Load record.
                for row in rows:
                    self.tblCustomer.insert('', tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Error", f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")


    def CustomerShow(self):
        # Clear existing records.
        self.tblCustomer.delete(*self.tblCustomer.get_children())

        # Iterate through the data returned by the fetch method in Database Class
        for row in CustomerDB().getAllCustomer():
            self.tblCustomer.insert('', tk.END, values=row)

        # Reset Search Bar.
        self.cmbCustomerSearch.current(0)
        self.txtCustomerSearch.delete(0, tk.END)
        

    def CustomerSelect(self, event):
        focus = self.tblCustomer.focus()
        curCustomer = (self.tblCustomer.item(focus))
        row = curCustomer['values']

        self.var_customer_id.set(row[0])
        self.txtCustomerFirstName.delete(0, tk.END)
        self.txtCustomerFirstName.insert(tk.END, row[1])
        self.txtCustomerLastName.delete(0, tk.END)
        self.txtCustomerLastName.insert(tk.END, row[2])
        self.txtCustomerPhone.delete(0, tk.END)
        self.txtCustomerPhone.insert(tk.END, row[3])
        self.txtCustomerEmail.delete(0, tk.END)
        self.txtCustomerEmail.insert(tk.END, row[4])


    def CustomerClear(self):
        # Clear Table Selection.
        for i in self.tblCustomer.selection():
            self.tblCustomer.selection_remove(i)

        # Clear Customer Id & Input Field.    
        self.var_customer_id.set("")
        self.txtCustomerFirstName.delete(0, tk.END)
        self.txtCustomerLastName.delete(0, tk.END)
        self.txtCustomerPhone.delete(0, tk.END)
        self.txtCustomerEmail.delete(0, tk.END)

        # Reset Search Bar.
        self.cmbCustomerSearch.current(0)
        self.txtCustomerSearch.delete(0, tk.END)


class Reset(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="#e2479c")
        self.controller = controller

        # Set Variables
        self.RS_username = tk.StringVar()
        self.RS_password = tk.StringVar()
        self.RS_CFpassword = tk.StringVar()
        self.RS_SQ = tk.StringVar()
        self.RS_SA = tk.StringVar()

        # left image
        bg1=Image.open("images/Nailwall.jpg").resize((470,610), Image.ANTIALIAS)
        self.lblbg1=ImageTk.PhotoImage(bg1)
        lblLeft=tk.Label(self, image=self.lblbg1)
        lblLeft.place(x=255,y=50,width=470,height=610) #x=85

        # main Frame
        frame=tk.Frame(self,bg="white")
        frame.place(x=725,y=50,width=370,height=610)  #x=710

        imgResetKey=Image.open("images/ResetKey.png").resize((80,80),Image.ANTIALIAS)
        self.photoimageResetKey=ImageTk.PhotoImage(imgResetKey)
        lblResetKey = tk.Label(frame,image=self.photoimageResetKey,borderwidth=0,bg="white")
        lblResetKey.place(x=0,y=0)
        

        lblReset=tk.Label(frame,text="RESET PASSWORD",font=("times new roman",24,"bold"),relief=GROOVE,borderwidth=1,fg="darkgreen",bg="white") ##fcfcfc
        lblReset.place(x=72,height=66)

        # label and entry

        # =============Row1=============
        imgResetuser=Image.open("images/Resetuser.png").resize((25,25),Image.ANTIALIAS)
        self.photoimageResetuser=ImageTk.PhotoImage(imgResetuser)
        lblResetuser = tk.Label(frame,image=self.photoimageResetuser,borderwidth=0,bg="white")
        lblResetuser.place(x=50,y=100)
        lblRS_username=tk.Label(frame,text="Username",font=("times new roman",15,"bold"),bg="white")
        lblRS_username.place(x=75,y=100)

        txtRS_username=ttk.Entry(frame,textvariable=self.RS_username,font=("times new roman",15))
        txtRS_username.place(x=50,y=130,width=250)

        # =============Row2=============
        imgQuestion=Image.open("images/Question.png").resize((25,25),Image.ANTIALIAS)
        self.photoimageQuestion=ImageTk.PhotoImage(imgQuestion)
        lblQuestion = tk.Label(frame,image=self.photoimageQuestion,borderwidth=0,bg="white")
        lblQuestion.place(x=50,y=170)
        lblRS_SecurityQ=tk.Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblRS_SecurityQ.place(x=75,y=170)

        self.RS_txtSecurityQ=ttk.Combobox(frame,textvariable=self.RS_SQ,font=("times new roman",15,"bold"),state="readonly",justify="center")
        self.RS_txtSecurityQ["values"]=("Select","Your Birth Place","Your Girlfriend name","Your Pet Name")
        self.RS_txtSecurityQ.place(x=50,y=200,width=250)
        self.RS_txtSecurityQ.current(0)

        # =============Row3=============
        imgAnswer=Image.open("images/Answer.png").resize((25,25),Image.ANTIALIAS)
        self.photoimageAnswer=ImageTk.PhotoImage(imgAnswer)
        lblAnswer = tk.Label(frame,image=self.photoimageAnswer,borderwidth=0,bg="white")
        lblAnswer.place(x=50,y=240)
        lblRS_SecurityA=tk.Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblRS_SecurityA.place(x=75,y=240)

        txtRS_SecurityA=ttk.Entry(frame,textvariable=self.RS_SA,font=("times new roman",15))
        txtRS_SecurityA.place(x=50,y=270,width=250)

        # =============Row4=============
        def show():
            txtRS_Password.config(show="")
            txtRS_ConfirmPw.config(show="")
            
        def hide():
            txtRS_Password.config(show="*")
            txtRS_ConfirmPw.config(show="*")

        imgLockpassword=Image.open("images/Lockpassword.png").resize((25,25),Image.ANTIALIAS)
        self.photoimageLockpassword=ImageTk.PhotoImage(imgLockpassword)
        lblLockpassword = tk.Label(frame,image=self.photoimageLockpassword,borderwidth=0,bg="white")
        lblLockpassword.place(x=50,y=310)
        lblRS_Password=tk.Label(frame,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblRS_Password.place(x=75,y=310)

        txtRS_Password=ttk.Entry(frame,textvariable=self.RS_password,font=("times new roman",15),show="*")
        txtRS_Password.place(x=50,y=340,width=250)

        # =============Row5=============
        imgLockpassword1=Image.open("images/Lockpassword.png").resize((25,25),Image.ANTIALIAS)
        self.photoimageLockpassword1=ImageTk.PhotoImage(imgLockpassword1)
        lblLockpassword1 = tk.Label(frame,image=self.photoimageLockpassword1,borderwidth=0,bg="white")
        lblLockpassword1.place(x=50,y=380)
        lblRS_ConfirmPw=tk.Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        lblRS_ConfirmPw.place(x=75,y=380)

        txtRS_ConfirmPw=ttk.Entry(frame,textvariable=self.RS_CFpassword,font=("times new roman",15),show="*")
        txtRS_ConfirmPw.place(x=50,y=410,width=250)

        imgRS_Visible=Image.open("images/visible.png").resize((35,35),Image.ANTIALIAS)
        self.photoimageRS_Visible=ImageTk.PhotoImage(imgRS_Visible)
        RS_toggle_btn = tk.Button(frame,image=self.photoimageRS_Visible,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),fg="white",bg="white",activebackground="white")
        RS_toggle_btn.place(x=310,y=405)
        RS_toggle_btn.bind("<ButtonPress>", lambda event:show())
        RS_toggle_btn.bind("<ButtonRelease>", lambda event:hide())

        # =============Row6=============
        btnResetPassword=tk.Button(frame,text="Reset Password",font=("times new roman",20,"bold"),relief=RAISED,fg="white",bg="#e2479c", activeforeground="white",activebackground="#e2479c",command=self.Resetpw)
        btnResetPassword.place(x=70,y=480,width=210,height=50)

        # =============Row7=============
        imgRS_back=Image.open("images/back1.png").resize((70,70),Image.ANTIALIAS)
        self.photoimageRS_back=ImageTk.PhotoImage(imgRS_back)
        RS_Back_btn = tk.Button(frame,image=self.photoimageRS_back,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),bg="white",activebackground="white",command=lambda: controller.show_frame("Login"))
        RS_Back_btn.place(x=145,y=540)

    def Resetpw(self):
        userfetch=(self.RS_username.get())
        fetchSQ=(self.RS_username.get(),self.RS_SQ.get())

        try:
            if self.RS_username.get()=="":
                messagebox.showerror("Error","Username missing.")
            elif self.RS_SQ.get()=="Select":
                messagebox.showerror("Error","Please select a security question.")
            elif self.RS_SA.get()=="":
                messagebox.showerror("Error","Security answer missing.")
            elif self.RS_password.get()=="":
                messagebox.showerror("Error","New password missing.")
            elif self.RS_CFpassword.get()=="":
                messagebox.showerror("Error","Confirm password missing.")
            elif self.RS_password.get() != self.RS_CFpassword.get():
                messagebox.showerror("Error","Your new password and confirmation password do not match.")
            else:
                if not AccountDB().fetch(userfetch):
                    messagebox.showerror("Error","Invalid username.")
                elif not AccountDB().fetchSQ(fetchSQ):
                    messagebox.showerror("Error","Invalid security question.")
                elif not bcrypt.checkpw(self.RS_SA.get().encode('utf8'), AccountDB().fetch(userfetch)[4].encode('utf8')):
                    messagebox.showerror("Error","Invalid security answer.")
                elif AccountDB().fetch(userfetch) and AccountDB().fetchSQ(fetchSQ) and bcrypt.checkpw(self.RS_SA.get().encode('utf8'), AccountDB().fetch(userfetch)[4].encode('utf8')):
                    SAhashed=bcrypt.hashpw(self.RS_password.get().encode('utf8'), bcrypt.gensalt())
                    pwUpdate=(SAhashed,self.RS_username.get())
                    AccountDB().Resetpassword(pwUpdate)
                    messagebox.showinfo("Success","Reset password successfully!")
                    self.RS_clear()
                else:
                    return
        except Exception as e:
            messagebox.showerror("Error",f"Error due to: {str(e)}")
            print(f"Something went wrong {e}.")

    def RS_clear(self):
        self.RS_username.set("")
        self.RS_txtSecurityQ.current(0)
        self.RS_SA.set("")
        self.RS_password.set("")
        self.RS_CFpassword.set("")

# Feedback Window
class Feedback(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Background color
        self.config(bg="#e2479c")

        # Create widgets
        self.create_widgets(controller)


    def create_widgets(self, controller):

        self.employeeName = tk.StringVar()

        # Main Frame
        frame = tk.Frame(self, bg="white")
        frame.place(x=435, y=50, width=480, height=620)

        # Thank you Frame
        imgThankyou=Image.open("images/thankyou.png").resize((1350,720),Image.ANTIALIAS)
        self.photoimageThankyou=ImageTk.PhotoImage(imgThankyou)
        self.thankyou = tk.Label(self, image=self.photoimageThankyou)

        # Header
        header = tk.Label(frame, text="Customer Feedback", font=("Segoe UI", 25, "bold"),bg="white")
        header.place(x=20, y=20)

        # Employee Name
        self.employeeNameLabel = tk.Label(frame, text="Employee Name:", font=("Segoe UI", 14, "bold"),bg="white")
        self.employeeNameLabel.place(x=20, y=160)

        self.employeeId = []
        def run_sql(event):
            index = employeeNameEntry.current()
            row = EmployeeDB().EmpfetchAll()[index]
            
            self.employeeId.clear()
            self.employeeId.append(row[0])
            
        employeeNameEntry = ttk.Combobox(frame,textvariable=self.employeeName,font=("Segoe UI", 14),state="readonly",justify="center")
        employeeNameEntry["values"] = [row[1] for row in EmployeeDB().EmpfetchAll()]
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
                    data=(self.employeeId[0],self.scale.get(),self.descriptionEntry.get("1.0",'end-1c'))
                    FeedbackDB().AddFB(data)
                    self.FB_clear()
                    self.thankyou.pack()
                    self.thankyou.after(3000,self.thankyou.pack_forget)
                else:
                    return
            else:
                data=(self.employeeId[0],self.scale.get(),self.descriptionEntry.get("1.0",'end-1c'))
                FeedbackDB().AddFB(data)
                self.FB_clear()
                self.thankyou.pack()
                self.thankyou.after(3000,self.thankyou.pack_forget)
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def FB_clear(self):
        self.scale.set(0)
        self.descriptionEntry.delete("1.0",END)
        self.employeeName.set("")
        self.employeeId.clear()

class EmployeeDashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.Start()

    def Start(self):

        #==========Set variables=============
        global SPW
        global SP
        global SPFS
        global RA
        global M
        global P
        global MP
        global R
        global PC
        global EFA
        global D
        global CD
        global BC
        global TN

        global E
        global UL
        global C
        global HL
        global FL
        global B
        global U
        global Face
        global Facial
        global EP
        global Duralash
        global MEE


        SPW=tk.DoubleVar()
        SP=tk.DoubleVar()
        SPFS=tk.DoubleVar()
        RA=tk.DoubleVar()

        M=tk.DoubleVar()
        P=tk.DoubleVar()
        MP=tk.DoubleVar()
        R=tk.DoubleVar()
        PC=tk.DoubleVar()
        EFA=tk.DoubleVar()
        D=tk.DoubleVar()
        CD=tk.DoubleVar()
        BC=tk.DoubleVar()
        TN=tk.DoubleVar()

        E=tk.DoubleVar()
        UL=tk.DoubleVar()
        C=tk.DoubleVar()
        HL=tk.DoubleVar()
        FL=tk.DoubleVar()
        B=tk.DoubleVar()
        U=tk.DoubleVar()
        Face=tk.DoubleVar()
        Facial=tk.DoubleVar()
        EP=tk.DoubleVar()
        Duralash=tk.DoubleVar()
        MEE=tk.DoubleVar()

        self.cname=tk.StringVar()
        self.cphn=tk.StringVar()
        self.c_email=tk.StringVar()

        self.totalMoney=tk.DoubleVar()
        self.totalTip=tk.DoubleVar()
        self.totalDiscount=tk.IntVar()

        self.Retrievedpw = tk.StringVar()


        SPW.set(0)
        SP.set(0)
        SPFS.set(0)
        RA.set(0)

        M.set(0)
        P.set(0)
        MP.set(0)
        R.set(0)
        PC.set(0)
        EFA.set(0)
        D.set(0)
        CD.set(0)
        BC.set(0)
        TN.set(0)

        E.set(0)
        UL.set(0)
        C.set(0)
        HL.set(0)
        FL.set(0)
        B.set(0)
        U.set(0)
        Face.set(0)
        Facial.set(0)
        EP.set(0)
        Duralash.set(0)
        MEE.set(0)

        
        self.ServiceId = []
        
        self.ServicePrice = []
        self.ServiceName = []
        self.ServiceType = []

        self.Selected_Services = []
        self.Selected_Services_Id = []
        self.Selected_Services_name = []

        self.retrieved_customers = []
        self.retrieved_customer_Id = []


        self.Selected_customer_Id = []
        
        self.retrieved_password = []
        self.retrieved_password_Id = []

        self.Selected_password_Id = []

        self.Service_id_price_name()
        self.Service_Type()
        self.get_All_Users()
        
        
        global SPW_btn1
        global SPW_btn2
        global sp_btn1
        global sp_btn2
        global CPFS_btn1
        global CPFS_btn2
        global RA_btn1
        global RA_btn2
        global M_btn1
        global M_btn2
        global P_btn1
        global P_btn2
        global MP_btn1
        global MP_btn2
        global R_btn1
        global R_btn2
        global PC_btn1
        global PC_btn2
        global EFA_btn1
        global EFA_btn2
        global D_btn1
        global D_btn2
        global CD_btn1
        global CD_btn2
        global BC__btn1
        global BC__btn2
        global TN__btn1
        global TN__btn2
        global E_btn1
        global E_btn2
        global UL_btn1
        global UL_btn2
        global C_btn1
        global C_btn2
        global HL_btn1
        global HL_btn2
        global FL_btn1
        global FL_btn2
        global B_btn1
        global B_btn2
        global U_btn1
        global U_btn2
        global Face_btn1
        global Face_btn2
        global Facial_btn1
        global Facial_btn2
        global EP_btn1
        global EP_btn2
        global Duralash_btn1
        global Duralash_btn2
        global MEE_btn1
        global MEE_btn2
               
        
        #========================Title==============================

        title=tk.Label(self,text="Billing Software",bd="12",relief=GROOVE,bg="#e2479c",fg="white",font=("time new roman",25,"bold"),pady=2)
        title.pack(fill=X)

        #========================Creating Frame==============================
        self.BillFrame=tk.Frame(self,relief=RIDGE)
        self.BillFrame.place(x=40,y=67,width=1310,height=652)

        F1=tk.LabelFrame(self.BillFrame,bd=10,relief=GROOVE,text="Customer Details",font=("time new roman",15,"bold"),fg="gold",bg="#e2479c")
        F1.place(relwidth=1)

        lblcname=tk.Label(F1,text="Customer Name",bg="#e2479c",fg="white",font=("time new roman",11,"bold"))
        lblcname.grid(row=0,column=0,padx=5,pady=5)

        self.txtcname=myentry(F1,textvariable=self.cname,width=15,font="arial 15",bd=3,relief=SUNKEN)
        self.txtcname.grid(row=0,column=1,pady=5)

        rows = CustomerDB().getAllCustByIdAndFname()
        cname = []
        cphn = []
        c_email = []
        
        for i in range(0, len(rows)):
            cname.append(rows[i][1])
            cphn.append(rows[i][2])
            c_email.append(rows[i][3])
        self.txtcname.set_completion_list(cname)

        lblcphn=tk.Label(F1,text="Phone No.",bg="#e2479c",fg="white",font=("time new roman",11,"bold"))
        lblcphn.grid(row=0,column=2,padx=5,pady=5)

        self.txtcphn=myentry(F1,textvariable=self.cphn,width=15,font="arial 15",bd=3,relief=SUNKEN)
        self.txtcphn.grid(row=0,column=3,pady=5,padx=5)
        self.txtcphn.set_completion_list(cphn)

        lblc_email=tk.Label(F1,text="Email",bg="#e2479c",fg="white",font=("time new roman",11,"bold"))
        lblc_email.grid(row=0,column=4,padx=5,pady=5)

        self.txtc_email=myentry(F1,textvariable=self.c_email,width=25,font="arial 15",bd=3,relief=SUNKEN)
        self.txtc_email.grid(row=0,column=5,pady=5,padx=5)
        self.txtc_email.set_completion_list(c_email)

        lblbill=tk.Label(F1,text="Bill Number",bg="#e2479c",fg="white",font=("time new roman",11,"bold"))
        lblbill.grid(row=0,column=6,padx=20,pady=10)

        self.txtbill=tk.Entry(F1,width=15,font="arial 15",bd=3,relief=SUNKEN)
        self.txtbill.grid(row=0,column=7,pady=10)

        self.bill_btn=tk.Button(F1,text="Find",width=5,bd=3,font="arial 11 bold",bg="#a50060",fg="white")
        self.bill_btn.grid(row=0,column=8,pady=10,padx=5)

        #========================Enhancement Services Set Frame==============================
        self.F2=tk.LabelFrame(self.BillFrame,bd=10,relief=GROOVE,text=self.ServiceType[0],font=("time new roman",15,"bold"),fg="gold",bg="#e2479c")
        self.F2.place(y=100,width=325,height=429)
   
        SPW_lbl=tk.Label(self.F2,text=f"{self.ServiceName[0]} (${self.ServicePrice[0]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        SPW_lbl.grid(row=0,column=0,padx=5,pady=4,sticky="w")

        def AddSPW_btn1():
            SPW_btn1.grid_forget()
            SPW_btn2.grid(row=0,column=2,pady=4)
            SPW.set(self.ServicePrice[0])
            print(f"SPW = {SPW.get()}")

        global BackSPW_btn2    

        def BackSPW_btn2():
            SPW_btn2.grid_forget()
            SPW_btn1.grid(row=0,column=1,pady=4)
            SPW.set(0)
            print(f"SPW = {SPW.get()}")
      
        imgSPW_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageSPW_btn1=ImageTk.PhotoImage(imgSPW_btn1)
        SPW_btn1=tk.Button(self.F2,image=self.photoimageSPW_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        SPW_btn1.grid(row=0,column=1,pady=4)
        SPW_btn1.bind("<ButtonRelease-1>",lambda event:AddSPW_btn1())

        imgSPW_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageSPW_btn2=ImageTk.PhotoImage(imgSPW_btn2)
        SPW_btn2=tk.Button(self.F2,image=self.photoimageSPW_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        SPW_btn2.bind("<ButtonRelease-1>",lambda event:BackSPW_btn2())

        sp_lbl=tk.Label(self.F2,text=f"{self.ServiceName[1]} (${self.ServicePrice[1]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        sp_lbl.grid(row=1,column=0,padx=5,pady=4,sticky="w")

        def Addsp_btn1():
            sp_btn1.grid_forget()
            sp_btn2.grid(row=1,column=2,pady=4)
            SP.set(self.ServicePrice[1])
            print(f"SP = {SP.get()}")

        global Backsp_btn2    

        def Backsp_btn2():
            sp_btn2.grid_forget()
            sp_btn1.grid(row=1,column=1,pady=4)
            SP.set(0)
            print(f"SP = {SP.get()}")

        imgsp_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimagesp_btn1=ImageTk.PhotoImage(imgsp_btn1)
        sp_btn1=tk.Button(self.F2,image=self.photoimagesp_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        sp_btn1.grid(row=1,column=1,pady=4)
        sp_btn1.bind("<ButtonRelease-1>",lambda event:Addsp_btn1())

        imgsp_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimagesp_btn2=ImageTk.PhotoImage(imgsp_btn2)
        sp_btn2=tk.Button(self.F2,image=self.photoimagesp_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        sp_btn2.bind("<ButtonRelease-1>",lambda event:Backsp_btn2())

        CPFS_lbl=tk.Label(self.F2,text=f"{self.ServiceName[2]} (${self.ServicePrice[2]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        CPFS_lbl.grid(row=2,column=0,padx=5,pady=4,sticky="w")

        def AddCPFS_btn1():
            CPFS_btn1.grid_forget()
            CPFS_btn2.grid(row=2,column=2,pady=4)
            SPFS.set(self.ServicePrice[2])
            print(f"SPFS = {SPFS.get()}")

        global BackCPFS_btn2    

        def BackCPFS_btn2():
            CPFS_btn2.grid_forget()
            CPFS_btn1.grid(row=2,column=1,pady=4)
            SPFS.set(0)
            print(f"SPFS = {SPFS.get()}")

        imgCPFS_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageCPFS_btn1=ImageTk.PhotoImage(imgCPFS_btn1)
        CPFS_btn1=tk.Button(self.F2,image=self.photoimageCPFS_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        CPFS_btn1.grid(row=2,column=1,pady=4)
        CPFS_btn1.bind("<ButtonRelease-1>",lambda event:AddCPFS_btn1())

        imgCPFS_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageCPFS_btn2=ImageTk.PhotoImage(imgCPFS_btn2)
        CPFS_btn2=tk.Button(self.F2,image=self.photoimageCPFS_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        CPFS_btn2.bind("<ButtonRelease-1>",lambda event:BackCPFS_btn2())
 
        RA_lbl=tk.Label(self.F2,text=f"{self.ServiceName[3]} (${self.ServicePrice[3]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        RA_lbl.grid(row=3,column=0,padx=5,pady=4,sticky="w")

        def AddRA_btn1():
            RA_btn1.grid_forget()
            RA_btn2.grid(row=3,column=2,pady=4)
            RA.set(self.ServicePrice[3])
            print(f"RA = {RA.get()}")

        global BackRA_btn2  

        def BackRA_btn2():
            RA_btn2.grid_forget()
            RA_btn1.grid(row=3,column=1,pady=4)
            RA.set(0)
            print(f"RA = {RA.get()}")

        imgRA_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageRA_btn1=ImageTk.PhotoImage(imgRA_btn1)
        RA_btn1=tk.Button(self.F2,image=self.photoimageRA_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        RA_btn1.grid(row=3,column=1,pady=4)
        RA_btn1.bind("<ButtonRelease-1>",lambda event:AddRA_btn1())

        imgRA_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageRA_btn2=ImageTk.PhotoImage(imgRA_btn2)
        RA_btn2=tk.Button(self.F2,image=self.photoimageRA_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        RA_btn2.bind("<ButtonRelease-1>",lambda event:BackRA_btn2())

        #========================Natural Nail Services Frame==============================
        self.F3=tk.LabelFrame(self.BillFrame,bd=10,relief=GROOVE,text=self.ServiceType[1],font=("time new roman",15,"bold"),fg="gold",bg="#e2479c")
        self.F3.place(x=326,y=100,width=325,height=429)
  
        M_lbl=tk.Label(self.F3,text=f"{self.ServiceName[4]} (${self.ServicePrice[4]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        M_lbl.grid(row=0,column=0,padx=5,pady=4,sticky="w")

        def AddM_btn1():
            M_btn1.grid_forget()
            M_btn2.grid(row=0,column=2,pady=3)
            M.set(self.ServicePrice[4])
            print(f"M = {M.get()}")

        global BackM_btn2 

        def BackM_btn2():
            M_btn2.grid_forget()
            M_btn1.grid(row=0,column=1,pady=3)
            M.set(0)
            print(f"M = {M.get()}")

        imgM_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageM_btn1=ImageTk.PhotoImage(imgM_btn1)
        M_btn1=tk.Button(self.F3,image=self.photoimageM_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        M_btn1.grid(row=0,column=1,pady=4)
        M_btn1.bind("<ButtonRelease-1>",lambda event:AddM_btn1())
        
        imgM_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageM_btn2=ImageTk.PhotoImage(imgM_btn2)
        M_btn2=tk.Button(self.F3,image=self.photoimageM_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        M_btn2.bind("<ButtonRelease-1>",lambda event:BackM_btn2())
        
        P_lbl=tk.Label(self.F3,text=f"{self.ServiceName[5]} (${self.ServicePrice[5]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        P_lbl.grid(row=1,column=0,padx=5,pady=4,sticky="w")

        def AddP_btn1():
            P_btn1.grid_forget()
            P_btn2.grid(row=1,column=2,pady=4)
            P.set(self.ServicePrice[5])
            print(f"P = {P.get()}")

        global BackP_btn2

        def BackP_btn2():
            P_btn2.grid_forget()
            P_btn1.grid(row=1,column=1,pady=4)
            P.set(0)
            print(f"P = {P.get()}")

        imgP_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageP_btn1=ImageTk.PhotoImage(imgP_btn1)
        P_btn1=tk.Button(self.F3,image=self.photoimageP_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        P_btn1.grid(row=1,column=1,pady=4)
        P_btn1.bind("<ButtonRelease-1>",lambda event:AddP_btn1())
        
        imgP_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageP_btn2=ImageTk.PhotoImage(imgP_btn2)
        P_btn2=tk.Button(self.F3,image=self.photoimageP_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        P_btn2.bind("<ButtonRelease-1>",lambda event:BackP_btn2())

        MP_lbl=tk.Label(self.F3,text=f"{self.ServiceName[6]} (${self.ServicePrice[6]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        MP_lbl.grid(row=2,column=0,padx=5,pady=4,sticky="w")

        def AddMP_btn1():
            MP_btn1.grid_forget()
            MP_btn2.grid(row=2,column=2,pady=4) 
            MP.set(self.ServicePrice[6])
            print(f"MP = {MP.get()}")

        global BackMP_btn2

        def BackMP_btn2():
            MP_btn2.grid_forget()
            MP_btn1.grid(row=2,column=1,pady=4)
            MP.set(0)
            print(f"MP = {MP.get()}")

        imgMP_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageMP_btn1=ImageTk.PhotoImage(imgMP_btn1)
        MP_btn1=tk.Button(self.F3,image=self.photoimageMP_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        MP_btn1.grid(row=2,column=1,pady=4)
        MP_btn1.bind("<ButtonRelease-1>",lambda event:AddMP_btn1()) 
        
        imgMP_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageMP_btn2=ImageTk.PhotoImage(imgMP_btn2)
        MP_btn2=tk.Button(self.F3,image=self.photoimageMP_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        MP_btn2.bind("<ButtonRelease-1>",lambda event:BackMP_btn2()) 
 
        R_lbl=tk.Label(self.F3,text=f"{self.ServiceName[7]} (${self.ServicePrice[7]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        R_lbl.grid(row=3,column=0,padx=5,pady=4,sticky="w")

        def AddR_btn1():
            R_btn1.grid_forget()
            R_btn2.grid(row=3,column=2,pady=4)
            R.set(self.ServicePrice[7])
            print(f"R = {R.get()}")

        global BackR_btn2

        def BackR_btn2():
            R_btn2.grid_forget()
            R_btn1.grid(row=3,column=1,pady=4)
            R.set(0)
            print(f"R = {R.get()}")

        imgR_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageR_btn1=ImageTk.PhotoImage(imgR_btn1)
        R_btn1=tk.Button(self.F3,image=self.photoimageR_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        R_btn1.grid(row=3,column=1,pady=4)
        R_btn1.bind("<ButtonRelease-1>",lambda event:AddR_btn1()) 
        
        imgR_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageR_btn2=ImageTk.PhotoImage(imgR_btn2)
        R_btn2=tk.Button(self.F3,image=self.photoimageR_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        R_btn2.bind("<ButtonRelease-1>",lambda event:BackR_btn2()) 

        PC_lbl=tk.Label(self.F3,text=f"{self.ServiceName[8]} (${self.ServicePrice[8]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        PC_lbl.grid(row=4,column=0,padx=5,pady=4,sticky="w")

        def AddPC_btn1():
            PC_btn1.grid_forget()
            PC_btn2.grid(row=4,column=2,pady=4) 
            PC.set(self.ServicePrice[8])
            print(f"PC = {PC.get()}")

        global BackPC_btn2

        def BackPC_btn2():
            PC_btn2.grid_forget()
            PC_btn1.grid(row=4,column=1,pady=4)
            PC.set(0)
            print(f"PC = {PC.get()}")

        imgPC_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimagePC_btn1=ImageTk.PhotoImage(imgPC_btn1)
        PC_btn1=tk.Button(self.F3,image=self.photoimagePC_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        PC_btn1.grid(row=4,column=1,pady=4)
        PC_btn1.bind("<ButtonRelease-1>",lambda event:AddPC_btn1())
        
        imgPC_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimagePC_btn2=ImageTk.PhotoImage(imgPC_btn2)
        PC_btn2=tk.Button(self.F3,image=self.photoimagePC_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c") 
        PC_btn2.bind("<ButtonRelease-1>",lambda event:BackPC_btn2())
       
        EFA_lbl=tk.Label(self.F3,text=f"{self.ServiceName[9]} (${self.ServicePrice[9]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        EFA_lbl.grid(row=5,column=0,padx=5,pady=4,sticky="w")

        def AddEFA_btn1():
            EFA_btn1.grid_forget()
            EFA_btn2.grid(row=5,column=2,pady=4) 
            EFA.set(self.ServicePrice[9])
            print(f"EFA = {EFA.get()}")

        global BackEFA_btn2

        def BackEFA_btn2():
            EFA_btn2.grid_forget()
            EFA_btn1.grid(row=5,column=1,pady=4)
            EFA.set(0)
            print(f"EFA = {EFA.get()}")

        imgEFA_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageEFA_btn1=ImageTk.PhotoImage(imgEFA_btn1)
        EFA_btn1=tk.Button(self.F3,image=self.photoimageEFA_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        EFA_btn1.grid(row=5,column=1,pady=4)
        EFA_btn1.bind("<ButtonRelease-1>",lambda event:AddEFA_btn1())
        
        imgEFA_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageEFA_btn2=ImageTk.PhotoImage(imgEFA_btn2)
        EFA_btn2=tk.Button(self.F3,image=self.photoimageEFA_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        EFA_btn2.bind("<ButtonRelease-1>",lambda event:BackEFA_btn2()) 

        D_lbl=tk.Label(self.F3,text=f"{self.ServiceName[10]} (${self.ServicePrice[10]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        D_lbl.grid(row=6,column=0,padx=5,pady=4,sticky="w")

        def AddD_btn1():
            D_btn1.grid_forget()
            D_btn2.grid(row=6,column=2,pady=4)
            D.set(self.ServicePrice[10])
            print(f"D = {D.get()}")

        global BackD_btn2

        def BackD_btn2():
            D_btn2.grid_forget()
            D_btn1.grid(row=6,column=1,pady=4)
            D.set(0)
            print(f"D = {D.get()}")

        imgD_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageD_btn1=ImageTk.PhotoImage(imgD_btn1)
        D_btn1=tk.Button(self.F3,image=self.photoimageD_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        D_btn1.grid(row=6,column=1,pady=4)
        D_btn1.bind("<ButtonRelease-1>",lambda event:AddD_btn1())
        
        imgD_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageD_btn2=ImageTk.PhotoImage(imgD_btn2)
        D_btn2=tk.Button(self.F3,image=self.photoimageD_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        D_btn2.bind("<ButtonRelease-1>",lambda event:BackD_btn2())

        CD_lbl=tk.Label(self.F3,text=f"{self.ServiceName[11]} (${self.ServicePrice[11]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        CD_lbl.grid(row=7,column=0,padx=5,pady=4,sticky="w")

        def AddCD_btn1():
            CD_btn1.grid_forget()
            CD_btn2.grid(row=7,column=2,pady=4)
            CD.set(self.ServicePrice[11])
            print(f"CD = {CD.get()}")

        global BackCD_btn2

        def BackCD_btn2():
            CD_btn2.grid_forget()
            CD_btn1.grid(row=7,column=1,pady=4)
            CD.set(0)
            print(f"CD = {CD.get()}")

        imgCD_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageCD_btn1=ImageTk.PhotoImage(imgCD_btn1)
        CD_btn1=tk.Button(self.F3,image=self.photoimageCD_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        CD_btn1.grid(row=7,column=1,pady=4)
        CD_btn1.bind("<ButtonRelease-1>",lambda event:AddCD_btn1())
        
        imgCD_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageCD_btn2=ImageTk.PhotoImage(imgCD_btn2)
        CD_btn2=tk.Button(self.F3,image=self.photoimageCD_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        CD_btn2.bind("<ButtonRelease-1>",lambda event:BackCD_btn2())
        
        BC_lbl=tk.Label(self.F3,text=f"{self.ServiceName[12]} (${self.ServicePrice[12]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        BC_lbl.grid(row=8,column=0,padx=5,pady=4,sticky="w")

        def AddBC__btn1():
            BC__btn1.grid_forget()
            BC__btn2.grid(row=8,column=2,pady=4)
            BC.set(self.ServicePrice[12])
            print(f"BC = {BC.get()}")

        global BackBC__btn2

        def BackBC__btn2():
            BC__btn2.grid_forget()
            BC__btn1.grid(row=8,column=1,pady=4)
            BC.set(0)
            print(f"BC = {BC.get()}")

        imgBC__btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageBC__btn1=ImageTk.PhotoImage(imgBC__btn1)
        BC__btn1=tk.Button(self.F3,image=self.photoimageBC__btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        BC__btn1.grid(row=8,column=1,pady=4)
        BC__btn1.bind("<ButtonRelease-1>",lambda event:AddBC__btn1())
        
        imgBC__btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageBC__btn2=ImageTk.PhotoImage(imgBC__btn2)
        BC__btn2=tk.Button(self.F3,image=self.photoimageBC__btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        BC__btn2.bind("<ButtonRelease-1>",lambda event:BackBC__btn2())

        TN_lbl=tk.Label(self.F3,text=f"{self.ServiceName[13]} (${self.ServicePrice[13]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        TN_lbl.grid(row=9,column=0,padx=5,pady=4,sticky="w")

        def AddTN__btn1():
            TN__btn1.grid_forget()
            TN__btn2.grid(row=9,column=2,pady=4)
            TN.set(self.ServicePrice[13])
            print(f"TN = {TN.get()}")

        global BackTN__btn2

        def BackTN__btn2():
            TN__btn2.grid_forget()
            TN__btn1.grid(row=9,column=1,pady=4)
            TN.set(0)
            print(f"TN = {TN.get()}")

        imgTN__btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageTN__btn1=ImageTk.PhotoImage(imgTN__btn1)
        TN__btn1=tk.Button(self.F3,image=self.photoimageTN__btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        TN__btn1.grid(row=9,column=1,pady=4)
        TN__btn1.bind("<ButtonRelease-1>",lambda event:AddTN__btn1())
        
        imgTN__btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageTN__btn2=ImageTk.PhotoImage(imgTN__btn2)
        TN__btn2=tk.Button(self.F3,image=self.photoimageTN__btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        TN__btn2.bind("<ButtonRelease-1>",lambda event:BackTN__btn2())

        self.lblEnterPassword = tk.Label(self.BillFrame, text="Enter password:",font=("time new roman",20,"bold"),bg="#f0f0f0")

        self.txtEnterPassword = ttk.Entry(self.BillFrame,textvariable=self.Retrievedpw,font=("time new roman",20,"bold"),show="*")

        self.BtnEnterPassword = tk.Button(self.BillFrame,text="Submit",font=("time new roman",10,"bold"),bg="#a50060",fg="white",activebackground="#a50060",activeforeground="white",command=self.SubmitPassword)

        #========================Waxing Services Frame==============================
        self.F4=tk.LabelFrame(self.BillFrame,bd=10,relief=GROOVE,text=self.ServiceType[2],font=("time new roman",15,"bold"),fg="gold",bg="#e2479c")
        self.F4.place(x=652,y=100,width=325,height=429)    

        E_lbl=tk.Label(self.F4,text=f"{self.ServiceName[14]} (${self.ServicePrice[14]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        E_lbl.grid(row=0,column=0,padx=5,pady=4,sticky="w")

        def AddE_btn1():
            E_btn1.grid_forget()
            E_btn2.grid(row=0,column=2,pady=4)
            E.set(self.ServicePrice[14])
            print(f"E = {E.get()}")

        global BackE_btn2

        def BackE_btn2():
            E_btn2.grid_forget()
            E_btn1.grid(row=0,column=1,pady=4)
            E.set(0)
            print(f"E = {E.get()}")

        imgE_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageE_btn1=ImageTk.PhotoImage(imgE_btn1)
        E_btn1=tk.Button(self.F4,image=self.photoimageE_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        E_btn1.grid(row=0,column=1,pady=4)
        E_btn1.bind("<ButtonRelease-1>",lambda event:AddE_btn1())

        imgE_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageE_btn2=ImageTk.PhotoImage(imgE_btn2)
        E_btn2=tk.Button(self.F4,image=self.photoimageE_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        E_btn2.bind("<ButtonRelease-1>",lambda event:BackE_btn2())

        UL_lbl=tk.Label(self.F4,text=f"{self.ServiceName[15]} (${self.ServicePrice[15]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        UL_lbl.grid(row=1,column=0,padx=5,pady=4,sticky="w")

        def AddUL_btn1():
            UL_btn1.grid_forget()
            UL_btn2.grid(row=1,column=2,pady=4)
            UL.set(self.ServicePrice[15])
            print(f"UL = {UL.get()}")

        global BackUL_btn2

        def BackUL_btn2():
            UL_btn2.grid_forget()
            UL_btn1.grid(row=1,column=1,pady=4)
            UL.set(0)
            print(f"UL = {UL.get()}")

        imgUL_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageUL_btn1=ImageTk.PhotoImage(imgUL_btn1)
        UL_btn1=tk.Button(self.F4,image=self.photoimageUL_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        UL_btn1.grid(row=1,column=1,pady=4)
        UL_btn1.bind("<ButtonRelease-1>",lambda event:AddUL_btn1()) 

        imgUL_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageUL_btn2=ImageTk.PhotoImage(imgUL_btn2)
        UL_btn2=tk.Button(self.F4,image=self.photoimageUL_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        UL_btn2.bind("<ButtonRelease-1>",lambda event:BackUL_btn2()) 
 
        C_lbl=tk.Label(self.F4,text=f"{self.ServiceName[16]} (${self.ServicePrice[16]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        C_lbl.grid(row=2,column=0,padx=5,pady=4,sticky="w")

        def AddC_btn1():
            C_btn1.grid_forget()
            C_btn2.grid(row=2,column=2,pady=4)
            C.set(self.ServicePrice[16])
            print(f"C = {C.get()}")

        global BackC_btn2

        def BackC_btn2():
            C_btn2.grid_forget()
            C_btn1.grid(row=2,column=1,pady=4)
            C.set(0)
            print(f"C = {C.get()}")

        imgC_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageC_btn1=ImageTk.PhotoImage(imgC_btn1)
        C_btn1=tk.Button(self.F4,image=self.photoimageC_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        C_btn1.grid(row=2,column=1,pady=4)
        C_btn1.bind("<ButtonRelease-1>",lambda event:AddC_btn1()) 

        imgC_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageC_btn2=ImageTk.PhotoImage(imgC_btn2)
        C_btn2=tk.Button(self.F4,image=self.photoimageC_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        C_btn2.bind("<ButtonRelease-1>",lambda event:BackC_btn2()) 
  
        HL_lbl=tk.Label(self.F4,text=f"{self.ServiceName[17]} (${self.ServicePrice[17]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        HL_lbl.grid(row=3,column=0,padx=5,pady=4,sticky="w")

        def AddHL_btn1():
            HL_btn1.grid_forget()
            HL_btn2.grid(row=3,column=2,pady=4)
            HL.set(self.ServicePrice[17])
            print(f"HL = {HL.get()}")

        global BackHL_btn2

        def BackHL_btn2():
            HL_btn2.grid_forget()
            HL_btn1.grid(row=3,column=1,pady=4)
            HL.set(0)
            print(f"HL = {HL.get()}")

        imgHL_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageHL_btn1=ImageTk.PhotoImage(imgHL_btn1)
        HL_btn1=tk.Button(self.F4,image=self.photoimageHL_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        HL_btn1.grid(row=3,column=1,pady=4)
        HL_btn1.bind("<ButtonRelease-1>",lambda event:AddHL_btn1())

        imgHL_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageHL_btn2=ImageTk.PhotoImage(imgHL_btn2)
        HL_btn2=tk.Button(self.F4,image=self.photoimageHL_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        HL_btn2.bind("<ButtonRelease-1>",lambda event:BackHL_btn2())

        FL_lbl=tk.Label(self.F4,text=f"{self.ServiceName[18]} (${self.ServicePrice[18]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        FL_lbl.grid(row=4,column=0,padx=5,pady=4,sticky="w")

        def AddFL_btn1():
            FL_btn1.grid_forget()
            FL_btn2.grid(row=4,column=2,pady=4)
            FL.set(self.ServicePrice[18])
            print(f"FL = {FL.get()}")

        global BackFL_btn2

        def BackFL_btn2():
            FL_btn2.grid_forget()
            FL_btn1.grid(row=4,column=1,pady=4)
            FL.set(0)
            print(f"FL = {FL.get()}")

        imgFL_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageFL_btn1=ImageTk.PhotoImage(imgFL_btn1)
        FL_btn1=tk.Button(self.F4,image=self.photoimageFL_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        FL_btn1.grid(row=4,column=1,pady=4)
        FL_btn1.bind("<ButtonRelease-1>",lambda event:AddFL_btn1()) 

        imgFL_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageFL_btn2=ImageTk.PhotoImage(imgFL_btn2)
        FL_btn2=tk.Button(self.F4,image=self.photoimageFL_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        FL_btn2.bind("<ButtonRelease-1>",lambda event:BackFL_btn2()) 
          
        B_lbl=tk.Label(self.F4,text=f"{self.ServiceName[19]} (${self.ServicePrice[19]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        B_lbl.grid(row=5,column=0,padx=5,pady=4,sticky="w")

        def AddB_btn1():
            B_btn1.grid_forget()
            B_btn2.grid(row=5,column=2,pady=4)
            B.set(self.ServicePrice[19])
            print(f"B = {B.get()}")

        global BackB_btn2

        def BackB_btn2():
            B_btn2.grid_forget()
            B_btn1.grid(row=5,column=1,pady=4)
            B.set(0)
            print(f"B = {B.get()}")

        imgB_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageB_btn1=ImageTk.PhotoImage(imgB_btn1)
        B_btn1=tk.Button(self.F4,image=self.photoimageB_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        B_btn1.grid(row=5,column=1,pady=4)
        B_btn1.bind("<ButtonRelease-1>",lambda event:AddB_btn1())

        imgB_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageB_btn2=ImageTk.PhotoImage(imgB_btn2)
        B_btn2=tk.Button(self.F4,image=self.photoimageB_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        B_btn2.bind("<ButtonRelease-1>",lambda event:BackB_btn2())

        U_lbl=tk.Label(self.F4,text=f"{self.ServiceName[20]} (${self.ServicePrice[20]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        U_lbl.grid(row=6,column=0,padx=5,pady=4,sticky="w")

        def AddU_btn1():
            U_btn1.grid_forget()
            U_btn2.grid(row=6,column=2,pady=4)
            U.set(self.ServicePrice[20])
            print(f"U = {U.get()}")

        global BackU_btn2

        def BackU_btn2():
            U_btn2.grid_forget()
            U_btn1.grid(row=6,column=1,pady=4)
            U.set(0)
            print(f"U = {U.get()}")

        imgU_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageU_btn1=ImageTk.PhotoImage(imgU_btn1)
        U_btn1=tk.Button(self.F4,image=self.photoimageU_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        U_btn1.grid(row=6,column=1,pady=4)
        U_btn1.bind("<ButtonRelease-1>",lambda event:AddU_btn1())

        imgU_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageU_btn2=ImageTk.PhotoImage(imgU_btn2)
        U_btn2=tk.Button(self.F4,image=self.photoimageU_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        U_btn2.bind("<ButtonRelease-1>",lambda event:BackU_btn2())

        Face_lbl=tk.Label(self.F4,text=f"{self.ServiceName[21]} (${self.ServicePrice[21]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        Face_lbl.grid(row=7,column=0,padx=5,pady=4,sticky="w")

        def AddFace_btn1():
            Face_btn1.grid_forget()
            Face_btn2.grid(row=7,column=2,pady=4)
            Face.set(self.ServicePrice[21])
            print(f"Face = {Face.get()}")

        global BackFace_btn2

        def BackFace_btn2():
            Face_btn2.grid_forget()
            Face_btn1.grid(row=7,column=1,pady=4)
            Face.set(0)
            print(f"Face = {Face.get()}")

        imgFace_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageFace_btn1=ImageTk.PhotoImage(imgFace_btn1)
        Face_btn1=tk.Button(self.F4,image=self.photoimageFace_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        Face_btn1.grid(row=7,column=1,pady=4)
        Face_btn1.bind("<ButtonRelease-1>",lambda event:AddFace_btn1())

        imgFace_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageFace_btn2=ImageTk.PhotoImage(imgFace_btn2)
        Face_btn2=tk.Button(self.F4,image=self.photoimageFace_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        Face_btn2.bind("<ButtonRelease-1>",lambda event:BackFace_btn2())
        
        Facial_lbl=tk.Label(self.F4,text=f"{self.ServiceName[22]} (${self.ServicePrice[22]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        Facial_lbl.grid(row=8,column=0,padx=5,pady=4,sticky="w")

        def AddFacial_btn1():
            Facial_btn1.grid_forget()
            Facial_btn2.grid(row=8,column=2,pady=4)
            Facial.set(self.ServicePrice[22])
            print(f"Facial = {Facial.get()}")

        global BackFacial_btn2

        def BackFacial_btn2():
            Facial_btn2.grid_forget()
            Facial_btn1.grid(row=8,column=1,pady=4)
            Facial.set(0)
            print(f"Facial = {Facial.get()}")

        imgFacial_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageFacial_btn1=ImageTk.PhotoImage(imgFacial_btn1)
        Facial_btn1=tk.Button(self.F4,image=self.photoimageFacial_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        Facial_btn1.grid(row=8,column=1,pady=4)
        Facial_btn1.bind("<ButtonRelease-1>",lambda event:AddFacial_btn1())

        imgFacial_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageFacial_btn2=ImageTk.PhotoImage(imgFacial_btn2)
        Facial_btn2=tk.Button(self.F4,image=self.photoimageFacial_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        Facial_btn2.bind("<ButtonRelease-1>",lambda event:BackFacial_btn2())

        EP_lbl=tk.Label(self.F4,text=f"{self.ServiceName[23]} (${self.ServicePrice[23]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        EP_lbl.grid(row=9,column=0,padx=5,pady=4,sticky="w")

        def AddEP_btn1():
            EP_btn1.grid_forget()
            EP_btn2.grid(row=9,column=2,pady=4)
            EP.set(self.ServicePrice[23])
            print(f"EP = {EP.get()}")

        global BackEP_btn2

        def BackEP_btn2():
            EP_btn2.grid_forget()
            EP_btn1.grid(row=9,column=1,pady=4)
            EP.set(0)
            print(f"EP = {EP.get()}")

        imgEP_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageEP_btn1=ImageTk.PhotoImage(imgEP_btn1)
        EP_btn1=tk.Button(self.F4,image=self.photoimageEP_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        EP_btn1.grid(row=9,column=1,pady=4)
        EP_btn1.bind("<ButtonRelease-1>",lambda event:AddEP_btn1())

        imgEP_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageEP_btn2=ImageTk.PhotoImage(imgEP_btn2)
        EP_btn2=tk.Button(self.F4,image=self.photoimageEP_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        EP_btn2.bind("<ButtonRelease-1>",lambda event:BackEP_btn2())

        Duralash_lbl=tk.Label(self.F4,text=f"{self.ServiceName[24]} (${self.ServicePrice[24]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        Duralash_lbl.grid(row=10,column=0,padx=5,pady=4,sticky="w")

        def AddDuralash_btn1():
            Duralash_btn1.grid_forget()
            Duralash_btn2.grid(row=10,column=2,pady=4)
            Duralash.set(self.ServicePrice[24])
            print(f"Duralash = {Duralash.get()}")

        global BackDuralash_btn2

        def BackDuralash_btn2():
            Duralash_btn2.grid_forget()
            Duralash_btn1.grid(row=10,column=1,pady=4)
            Duralash.set(0)
            print(f"Duralash = {Duralash.get()}")

        imgDuralash_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageDuralash_btn1=ImageTk.PhotoImage(imgDuralash_btn1)
        Duralash_btn1=tk.Button(self.F4,image=self.photoimageDuralash_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        Duralash_btn1.grid(row=10,column=1,pady=4)
        Duralash_btn1.bind("<ButtonRelease-1>",lambda event:AddDuralash_btn1())

        imgDuralash_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageDuralash_btn2=ImageTk.PhotoImage(imgDuralash_btn2)
        Duralash_btn2=tk.Button(self.F4,image=self.photoimageDuralash_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        Duralash_btn2.bind("<ButtonRelease-1>",lambda event:BackDuralash_btn2())

        MEE_lbl=tk.Label(self.F4,text=f"{self.ServiceName[25]} (${self.ServicePrice[25]})",font=("time new roman",11,"bold"),bg="#e2479c",fg="lightgreen")
        MEE_lbl.grid(row=11,column=0,padx=5,pady=4,sticky="w")

        def AddMEE_btn1():
            MEE_btn1.grid_forget()
            MEE_btn2.grid(row=11,column=2,pady=4)
            MEE.set(self.ServicePrice[25])
            print(f"MEE = {MEE.get()}")

        global BackMEE_btn2

        def BackMEE_btn2():
            MEE_btn2.grid_forget()
            MEE_btn1.grid(row=11,column=1,pady=4)
            MEE.set(0)
            print(f"MEE = {MEE.get()}")

        imgMEE_btn1=Image.open("images/plus.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageMEE_btn1=ImageTk.PhotoImage(imgMEE_btn1)
        MEE_btn1=tk.Button(self.F4,image=self.photoimageMEE_btn1,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        MEE_btn1.grid(row=11,column=1,pady=4)
        MEE_btn1.bind("<ButtonRelease-1>",lambda event:AddMEE_btn1())

        imgMEE_btn2=Image.open("images/check.png").resize((17,17),Image.ANTIALIAS)
        self.photoimageMEE_btn2=ImageTk.PhotoImage(imgMEE_btn2)
        MEE_btn2=tk.Button(self.F4,image=self.photoimageMEE_btn2,borderwidth=0,cursor="hand2",bg="#e2479c",activebackground="#e2479c")
        MEE_btn2.bind("<ButtonRelease-1>",lambda event:BackMEE_btn2())

        #========================Bill Area==============================
        self.F5=tk.LabelFrame(self.BillFrame,bd=10,relief=GROOVE)
        self.F5.place(x=978,y=100,width=332,height=429)
  
        bill_title=tk.Label(self.F5,text="Bill Area",font="arial 15 bold",bd=7,relief=GROOVE)
        bill_title.pack(fill=X)

        scrol_y=tk.Scrollbar(self.F5,orient=VERTICAL)
        self.txtarea=tk.Text(self.F5,yscrollcommand=scrol_y.set)
        scrol_y.pack(side=RIGHT,fill=Y)
        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH,expand=1)

        #========================Button Frame==============================
        F6=tk.LabelFrame(self.BillFrame,bd=10,relief=GROOVE,text="Bill Menu",font=("time new roman",15,"bold"),fg="gold",bg="#e2479c")
        F6.place(x=0,y=530,relwidth=1,height=122)

        Total_lbl=Label(F6,text="Total Price:   $",bg="#e2479c",fg="white",font=("time new roman",14,"bold"))   
        Total_lbl.grid(row=0,column=0,pady=25,sticky="w")

        self.Total_txt=tk.Entry(F6,textvariable=self.totalMoney,width=12,font="arial 10 bold",bd=3,relief=SUNKEN,state=DISABLED)
        self.Total_txt.grid(row=0,column=1,pady=25)

        Tip_lbl=Label(F6,text="Tip:   $",bg="#e2479c",fg="white",font=("time new roman",14,"bold"))   
        Tip_lbl.grid(row=0,column=2,pady=25,sticky="w")

        self.Tip_txt=tk.Entry(F6,textvariable=self.totalTip,width=12,font="arial 10 bold",bd=3,relief=SUNKEN)
        self.Tip_txt.grid(row=0,column=3,pady=25)

        Discount_lbl=Label(F6,text="% Discount",bg="#e2479c",fg="white",font=("time new roman",14,"bold"))   
        Discount_lbl.grid(row=0,column=4,padx=5,pady=25,sticky="w")

        self.Discount_txt=ttk.Combobox(F6,textvariable=self.totalDiscount,font=("arial",10,"bold"),state="readonly",justify="center")
        self.Discount_txt["values"]=(0,5,10,15,20,25,30)
        self.Discount_txt.grid(row=0,column=5,pady=25)

        btn_F=tk.Frame(F6,bd=2,relief=GROOVE,bg="#e2479c")
        btn_F.place(x=700,width=579,height=80)

        total_btn=tk.Button(btn_F,text="Total",bg="#A50060",fg="white",bd=2,pady=15,width=10,font="arial 15 bold",command=self.total)
        total_btn.grid(row=0,column=0,padx=7,pady=3)

        GBill_btn=tk.Button(btn_F,text="Generate Bill",bg="#A50060",fg="white",bd=2,pady=15,width=10,font="arial 15 bold",command=self.generate_bill)
        GBill_btn.grid(row=0,column=1,padx=7,pady=3)

        Clear_btn=tk.Button(btn_F,text="Refresh",bg="#A50060",fg="white",bd=2,pady=15,width=10,font="arial 15 bold",command=self.Start)
        Clear_btn.grid(row=0,column=2,padx=7,pady=3)

        Exit_btn=tk.Button(btn_F,text="Exit",bg="#A50060",fg="white",bd=2,pady=15,width=10,font="arial 15 bold")
        Exit_btn.grid(row=0,column=3,padx=7,pady=3)

        self.ApptFrame=tk.Frame(self,relief=RIDGE,bd=1 ,bg="#e2479c")
        self.CusFrame=tk.Frame(self,relief=RIDGE,bd=1 ,bg="#e2479c")

        #========================Button switch Frame==============================
        
        btnFrame=tk.Frame(self,relief=GROOVE,bg="#e2479c",bd=1)
        btnFrame.place(y=67,width=40,height=653)
        
        font = tkfont.nametofont("TkDefaultFont")
        font = tkfont.Font(family="time new roman", size=13, weight=tkfont.BOLD)
        
        BillLabel = "Billing"
        Apptlabel = "Appointment"
        CusLabel = "Customer"
        Apptheight = font.measure(Apptlabel) + 170
        Billheight = font.measure(BillLabel) + 170
        Cusheight = font.measure(CusLabel) + 170

        width = font.metrics()['linespace'] + 20

        Billcanvas = tk.Canvas(btnFrame, height=Billheight, width=width, bg="#ffcae5",borderwidth=1, relief="raised")
        Billcanvas.create_text((18, 110), angle="90", anchor="center", text=BillLabel, fill="#e2479c", font=font)

        Billcanvas.bind("<ButtonPress-1>", lambda ev: ev.widget.configure(relief="sunken"))
        Billcanvas.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief="raised"))
        Billcanvas.bind("<ButtonPress-1>", lambda ev: self.bill(), add=True)

        Apptcanvas = tk.Canvas(btnFrame, height=Apptheight, width=width, bg="#ffcae5", borderwidth=1, relief="raised")
        Apptcanvas.create_text((18, 116), angle="90", anchor="center", text=Apptlabel, fill="#e2479c", font=font)

        Apptcanvas.bind("<ButtonPress-1>", lambda ev: ev.widget.configure(relief="sunken"))
        Apptcanvas.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief="raised"))
               
        Cuscanvas = tk.Canvas(btnFrame, height=Cusheight, width=width, bg="#ffcae5",borderwidth=1, relief="raised")
        Cuscanvas.create_text((18, 75), angle="90", anchor="center", text=CusLabel, fill="#e2479c", font=font)

        Cuscanvas.bind("<ButtonPress-1>", lambda ev: ev.widget.configure(relief="sunken"))
        Cuscanvas.bind("<ButtonRelease-1>", lambda ev: ev.widget.configure(relief="raised"))
        
        Billcanvas.pack(fill=Y)
        Apptcanvas.pack(fill=Y)
        Cuscanvas.pack(fill=Y)

    

    def bill(self):
        self.hide_usr_all_frames()
        self.BillFrame.place(x=40,y=67,width=1310,height=652)

    def hide_usr_all_frames(self):
        self.Retrievedpw.set("")
        self.cname.set("")
        self.cphn.set("")
        self.c_email.set("")

        self.totalMoney.set(0)
        self.totalTip.set(0)
        self.totalDiscount.set(0)

        BackSPW_btn2()
        Backsp_btn2()
        BackCPFS_btn2()
        BackRA_btn2()

        BackM_btn2()
        BackP_btn2()
        BackMP_btn2()
        BackR_btn2()
        BackPC_btn2()
        BackEFA_btn2()
        BackD_btn2()
        BackCD_btn2()
        BackBC__btn2()
        BackTN__btn2()

        BackE_btn2()
        BackUL_btn2()
        BackC_btn2()
        BackHL_btn2()
        BackFL_btn2()
        BackB_btn2()
        BackU_btn2()
        BackFace_btn2()
        BackFacial_btn2()
        BackEP_btn2()
        BackDuralash_btn2()
        BackMEE_btn2()

        self.BillFrame.place_forget()
        self.ApptFrame.place_forget()
        self.CusFrame.place_forget()

    #========================Retrieve Service ID and price==============================
    def Service_id_price_name(self):

        self.ServiceId.clear()
        self.ServicePrice.clear()
        self.ServiceName.clear()

        try:
            Times = 26
            Price = "?"
            Name = "N/A"
            if not ServiceDB().getAllServices():
                self.ServicePrice.extend(repeat(Price, Times))
                self.ServiceName.extend(repeat(Name, Times))
                print(type(self.ServicePrice[0]))
            else:
                for row in ServiceDB().getAllServices():
                    self.ServiceId.append(row[0])
                    self.ServiceName.append(row[1])
                    self.ServicePrice.append(row[2])
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def Service_Type(self):
        self.ServiceType.clear()
        try:
            Times = 3
            TypeName = "N/A"
            if not ServiceDB().getAllServicesType():
                messagebox.showerror("Error","No services type available!!!")
                self.ServiceType.extend(repeat(TypeName, Times))
            else:
                for row in ServiceDB().getAllServicesType():
                    self.ServiceType.append(row[0])
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def total(self):
        self.Selected_Services.clear()
        self.Selected_Services_Id.clear()
        self.Selected_Services_name.clear()
        
        Services = [
                SPW.get(),SP.get(),SPFS.get(),RA.get(),M.get(),P.get(),MP.get(),R.get(),PC.get(),
                EFA.get(),D.get(),CD.get(),BC.get(),TN.get(),E.get(),UL.get(),C.get(),HL.get(),
                FL.get(),B.get(),U.get(),Face.get(),Facial.get(),EP.get(),Duralash.get(),MEE.get()
            ]

        for index in range(len(Services)):   
            value = Services[index]
            
            if value != 0 and type(value) != str:
                self.Selected_Services.append(value)
                self.Selected_Services_Id.append(index + 1)

        for index in self.Selected_Services_Id:
            self.Selected_Services_name.append(self.ServiceName[index-1])
            print(self.Selected_Services_name)

        if  self.ServiceName[0] == "N/A":
            messagebox.showerror("Error","No services available!!!")
            return
        elif sum(self.Selected_Services) == 0:
            messagebox.showerror("Error","No services selected!!!")
            self.totalMoney.set(0.0)
            self.totalTip.set(0.0)  
        elif (self.totalDiscount.get() == 0) and (sum(self.Selected_Services) != 0):
            Tip = self.totalTip.get()
            self.totalMoney.set(sum(self.Selected_Services) + Tip)
        elif (self.totalDiscount.get() != 0) and (sum(self.Selected_Services) != 0):
            Discount = self.totalDiscount.get()
            Tip = self.totalTip.get()
            self.totalMoney.set((sum(self.Selected_Services) + Tip) - ((sum(self.Selected_Services) + Tip) * (Discount/100)))
            
    def get_All_Users(self):
        self.retrieved_password.clear()
        self.retrieved_password_Id.clear()
        try:
            if not AccountDB().getEmpByPass():
                pass
            else:
                for row in AccountDB().getEmpByPass():
                    self.retrieved_password_Id.append(row[0])
                    self.retrieved_password.append(row[1])
        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def SubmitPassword(self):
        try:
            self.Selected_password_Id.clear()
            value_found = False
            for index in range(len(self.retrieved_password)):
                
                if bcrypt.checkpw(self.Retrievedpw.get().encode('utf8'), self.retrieved_password[index].encode('utf8')):
                    self.Selected_password_Id.append(self.retrieved_password_Id[index])
                    print(self.Selected_password_Id[0])
                    print("Correct")
                    
                    Customer_name = HumanName(self.cname.get())
                    first = Customer_name.first
                    last = Customer_name.last
                    phone = self.cphn.get()
                    email = self.c_email.get()

                    empId = self.Selected_password_Id[0]
                    tip = self.totalTip.get()
                    discount = self.totalDiscount.get()
                    total = self.totalMoney.get()

                    SerId = self.Selected_Services_Id

                    if not CustomerDB().fetchCusId(first, last):
                        print("No matched customer.")
                        CustomerId = []
                        InvoiceId = []
                        
                        RetrievedCustomerId = CustomerDB().addCustomerAndGetId(first, last, phone, email)
                        CustomerId.append(RetrievedCustomerId)

                        cusId = CustomerId[0]

                        RetrievedInvoiceId = InvoiceDB().Add_Invoice(empId, cusId, tip, discount, total)
                        InvoiceId.append(RetrievedInvoiceId)

                        InvId = InvoiceId[0]

                        InvoiceLineItemDB().Add_InvoiceItem(InvId, SerId)

                        messagebox.showinfo("Success","Invoice is submitted successfully!!!")

                        value_found = True
                        self.after_Submit_order()
                        break
                    else:
                        CustomerId = []
                        InvoiceId = []

                        RetrievedCustomerId = CustomerDB().fetchCusId(first, last)
                        CustomerId.append(RetrievedCustomerId)

                        cusId = CustomerId[0]

                        RetrievedInvoiceId = InvoiceDB().Add_Invoice(empId, cusId, tip, discount, total)
                        InvoiceId.append(RetrievedInvoiceId)

                        InvId = InvoiceId[0]

                        InvoiceLineItemDB().Add_InvoiceItem(InvId, SerId)

                        messagebox.showinfo("Success","Invoice is submitted successfully!!!")
                        value_found = True
                        self.after_Submit_order()
                        
                        break

            if not value_found:
                messagebox.showerror("Error","Wrong password")
                self.lblEnterPassword.place_forget()
                self.txtEnterPassword.place_forget()
                self.BtnEnterPassword.place_forget()

                self.F2.place(y=100,width=325,height=429)
                self.F3.place(x=326,y=100,width=325,height=429)
                self.F4.place(x=652,y=100,width=325,height=429)
                self.F5.place(x=978,y=100,width=332,height=429)

        except Exception as e:
            messagebox.showerror("Error","Something went wrong")
            print(f"Error due to: {str(e)}.")

    def generate_bill(self):
        if  self.ServiceName[0] == "N/A":
            messagebox.showerror("Error","No services available!!!")
            return
        elif sum(self.Selected_Services) == 0:
            messagebox.showerror("Error","No services selected!!!")
        elif self.cname.get() == "":
            messagebox.showerror("Error","Missing customer name!!!")
        else:
            self.F2.place_forget()
            self.F3.place_forget()
            self.F4.place_forget()
            self.F5.place_forget()

            self.lblEnterPassword.place(x=340, y=326)
            self.txtEnterPassword.place(x=600, y=326)
            self.BtnEnterPassword.place(x=470, y=390, width=80)

    def after_Submit_order(self):
        self.Start()

if __name__ == "__main__":
    app = App()
    app.mainloop()