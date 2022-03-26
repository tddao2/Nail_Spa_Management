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
        self.show_frame("Feedback")

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
        FeedbackBtn=tk.Button(LeftFrame, image=self.imageFeedback,borderwidth=0,activebackground="#e2479c",bg="#e2479c")
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

        # Customer ID
        #lblCustomerId = tk.Label(LeftFrame, text="Customer ID", font=("Segoe UI", 18, "bold"), bg="#e2479c", fg="white")
        #lblCustomerId.place(x=15, y=80)

        #txtCustomerId = ttk.Entry(LeftFrame, textvariable=self.var_customer_id, font=("Segoe UI", 18), state=DISABLED)
        #txtCustomerId.place(x=140, y=80, width=200)

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
        btnDelete = tk.Button(LeftFrame, image=self.photoIamgeDelete, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerAddOrUpdate)
        btnDelete.place(x=230, y=380, width=50, height=50)

        # Refresh Button
        imgRefresh = Image.open("images/icons8-available-updates-40.png")
        self.photoIamgeRefresh = ImageTk.PhotoImage(imgRefresh)
        btnRefresh = tk.Button(LeftFrame, image=self.photoIamgeRefresh, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.CustomerClear)
        btnRefresh.place(x=290, y=380, width=50, height=50)

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
        self.cmbCustomerSearch["values"] = ("Select", "First Name", "Last Name", "Phone", "Email")
        self.cmbCustomerSearch.place(x=15, y=10, width=150)
        self.cmbCustomerSearch.current(0)

        txtCustomerSearch = tk.Entry(SearchFrame, textvariable=self.var_customer_searchtxt, font=("Segoe UI",15), bg="white")
        txtCustomerSearch.place(x=180, y=10, height=29)

        imgSearch = Image.open("images/icons8-browse-folder-30.png").resize((20,20),Image.ANTIALIAS)
        self.photoImageSearch=ImageTk.PhotoImage(imgSearch)
        btnSearch = tk.Button(SearchFrame, image=self.photoImageSearch, borderwidth=0, cursor="hand2", bg="#e2479c", activebackground="#e2479c", command=self.AcctSearch)
        btnSearch.place(x=385, y=10)

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


    def CustomerShow(self):
        # Clear existing records.
        self.tblCustomer.delete(*self.tblCustomer.get_children())

        try:
            # Iterate through the data returned by the fetch method in Database Class
            for row in CustomerDB().getAllCustomer():
                self.tblCustomer.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong")
            print(f"Error due to: {str(e)}.")

    
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
            
        employeeNameEntry = ttk.Combobox(frame,font=("Segoe UI", 14),state="readonly",justify="center")
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
                    data=(self.employeeId[0],self.scale.get(),self.descriptionEntry.get("1.0",'end-1c'),datetime.datetime.now())
                    FeedbackDB().AddFB(data)
                    self.FB_clear()
                    self.thankyou.pack()
                    self.thankyou.after(3000,self.thankyou.pack_forget)
                else:
                    return
            # elif len(self.descriptionEntry.get("1.0",'end-1c'))==0:
            #     messagebox.showerror("Error","Please leave some comments")
            else:
                data=(self.employeeId[0],self.scale.get(),self.descriptionEntry.get("1.0",'end-1c'),datetime.datetime.now())
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

if __name__ == "__main__":
    app = App()
    app.mainloop()