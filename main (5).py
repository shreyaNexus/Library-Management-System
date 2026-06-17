"""
╔══════════════════════════════════════════════════════╗
║  BIBLIOTHECA — Library Management System             ║
║  Python 3 + Tkinter + Matplotlib                     ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json, os, datetime, hashlib, random

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

BG=      "#f0f7f4"; SURFACE= "#ffffff"; SIDEBAR= "#0d1f3c"; DEEP=    "#0a1628"
TEAL=    "#0d9488"; TEAL2=   "#0f766e"; TEAL_LT= "#5eead4"; TEAL_PAL="#ccfbf1"
MIST=    "#e8f5f0"; EMERALD= "#059669"; CYAN=    "#0891b2"; ROSE=    "#e11d48"
AMBER=   "#d97706"; VIOLET=  "#7c3aed"; TXT=     "#0f2027"; MUTED=   "#6b7280"
GOLD=    "#a7f3d0"; BORDER=  "#d1fae5"; BORDER2= "#e2e8f0"
CHART_COLORS=["#0d9488","#059669","#0891b2","#7c3aed","#d97706","#e11d48","#0f766e","#14b8a6","#6d28d9","#047857"]
FINE_RATE=2

DATA_FILE=os.path.join(os.path.dirname(os.path.abspath(__file__)),"library_data.json")
SEED={
"users":[
    {"email":"admin@library.com",    "pw":hashlib.md5(b"admin123").hexdigest(),"role":"Admin",    "name":"Dr. Ananya Roy"},
    {"email":"librarian@library.com","pw":hashlib.md5(b"lib123").hexdigest(),  "role":"Librarian","name":"Suresh Panda"},
    {"email":"member@library.com",   "pw":hashlib.md5(b"mem123").hexdigest(),  "role":"Member",   "name":"Priya Nayak"},
],
"books":[
    {"id":1,"title":"The God of Small Things","author":"Arundhati Roy",   "isbn":"978-0-06-097749-0","genre":"Fiction",    "year":"1997","publisher":"HarperCollins","copies":3,"available":3,"desc":"Forbidden love in Kerala."},
    {"id":2,"title":"Sapiens",                "author":"Yuval N. Harari","isbn":"978-0-06-231609-7","genre":"History",    "year":"2011","publisher":"Harvill Secker","copies":2,"available":1,"desc":"A brief history of humankind."},
    {"id":3,"title":"Wings of Fire",          "author":"A.P.J. Abdul Kalam","isbn":"978-81-7371-146-6","genre":"Biography","year":"1999","publisher":"Universities Press","copies":4,"available":4,"desc":"Autobiography of the missile man."},
    {"id":4,"title":"The Alchemist",          "author":"Paulo Coelho",   "isbn":"978-0-06-112241-5","genre":"Fiction",    "year":"1988","publisher":"HarperOne","copies":5,"available":3,"desc":"Following your dreams."},
    {"id":5,"title":"A Brief History of Time","author":"Stephen Hawking","isbn":"978-0-553-38016-3","genre":"Science",   "year":"1988","publisher":"Bantam Books","copies":2,"available":0,"desc":"From Big Bang to black holes."},
    {"id":6,"title":"Thinking, Fast and Slow","author":"D. Kahneman",    "isbn":"978-0-374-27563-1","genre":"Non-Fiction","year":"2011","publisher":"FSG","copies":3,"available":3,"desc":"Dual process cognition theory."},
    {"id":7,"title":"Clean Code",             "author":"Robert C. Martin","isbn":"978-0-13-235088-4","genre":"Technology","year":"2008","publisher":"Prentice Hall","copies":2,"available":2,"desc":"Software craftsmanship guide."},
    {"id":8,"title":"Discovery of India",     "author":"J. Nehru",       "isbn":"978-0-14-013802-5","genre":"History",   "year":"1946","publisher":"Penguin Books","copies":3,"available":2,"desc":"India through Nehru's eyes."},
],
"members":[
    {"id":1,"fname":"Aarav","lname":"Sharma","email":"aarav@ex.com","phone":"9876543210","type":"Student","address":"Bhubaneswar","joined":"2024-01-10","issued":2},
    {"id":2,"fname":"Priya","lname":"Patel", "email":"priya@ex.com","phone":"9865432109","type":"Faculty","address":"Cuttack","joined":"2023-08-15","issued":1},
    {"id":3,"fname":"Rahul","lname":"Das",   "email":"rahul@ex.com","phone":"9754321098","type":"Researcher","address":"Puri","joined":"2024-03-01","issued":0},
    {"id":4,"fname":"Sneha","lname":"Mishra","email":"sneha@ex.com","phone":"9643210987","type":"Student","address":"Rourkela","joined":"2024-02-20","issued":1},
],
"issues":[
    {"id":1,"book_id":2,"member_id":1,"book_title":"Sapiens","member_name":"Aarav Sharma","issued":"2026-02-20","due":"2026-03-06","returned":False,"fine":0},
    {"id":2,"book_id":4,"member_id":2,"book_title":"The Alchemist","member_name":"Priya Patel","issued":"2026-03-01","due":"2026-03-15","returned":False,"fine":0},
    {"id":3,"book_id":5,"member_id":1,"book_title":"A Brief History of Time","member_name":"Aarav Sharma","issued":"2026-02-01","due":"2026-02-15","returned":False,"fine":0},
    {"id":4,"book_id":8,"member_id":4,"book_title":"Discovery of India","member_name":"Sneha Mishra","issued":"2026-03-10","due":"2026-03-24","returned":False,"fine":0},
    {"id":5,"book_id":4,"member_id":3,"book_title":"The Alchemist","member_name":"Rahul Das","issued":"2026-01-15","due":"2026-01-29","returned":True,"fine":14},
],
"activity":[
    {"txt":"A Brief History of Time issued to Aarav Sharma","time":"2 hrs ago"},
    {"txt":"Discovery of India issued to Sneha Mishra","time":"1 day ago"},
    {"txt":"The Alchemist returned - Fine Rs.14","time":"2 days ago"},
    {"txt":"New member Rahul Das registered","time":"3 days ago"},
],
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE,encoding="utf-8") as f: return json.load(f)
        except: pass
    return {k:[dict(r) for r in v] for k,v in SEED.items()}

def save_data(d):
    try:
        with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(d,f,indent=2)
    except: pass

def today(): return datetime.date.today().isoformat()
def days_diff(d1,d2):
    try: return max(0,(datetime.date.fromisoformat(d2)-datetime.date.fromisoformat(d1)).days)
    except: return 0
def calc_fine(issue):
    if issue["returned"]: return issue["fine"]
    return days_diff(issue["due"],today())*FINE_RATE
def bk_status(book,issues):
    if book["available"]>0: return "Available"
    for i in issues:
        if i["book_id"]==book["id"] and not i["returned"] and i["due"]<today(): return "Overdue"
    return "Issued"
def get_initials(name):
    parts=name.strip().split()
    return (parts[0][0]+(parts[1][0] if len(parts)>1 else "")).upper()

def Btn(parent,text,cmd=None,kind="primary",**kw):
    PAL={"primary":(TEAL,"#ffffff",TEAL2),"danger":(ROSE,"#ffffff","#b91c1c"),
         "outline":(SURFACE,TEAL,TEAL_PAL),"ghost":(MIST,MUTED,BORDER),
         "dark":(DEEP,GOLD,SIDEBAR),"amber":(AMBER,"#ffffff","#b45309")}
    bg,fg,abg=PAL.get(kind,PAL["primary"])
    b=tk.Button(parent,text=text,command=cmd,bg=bg,fg=fg,
                activebackground=abg,activeforeground=fg,
                relief="flat",cursor="hand2",font=("Segoe UI",10,"bold"),
                padx=16,pady=7,bd=0,**kw)
    b.bind("<Enter>",lambda e:b.config(bg=abg))
    b.bind("<Leave>",lambda e:b.config(bg=bg))
    return b

def mkEntry(parent,**kw):
    kw.setdefault("bg",SURFACE); kw.setdefault("fg",TXT)
    kw.setdefault("insertbackground",TEAL); kw.setdefault("relief","flat")
    kw.setdefault("font",("Segoe UI",11)); kw.setdefault("bd",0)
    return tk.Entry(parent,**kw)

def LF(parent,label_txt,bg=BG):
    f=tk.Frame(parent,bg=bg)
    tk.Label(f,text=label_txt.upper(),bg=bg,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(0,3))
    bdr=tk.Frame(f,bg=BORDER2,padx=1,pady=1); bdr.pack(fill="x")
    e=mkEntry(bdr); e.pack(fill="x",padx=6,pady=5)
    return f,e

def CF(parent,label_txt,values,bg=BG):
    f=tk.Frame(parent,bg=bg)
    tk.Label(f,text=label_txt.upper(),bg=bg,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(0,3))
    c=ttk.Combobox(f,values=values,state="readonly",font=("Segoe UI",11)); c.pack(fill="x")
    return f,c

def mktree(parent,cols,widths,height=16):
    s=ttk.Style(); s.theme_use("clam")
    s.configure("T.Treeview",background=SURFACE,foreground=TXT,rowheight=32,
                fieldbackground=SURFACE,font=("Segoe UI",10),borderwidth=0)
    s.configure("T.Treeview.Heading",background=DEEP,foreground=GOLD,
                font=("Courier",9,"bold"),relief="flat")
    s.map("T.Treeview",background=[("selected",TEAL)],foreground=[("selected","#ffffff")])
    wrap=tk.Frame(parent,bg=BORDER2,padx=1,pady=1); wrap.pack(fill="both",expand=True)
    wrap.rowconfigure(0,weight=1); wrap.columnconfigure(0,weight=1)
    tree=ttk.Treeview(wrap,columns=cols,show="headings",style="T.Treeview",height=height)
    vsb=ttk.Scrollbar(wrap,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0,column=1,sticky="ns"); tree.grid(row=0,column=0,sticky="nsew")
    for col,w in zip(cols,widths): tree.heading(col,text=col); tree.column(col,width=w,anchor="w",minwidth=30)
    tree.tag_configure("avail",background="#f0fdf4")
    tree.tag_configure("issued",background="#fffbeb")
    tree.tag_configure("overdue",background="#fff1f2")
    return tree

def Toast(root,msg,kind="info"):
    t=tk.Toplevel(root); t.overrideredirect(True); t.attributes("-topmost",True)
    cols={"info":(DEEP,GOLD),"success":(EMERALD,"#ffffff"),"error":(ROSE,"#ffffff")}
    bg,fg=cols.get(kind,cols["info"]); t.configure(bg=bg)
    tk.Label(t,text=f"  {msg}  ",bg=bg,fg=fg,font=("Segoe UI",11,"bold"),padx=10,pady=9).pack()
    t.update_idletasks()
    sw,sh=root.winfo_screenwidth(),root.winfo_screenheight()
    t.geometry(f"+{sw-t.winfo_width()-30}+{sh-t.winfo_height()-60}")
    t.after(2800,t.destroy)


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bibliotheca"); self.configure(bg=DEEP); self.resizable(False,False)
        self.current_user=None; self.data=load_data()
        w,h=920,600
        self.geometry(f"{w}x{h}+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")
        self._build()

    def _build(self):
        self.columnconfigure(0,weight=4); self.columnconfigure(1,weight=5); self.rowconfigure(0,weight=1)
        self._build_left()
        self._right=tk.Frame(self,bg=MIST); self._right.grid(row=0,column=1,sticky="nsew")
        self._show_login()

    def _build_left(self):
        left=tk.Frame(self,bg=SIDEBAR); left.grid(row=0,column=0,sticky="nsew")
        brand=tk.Frame(left,bg=SIDEBAR); brand.pack(fill="x",padx=38,pady=(42,0))
        tk.Label(brand,text="Bibliotheca",bg=SIDEBAR,fg=TEAL_LT,font=("Georgia",28,"bold")).pack(anchor="w")
        tk.Label(brand,text="LIBRARY MANAGEMENT SYSTEM",bg=SIDEBAR,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(4,0))
        shelf=tk.Canvas(left,bg=SIDEBAR,height=110,highlightthickness=0); shelf.pack(side="bottom",fill="x")
        spines=["#0d9488","#059669","#0891b2","#7c3aed","#d97706","#0f766e","#14b8a6","#6d28d9","#047857","#0e7490","#065f46","#1d4ed8","#be185d","#92400e","#166534"]
        x=8
        for c in spines*3:
            h=random.randint(45,100); w=random.randint(14,26)
            shelf.create_rectangle(x,110-h,x+w,110,fill=c,outline="")
            x+=w+random.randint(1,5)
            if x>400: break
        qf=tk.Frame(left,bg=SIDEBAR); qf.pack(side="bottom",fill="x",padx=38,pady=(0,30))
        qt,qa=random.choice([
            ('"A library is not a luxury but\none of the necessities of life."',"— Henry Ward Beecher"),
            ('"In the library, there is hope\nfor everything."',"— Neil Gaiman"),
            ('"A reader lives a thousand lives\nbefore he dies."',"— George R.R. Martin"),
        ])
        tk.Label(qf,text=qt,bg=SIDEBAR,fg="#6ee7b7",font=("Georgia",11,"italic"),justify="left").pack(anchor="w")
        tk.Label(qf,text=qa,bg=SIDEBAR,fg=MUTED,font=("Courier",9)).pack(anchor="w",pady=(6,0))

    def _clear(self):
        for w in self._right.winfo_children(): w.destroy()

    def _show_login(self):
        self._clear(); f=self._right; pad=dict(padx=46)
        tk.Label(f,text="Welcome back",bg=MIST,fg=TXT,font=("Georgia",22,"bold")).pack(anchor="w",pady=(40,2),**pad)
        tk.Label(f,text="Sign in to your Bibliotheca account",bg=MIST,fg=MUTED,font=("Segoe UI",11)).pack(anchor="w",pady=(0,16),**pad)
        rf=tk.Frame(f,bg=BORDER2,padx=1,pady=1); rf.pack(fill="x",**pad)
        self._role=tk.StringVar(value="Admin")
        for r in ("Admin","Librarian","Member"):
            rb=tk.Radiobutton(rf,text=r,variable=self._role,value=r,
                              bg=MIST,fg=MUTED,selectcolor=TEAL,activebackground=MIST,
                              font=("Segoe UI",10,"bold"),indicatoron=False,
                              relief="flat",padx=20,pady=9,cursor="hand2")
            rb.pack(side="left",expand=True,fill="x")
        tk.Frame(f,bg=BORDER2,height=1).pack(fill="x",padx=46,pady=(2,16))
        ef,self._em=LF(f,"Email Address",bg=MIST); ef.pack(fill="x",**pad,pady=(0,10))
        self._em.insert(0,"admin@library.com")
        pf=tk.Frame(f,bg=MIST); pf.pack(fill="x",**pad,pady=(0,2))
        tk.Label(pf,text="PASSWORD",bg=MIST,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(0,3))
        pw_bdr=tk.Frame(pf,bg=BORDER2,padx=1,pady=1); pw_bdr.pack(fill="x")
        self._pw=mkEntry(pw_bdr,show="*"); self._pw.insert(0,"admin123")
        self._pw.pack(side="left",fill="x",expand=True,padx=6,pady=5)
        self._pw.bind("<Return>",lambda e:self._login())
        self._spv=tk.BooleanVar()
        tk.Checkbutton(pw_bdr,text="Show",variable=self._spv,bg=SURFACE,relief="flat",
                       font=("Segoe UI",9),
                       command=lambda:self._pw.config(show="" if self._spv.get() else "*")
                       ).pack(side="right",padx=6)
        fl=tk.Label(f,text="Forgot password?",bg=MIST,fg=TEAL,font=("Segoe UI",9),cursor="hand2")
        fl.pack(anchor="e",**pad,pady=(2,10)); fl.bind("<Button-1>",lambda e:self._show_forgot())
        self._lerr=tk.Label(f,text="",bg=MIST,fg=ROSE,font=("Segoe UI",10)); self._lerr.pack(**pad)
        Btn(f,"  Sign In  ->",cmd=self._login,kind="primary").pack(fill="x",**pad,pady=(8,0),ipady=4)
        tk.Frame(f,bg=BORDER2,height=1).pack(fill="x",padx=46,pady=12)
        demo=tk.Frame(f,bg=TEAL_PAL); demo.pack(fill="x",**pad)
        tk.Label(demo,text="DEMO CREDENTIALS",bg=TEAL_PAL,fg=TEAL2,font=("Courier",8)).pack(anchor="w",padx=12,pady=(8,3))
        for line in ("Admin: admin@library.com / admin123","Librarian: librarian@library.com / lib123","Member: member@library.com / mem123"):
            tk.Label(demo,text=line,bg=TEAL_PAL,fg=TXT,font=("Courier",10)).pack(anchor="w",padx=12)
        tk.Frame(demo,height=8,bg=TEAL_PAL).pack()
        sw=tk.Frame(f,bg=MIST); sw.pack(pady=10)
        tk.Label(sw,text="No account? ",bg=MIST,fg=MUTED,font=("Segoe UI",10)).pack(side="left")
        lnk=tk.Label(sw,text="Create one",bg=MIST,fg=TEAL,font=("Segoe UI",10,"bold"),cursor="hand2"); lnk.pack(side="left")
        lnk.bind("<Button-1>",lambda e:self._show_signup())

    def _show_signup(self):
        self._clear(); f=self._right; pad=dict(padx=46)
        bk=tk.Label(f,text="<- Back",bg=MIST,fg=TEAL,font=("Courier",9),cursor="hand2")
        bk.pack(anchor="w",**pad,pady=(28,0)); bk.bind("<Button-1>",lambda e:self._show_login())
        tk.Label(f,text="Create Account",bg=MIST,fg=TXT,font=("Georgia",20,"bold")).pack(anchor="w",pady=(6,2),**pad)
        tk.Label(f,text="Join the Bibliotheca community",bg=MIST,fg=MUTED,font=("Segoe UI",11)).pack(anchor="w",pady=(0,14),**pad)
        nr=tk.Frame(f,bg=MIST); nr.pack(fill="x",**pad,pady=(0,8))
        fnf,self._sfn=LF(nr,"First Name",bg=MIST); fnf.pack(side="left",expand=True,fill="x",padx=(0,8))
        lnf,self._sln=LF(nr,"Last Name",bg=MIST);  lnf.pack(side="left",expand=True,fill="x")
        emf,self._sem=LF(f,"Email Address",bg=MIST); emf.pack(fill="x",**pad,pady=(0,8))
        tpf,self._stp=CF(f,"Member Type",["Student","Faculty","Public","Researcher"],bg=MIST)
        tpf.pack(fill="x",**pad,pady=(0,8)); self._stp.set("Student")
        pwf,self._spw=LF(f,"Password (min 6)",bg=MIST); pwf.pack(fill="x",**pad,pady=(0,8)); self._spw.config(show="*")
        pf2,self._spw2=LF(f,"Confirm Password",bg=MIST); pf2.pack(fill="x",**pad,pady=(0,8))
        self._spw2.config(show="*"); self._spw2.bind("<Return>",lambda e:self._signup())
        self._serr=tk.Label(f,text="",bg=MIST,fg=ROSE,font=("Segoe UI",10)); self._serr.pack(**pad)
        Btn(f,"  Create Account  ->",cmd=self._signup,kind="primary").pack(fill="x",**pad,pady=(8,0),ipady=4)
        sw=tk.Frame(f,bg=MIST); sw.pack(pady=10)
        tk.Label(sw,text="Have account? ",bg=MIST,fg=MUTED,font=("Segoe UI",10)).pack(side="left")
        lnk=tk.Label(sw,text="Sign in",bg=MIST,fg=TEAL,font=("Segoe UI",10,"bold"),cursor="hand2"); lnk.pack(side="left")
        lnk.bind("<Button-1>",lambda e:self._show_login())

    def _show_forgot(self):
        self._clear(); f=self._right; pad=dict(padx=46)
        bk=tk.Label(f,text="<- Back",bg=MIST,fg=TEAL,font=("Courier",9),cursor="hand2")
        bk.pack(anchor="w",**pad,pady=(40,0)); bk.bind("<Button-1>",lambda e:self._show_login())
        tk.Label(f,text="Reset Password",bg=MIST,fg=TXT,font=("Georgia",22,"bold")).pack(anchor="w",pady=(12,2),**pad)
        tk.Label(f,text="Enter your email to receive a reset link",bg=MIST,fg=MUTED,font=("Segoe UI",11)).pack(anchor="w",pady=(0,22),**pad)
        emf,self._fem=LF(f,"Email Address",bg=MIST); emf.pack(fill="x",**pad,pady=(0,12))
        self._fem.bind("<Return>",lambda e:self._forgot())
        self._fmsg=tk.Label(f,text="",bg=MIST,font=("Segoe UI",10)); self._fmsg.pack(**pad)
        Btn(f,"  Send Reset Link  ->",cmd=self._forgot,kind="primary").pack(fill="x",**pad,pady=(10,0),ipady=4)

    def _login(self):
        em=self._em.get().strip().lower(); pw=self._pw.get()
        ph=hashlib.md5(pw.encode()).hexdigest()
        u=next((x for x in self.data["users"] if x["email"].lower()==em and x["pw"]==ph),None)
        if not u: self._lerr.config(text="Invalid email or password. Try demo credentials."); return
        self.current_user=u; self.destroy()

    def _signup(self):
        fn=self._sfn.get().strip(); ln=self._sln.get().strip()
        em=self._sem.get().strip().lower(); tp=self._stp.get()
        pw=self._spw.get(); pw2=self._spw2.get()
        if not fn or not ln: self._serr.config(text="Enter full name"); return
        if "@" not in em:    self._serr.config(text="Enter valid email"); return
        if len(pw)<6:        self._serr.config(text="Password min 6 chars"); return
        if pw!=pw2:          self._serr.config(text="Passwords do not match"); return
        if any(u["email"]==em for u in self.data["users"]): self._serr.config(text="Email already registered"); return
        nu={"email":em,"pw":hashlib.md5(pw.encode()).hexdigest(),"role":"Member","name":f"{fn} {ln}"}
        self.data["users"].append(nu)
        self.data["members"].append({"id":int(datetime.datetime.now().timestamp()),
            "fname":fn,"lname":ln,"email":em,"phone":"","type":tp,"address":"","joined":today(),"issued":0})
        save_data(self.data); self.current_user=nu; self.destroy()

    def _forgot(self):
        em=self._fem.get().strip().lower()
        if not em: self._fmsg.config(fg=ROSE,text="Enter your email"); return
        if not any(u["email"]==em for u in self.data["users"]): self._fmsg.config(fg=ROSE,text="No account found"); return
        self._fmsg.config(fg=EMERALD,text="Reset link sent! (Demo mode - password unchanged)")


class App(tk.Tk):
    def __init__(self,user,data):
        super().__init__()
        self.user=user; self.data=data
        self.title("Bibliotheca — Library Management System")
        self.configure(bg=BG); self.geometry("1300x800"); self.minsize(1100,680)
        self.geometry(f"1300x800+{(self.winfo_screenwidth()-1300)//2}+{(self.winfo_screenheight()-800)//2}")
        self._bk_filter="all"; self._build(); self.navigate("dashboard")

    def _build(self):
        self.columnconfigure(1,weight=1); self.rowconfigure(0,weight=1)
        self._build_sidebar()
        right=tk.Frame(self,bg=BG); right.grid(row=0,column=1,sticky="nsew")
        right.rowconfigure(1,weight=1); right.columnconfigure(0,weight=1)
        self._build_topbar(right)
        body=tk.Frame(right,bg=BG); body.grid(row=1,column=0,sticky="nsew")
        body.rowconfigure(0,weight=1); body.columnconfigure(0,weight=1)
        self._pages={}
        for name in ("dashboard","books","members","issue","returns","reports"):
            p=tk.Frame(body,bg=BG); p.grid(row=0,column=0,sticky="nsew"); self._pages[name]=p

    def _build_sidebar(self):
        sb=tk.Frame(self,bg=SIDEBAR,width=228); sb.grid(row=0,column=0,sticky="nsew"); sb.pack_propagate(False)
        lg=tk.Frame(sb,bg=SIDEBAR); lg.pack(fill="x",padx=18,pady=(24,14))
        tk.Label(lg,text="Bibliotheca",bg=SIDEBAR,fg=TEAL_LT,font=("Georgia",19,"bold")).pack(anchor="w")
        tk.Label(lg,text="LIBRARY MANAGEMENT",bg=SIDEBAR,fg=MUTED,font=("Courier",7)).pack(anchor="w")
        tk.Frame(sb,bg="#1a3050",height=1).pack(fill="x")
        nf=tk.Frame(sb,bg=SIDEBAR); nf.pack(fill="both",expand=True,pady=8)
        self._nav={}
        for key,lbl in (("dashboard","  Dashboard"),("books","  Books"),("members","  Members"),
                         ("issue","  Issue Book"),("returns","  Returns"),("reports","  Reports")):
            b=tk.Button(nf,text=lbl,bg=SIDEBAR,fg="#8fa8c0",relief="flat",font=("Segoe UI",11),
                        anchor="w",padx=18,cursor="hand2",bd=0,
                        activebackground=TEAL2,activeforeground="#fff",
                        command=lambda k=key:self.navigate(k))
            b.pack(fill="x",ipady=10)
            b.bind("<Enter>",lambda e,btn=b:btn.config(bg="#122a47") if btn!=self._nav.get(getattr(self,"_cur","")) else None)
            b.bind("<Leave>",lambda e,btn=b:btn.config(bg=SIDEBAR) if btn!=self._nav.get(getattr(self,"_cur","")) else None)
            self._nav[key]=b
        tk.Frame(sb,bg="#1a3050",height=1).pack(fill="x")
        ft=tk.Frame(sb,bg=SIDEBAR); ft.pack(fill="x",padx=16,pady=14)
        ini=get_initials(self.user["name"])
        row=tk.Frame(ft,bg=SIDEBAR); row.pack(fill="x",pady=(0,10))
        av=tk.Canvas(row,width=36,height=36,bg=SIDEBAR,highlightthickness=0); av.pack(side="left",padx=(0,8))
        av.create_oval(1,1,35,35,fill=TEAL,outline=""); av.create_text(18,18,text=ini,fill="#fff",font=("Georgia",12,"bold"))
        info=tk.Frame(row,bg=SIDEBAR); info.pack(side="left")
        tk.Label(info,text=self.user["name"],bg=SIDEBAR,fg="#dde8f0",font=("Segoe UI",10,"bold")).pack(anchor="w")
        tk.Label(info,text=self.user["role"].upper(),bg=SIDEBAR,fg=MUTED,font=("Courier",8)).pack(anchor="w")
        Btn(ft,"  Sign Out",cmd=self._logout,kind="ghost").pack(fill="x")

    def _build_topbar(self,parent):
        tb=tk.Frame(parent,bg=SURFACE,height=56); tb.grid(row=0,column=0,sticky="ew"); tb.pack_propagate(False)
        tb.columnconfigure(1,weight=1)
        self._title_lbl=tk.Label(tb,text="Dashboard",bg=SURFACE,fg=TXT,font=("Georgia",17,"bold"))
        self._title_lbl.grid(row=0,column=0,padx=22,sticky="w")
        sf=tk.Frame(tb,bg=BORDER2,padx=1,pady=1); sf.grid(row=0,column=1,padx=18,sticky="ew",pady=10)
        tk.Label(sf,text="  Search:",bg=SURFACE,fg=MUTED,font=("Segoe UI",10)).pack(side="left")
        self._q=tk.StringVar(); self._q.trace("w",self._on_search)
        tk.Entry(sf,textvariable=self._q,bg=SURFACE,fg=TXT,relief="flat",font=("Segoe UI",11),
                 insertbackground=TEAL,width=26).pack(side="left",pady=6,padx=4)
        acts=tk.Frame(tb,bg=SURFACE); acts.grid(row=0,column=2,padx=12)
        Btn(acts,"Issue",cmd=lambda:self.navigate("issue"),kind="outline").pack(side="left",padx=(0,8))
        Btn(acts,"+ Add Book",cmd=self._add_book_dlg,kind="primary").pack(side="left")
        chip=tk.Frame(tb,bg=TEAL_PAL,padx=8,pady=6); chip.grid(row=0,column=3,padx=12)
        cv=tk.Canvas(chip,width=28,height=28,bg=TEAL_PAL,highlightthickness=0); cv.pack(side="left",padx=(0,6))
        cv.create_oval(1,1,27,27,fill=TEAL,outline=""); cv.create_text(14,14,text=get_initials(self.user["name"]),fill="#fff",font=("Georgia",10,"bold"))
        tk.Label(chip,text=self.user["name"].split()[0],bg=TEAL_PAL,fg=TXT,font=("Segoe UI",10,"bold")).pack(side="left")

    def navigate(self,page):
        self._cur=page
        titles={"dashboard":"Dashboard","books":"Book Catalog","members":"Members",
                "issue":"Issue Book","returns":"Returns & Fines","reports":"Reports & Analytics"}
        self._title_lbl.config(text=titles.get(page,"")); self._q.set("")
        for k,btn in self._nav.items():
            if k==page: btn.config(bg=TEAL2,fg="#ffffff",font=("Segoe UI",11,"bold"))
            else:       btn.config(bg=SIDEBAR,fg="#8fa8c0",font=("Segoe UI",11))
        for w in self._pages[page].winfo_children(): w.destroy()
        {"dashboard":self._pg_dash,"books":self._pg_books,"members":self._pg_members,
         "issue":self._pg_issue,"returns":self._pg_returns,"reports":self._pg_reports}[page]()
        self._pages[page].tkraise()

    def _on_search(self,*_):
        if self._cur=="books": self._pg_books()
        elif self._cur=="members": self._pg_members()

    def toast(self,msg,kind="info"): Toast(self,msg,kind)

    def _logout(self):
        if messagebox.askyesno("Sign Out","Sign out of Bibliotheca?"): self.destroy()

    def _scroll_frame(self,parent):
        canvas=tk.Canvas(parent,bg=BG,highlightthickness=0)
        vsb=ttk.Scrollbar(parent,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right",fill="y"); canvas.pack(side="left",fill="both",expand=True)
        inner=tk.Frame(canvas,bg=BG); win=canvas.create_window((0,0),window=inner,anchor="nw")
        inner.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",lambda e:canvas.itemconfig(win,width=e.width))
        canvas.bind_all("<MouseWheel>",lambda e:canvas.yview_scroll(-1*(e.delta//120),"units"))
        return inner

    def _stat_card(self,parent,ico,val,lbl,accent,col):
        card=tk.Frame(parent,bg=SURFACE)
        card.grid(row=0,column=col,padx=(16 if col==0 else 6,6 if col<3 else 16),pady=(16,8),sticky="nsew")
        tk.Frame(card,bg=accent,height=4).pack(fill="x")
        tk.Label(card,text=ico,bg=SURFACE,font=("Segoe UI",22)).pack(anchor="w",padx=16,pady=(12,0))
        tk.Label(card,text=val,bg=SURFACE,fg=TXT,font=("Georgia",32,"bold")).pack(anchor="w",padx=16)
        tk.Label(card,text=lbl.upper(),bg=SURFACE,fg=MUTED,font=("Courier",9)).pack(anchor="w",padx=16,pady=(0,14))

    def _pg_dash(self):
        p=self._pages["dashboard"]; p.columnconfigure((0,1,2,3),weight=1); p.rowconfigure(1,weight=1)
        bks=self.data["books"]; iss=self.data["issues"]; mems=self.data["members"]
        total=len(bks); avail=sum(b["available"] for b in bks)
        issued=sum(1 for i in iss if not i["returned"])
        over=sum(1 for i in iss if not i["returned"] and i["due"]<today())
        for col,(ico,val,lbl,acc) in enumerate([("Books",str(total),"Total Books",TEAL),("OK",str(avail),"Available",EMERALD),("Out",str(issued),"Issued",CYAN),("LATE",str(over),"Overdue",ROSE)]):
            self._stat_card(p,ico,val,lbl,acc,col)
        bot=tk.Frame(p,bg=BG); bot.grid(row=1,column=0,columnspan=4,sticky="nsew",padx=16,pady=(0,16))
        bot.columnconfigure(0,weight=1); bot.columnconfigure(1,weight=1); bot.rowconfigure(0,weight=1)
        ac=tk.Frame(bot,bg=SURFACE); ac.grid(row=0,column=0,padx=(0,8),sticky="nsew")
        tk.Frame(ac,bg=TEAL,height=3).pack(fill="x")
        tk.Label(ac,text="Recent Activity",bg=SURFACE,fg=TXT,font=("Georgia",13,"bold")).pack(anchor="w",padx=16,pady=(12,4))
        tk.Frame(ac,bg=BORDER,height=1).pack(fill="x")
        dot_c=[TEAL,EMERALD,CYAN,VIOLET,AMBER]
        for idx,a in enumerate(self.data["activity"][:6]):
            row=tk.Frame(ac,bg=SURFACE); row.pack(fill="x",padx=14,pady=5)
            cv=tk.Canvas(row,width=10,height=10,bg=SURFACE,highlightthickness=0); cv.pack(side="left",padx=(0,8))
            cv.create_oval(1,1,9,9,fill=dot_c[idx%len(dot_c)],outline="")
            tk.Label(row,text=a["txt"],bg=SURFACE,fg=TXT,font=("Segoe UI",10),wraplength=280,justify="left").pack(side="left",fill="x",expand=True)
            tk.Label(row,text=a["time"],bg=SURFACE,fg=MUTED,font=("Courier",9)).pack(side="right")
        oc=tk.Frame(bot,bg=SURFACE); oc.grid(row=0,column=1,padx=(8,0),sticky="nsew")
        tk.Frame(oc,bg=ROSE,height=3).pack(fill="x")
        tk.Label(oc,text="Overdue Books",bg=SURFACE,fg=TXT,font=("Georgia",13,"bold")).pack(anchor="w",padx=16,pady=(12,4))
        tk.Frame(oc,bg=BORDER,height=1).pack(fill="x")
        od=[i for i in iss if not i["returned"] and i["due"]<today()]
        if od:
            for issue in od:
                d=days_diff(issue["due"],today()); fr=tk.Frame(oc,bg=SURFACE); fr.pack(fill="x",padx=14,pady=7)
                tk.Label(fr,text=issue["book_title"][:28],bg=SURFACE,fg=TXT,font=("Segoe UI",10,"bold")).pack(side="left")
                tk.Label(fr,text=f"{d}d  Rs.{d*FINE_RATE}",bg="#fff1f2",fg=ROSE,font=("Courier",10),padx=8).pack(side="right")
                tk.Label(fr,text=issue["member_name"],bg=SURFACE,fg=MUTED,font=("Segoe UI",9)).pack(side="left",padx=6)
        else:
            tk.Label(oc,text="No overdue books!",bg=SURFACE,fg=MUTED,font=("Segoe UI",12)).pack(pady=30)

    def _pg_books(self):
        p=self._pages["books"]; p.rowconfigure(1,weight=1); p.columnconfigure(0,weight=1)
        fb=tk.Frame(p,bg=BG); fb.grid(row=0,column=0,sticky="ew",padx=16,pady=(14,8))
        for lbl,val in (("All","all"),("Available","Available"),("Issued","Issued"),("Overdue","Overdue")):
            act=self._bk_filter==val
            btn=tk.Button(fb,text=lbl,bg=TEAL if act else SURFACE,fg="#fff" if act else MUTED,
                          relief="flat",padx=14,pady=7,font=("Segoe UI",10,"bold" if act else "normal"),
                          cursor="hand2",command=lambda v=val:self._set_filter(v))
            btn.pack(side="left",padx=(0,4))
        Btn(fb,"+ Add Book",cmd=self._add_book_dlg,kind="primary").pack(side="right")
        wrap=tk.Frame(p,bg=BG); wrap.grid(row=1,column=0,sticky="nsew",padx=16,pady=(0,16))
        wrap.rowconfigure(0,weight=1); wrap.columnconfigure(0,weight=1)
        self._btree=mktree(wrap,("Title","Author","ISBN","Genre","Year","Copies","Status"),[220,155,145,100,55,65,90],height=18)
        self._btree.bind("<Double-1>",lambda e:self._edit_book())
        cm=tk.Menu(self,tearoff=0,bg=SURFACE,fg=TXT,activebackground=TEAL,activeforeground="#fff",font=("Segoe UI",10))
        cm.add_command(label="Edit Book",command=self._edit_book)
        cm.add_command(label="Delete Book",command=self._del_book)
        self._btree.bind("<Button-3>",lambda e:cm.post(e.x_root,e.y_root))
        self._fill_books()

    def _set_filter(self,v): self._bk_filter=v; self._pg_books()

    def _fill_books(self):
        t=self._btree
        for r in t.get_children(): t.delete(r)
        q=self._q.get().lower()
        for b in self.data["books"]:
            st=bk_status(b,self.data["issues"])
            if self._bk_filter!="all" and st!=self._bk_filter: continue
            if q and q not in b["title"].lower() and q not in b["author"].lower(): continue
            tag={"Available":"avail","Issued":"issued","Overdue":"overdue"}.get(st,"")
            t.insert("","end",iid=str(b["id"]),
                     values=(b["title"],b["author"],b.get("isbn",""),b.get("genre",""),b.get("year",""),f"{b['available']}/{b['copies']}",st),
                     tags=(tag,))

    def _edit_book(self):
        sel=self._btree.selection()
        if sel: self._add_book_dlg(int(sel[0]))

    def _del_book(self):
        sel=self._btree.selection()
        if not sel: return
        bid=int(sel[0]); b=next((x for x in self.data["books"] if x["id"]==bid),None)
        if b and messagebox.askyesno("Delete",f'Delete "{b["title"]}"?'):
            self.data["books"]=[x for x in self.data["books"] if x["id"]!=bid]
            save_data(self.data); self._pg_books(); self.toast(f'"{b["title"]}" deleted',"error")

    def _add_book_dlg(self,book_id=None):
        b=next((x for x in self.data["books"] if x["id"]==book_id),None) if book_id else None
        dlg=tk.Toplevel(self); dlg.title("Edit Book" if b else "Add New Book")
        dlg.configure(bg=BG); dlg.geometry("540x570"); dlg.resizable(False,False)
        dlg.grab_set(); dlg.transient(self)
        tk.Frame(dlg,bg=TEAL,height=4).pack(fill="x")
        tk.Label(dlg,text="Edit Book" if b else "Add New Book",bg=BG,fg=TXT,font=("Georgia",18,"bold")).pack(anchor="w",padx=28,pady=(18,4))
        tk.Frame(dlg,bg=BORDER2,height=1).pack(fill="x",padx=28,pady=(0,14))
        fields={}
        for lbl,key in (("Book Title *","title"),("Author *","author"),("ISBN","isbn"),("Year","year"),("Publisher","publisher")):
            row=tk.Frame(dlg,bg=BG); row.pack(fill="x",padx=28,pady=3)
            tk.Label(row,text=lbl,bg=BG,fg=MUTED,font=("Courier",8),width=14,anchor="w").pack(side="left")
            e=mkEntry(row,bg=SURFACE); e.pack(side="left",fill="x",expand=True)
            if b: e.insert(0,str(b.get(key,"")))
            fields[key]=e
        grow=tk.Frame(dlg,bg=BG); grow.pack(fill="x",padx=28,pady=3)
        tk.Label(grow,text="Genre",bg=BG,fg=MUTED,font=("Courier",8),width=14,anchor="w").pack(side="left")
        genre_cb=ttk.Combobox(grow,values=["Fiction","Non-Fiction","Science","History","Technology","Biography","Philosophy","Poetry","Mystery"],state="readonly",font=("Segoe UI",11),width=28)
        genre_cb.pack(side="left"); genre_cb.set(b.get("genre","Fiction") if b else "Fiction")
        crow=tk.Frame(dlg,bg=BG); crow.pack(fill="x",padx=28,pady=3)
        tk.Label(crow,text="Total Copies *",bg=BG,fg=MUTED,font=("Courier",8),width=14,anchor="w").pack(side="left")
        copies_e=mkEntry(crow,bg=SURFACE,width=10); copies_e.pack(side="left"); copies_e.insert(0,str(b.get("copies",1)) if b else "1")
        df=tk.Frame(dlg,bg=BG); df.pack(fill="x",padx=28,pady=(8,4))
        tk.Label(df,text="DESCRIPTION",bg=BG,fg=MUTED,font=("Courier",8)).pack(anchor="w")
        desc_t=tk.Text(df,height=3,font=("Segoe UI",10),bg=SURFACE,fg=TXT,relief="flat",bd=1,insertbackground=TEAL)
        desc_t.pack(fill="x")
        if b: desc_t.insert("1.0",b.get("desc",""))
        err_lbl=tk.Label(dlg,text="",bg=BG,fg=ROSE,font=("Segoe UI",10)); err_lbl.pack(pady=4)
        def _save():
            title=fields["title"].get().strip(); author=fields["author"].get().strip()
            try: copies=max(1,int(copies_e.get()))
            except ValueError: err_lbl.config(text="Copies must be a number"); return
            if not title or not author: err_lbl.config(text="Title and Author required"); return
            if b:
                diff=copies-b["copies"]
                b.update({"title":title,"author":author,"isbn":fields["isbn"].get(),"genre":genre_cb.get(),
                          "year":fields["year"].get(),"publisher":fields["publisher"].get(),"copies":copies,
                          "available":max(0,b["available"]+diff),"desc":desc_t.get("1.0","end").strip()})
                self.toast("Book updated","success")
            else:
                self.data["books"].append({"id":int(datetime.datetime.now().timestamp()),"title":title,"author":author,
                    "isbn":fields["isbn"].get(),"genre":genre_cb.get(),"year":fields["year"].get(),
                    "publisher":fields["publisher"].get(),"copies":copies,"available":copies,"desc":desc_t.get("1.0","end").strip()})
                self.data["activity"].insert(0,{"txt":f'New book "{title}" added',"time":"just now"})
                self.toast(f'"{title}" added',"success")
            save_data(self.data); dlg.destroy(); self._pg_books()
        bf=tk.Frame(dlg,bg=BG); bf.pack(pady=12)
        Btn(bf,"Cancel",cmd=dlg.destroy,kind="ghost").pack(side="left",padx=6)
        Btn(bf,"  Save Book",cmd=_save,kind="primary").pack(side="left",padx=6)

    def _pg_members(self):
        p=self._pages["members"]; p.rowconfigure(1,weight=1); p.columnconfigure(0,weight=1)
        tb=tk.Frame(p,bg=BG); tb.grid(row=0,column=0,sticky="ew",padx=16,pady=(14,8))
        tk.Label(tb,text=f"  {len(self.data['members'])} members",bg=BG,fg=MUTED,font=("Courier",10)).pack(side="left")
        Btn(tb,"+ Add Member",cmd=self._add_member_dlg,kind="primary").pack(side="right")
        wrap=tk.Frame(p,bg=BG); wrap.grid(row=1,column=0,sticky="nsew",padx=16,pady=(0,16))
        wrap.rowconfigure(0,weight=1); wrap.columnconfigure(0,weight=1)
        self._mtree=mktree(wrap,("Name","ID","Email","Phone","Type","Issued","Joined"),[180,95,195,125,95,75,105],height=18)
        q=self._q.get().lower()
        for m in self.data["members"]:
            name=f"{m['fname']} {m['lname']}"
            if q and q not in name.lower() and q not in m["email"].lower(): continue
            mid=f"MEM-{str(m['id'])[-4:].zfill(4)}"
            self._mtree.insert("","end",iid=str(m["id"]),
                               values=(name,mid,m["email"],m.get("phone",""),m.get("type",""),f"{m['issued']} books",m.get("joined","")))
        cm=tk.Menu(self,tearoff=0,bg=SURFACE,fg=TXT,activebackground=TEAL,activeforeground="#fff",font=("Segoe UI",10))
        cm.add_command(label="Edit Member",command=self._edit_member)
        cm.add_command(label="Delete Member",command=self._del_member)
        self._mtree.bind("<Double-1>",lambda e:self._edit_member())
        self._mtree.bind("<Button-3>",lambda e:cm.post(e.x_root,e.y_root))

    def _edit_member(self):
        sel=self._mtree.selection()
        if sel: self._add_member_dlg(int(sel[0]))

    def _del_member(self):
        sel=self._mtree.selection()
        if not sel: return
        mid=int(sel[0]); m=next((x for x in self.data["members"] if x["id"]==mid),None)
        if m and messagebox.askyesno("Delete",f'Delete "{m["fname"]} {m["lname"]}"?'):
            self.data["members"]=[x for x in self.data["members"] if x["id"]!=mid]
            save_data(self.data); self._pg_members(); self.toast("Member removed","error")

    def _add_member_dlg(self,member_id=None):
        m=next((x for x in self.data["members"] if x["id"]==member_id),None) if member_id else None
        dlg=tk.Toplevel(self); dlg.title("Edit Member" if m else "Add New Member")
        dlg.configure(bg=BG); dlg.geometry("500x450"); dlg.resizable(False,False)
        dlg.grab_set(); dlg.transient(self)
        tk.Frame(dlg,bg=TEAL,height=4).pack(fill="x")
        tk.Label(dlg,text="Edit Member" if m else "Add New Member",bg=BG,fg=TXT,font=("Georgia",18,"bold")).pack(anchor="w",padx=28,pady=(18,4))
        tk.Frame(dlg,bg=BORDER2,height=1).pack(fill="x",padx=28,pady=(0,14))
        flds={}
        for lbl,key in (("First Name *","fname"),("Last Name *","lname"),("Email *","email"),("Phone","phone"),("Address","address")):
            row=tk.Frame(dlg,bg=BG); row.pack(fill="x",padx=28,pady=3)
            tk.Label(row,text=lbl,bg=BG,fg=MUTED,font=("Courier",8),width=14,anchor="w").pack(side="left")
            e=mkEntry(row,bg=SURFACE); e.pack(side="left",fill="x",expand=True)
            if m: e.insert(0,str(m.get(key,"")))
            flds[key]=e
        tr=tk.Frame(dlg,bg=BG); tr.pack(fill="x",padx=28,pady=3)
        tk.Label(tr,text="Type",bg=BG,fg=MUTED,font=("Courier",8),width=14,anchor="w").pack(side="left")
        type_cb=ttk.Combobox(tr,values=["Student","Faculty","Public","Researcher"],state="readonly",font=("Segoe UI",11),width=28)
        type_cb.pack(side="left"); type_cb.set(m.get("type","Student") if m else "Student")
        err_lbl=tk.Label(dlg,text="",bg=BG,fg=ROSE,font=("Segoe UI",10)); err_lbl.pack(pady=4)
        def _save():
            fn=flds["fname"].get().strip(); ln=flds["lname"].get().strip(); em=flds["email"].get().strip()
            if not fn or not ln: err_lbl.config(text="Name required"); return
            if "@" not in em:    err_lbl.config(text="Valid email required"); return
            if m:
                m.update({"fname":fn,"lname":ln,"email":em,"phone":flds["phone"].get(),"type":type_cb.get(),"address":flds["address"].get()})
                self.toast("Member updated","success")
            else:
                self.data["members"].append({"id":int(datetime.datetime.now().timestamp()),
                    "fname":fn,"lname":ln,"email":em,"phone":flds["phone"].get(),"type":type_cb.get(),
                    "address":flds["address"].get(),"joined":today(),"issued":0})
                self.data["activity"].insert(0,{"txt":f"New member {fn} {ln} registered","time":"just now"})
                self.toast(f"Member {fn} {ln} added","success")
            save_data(self.data); dlg.destroy(); self._pg_members()
        bf=tk.Frame(dlg,bg=BG); bf.pack(pady=12)
        Btn(bf,"Cancel",cmd=dlg.destroy,kind="ghost").pack(side="left",padx=6)
        Btn(bf,"  Save Member",cmd=_save,kind="primary").pack(side="left",padx=6)

    def _pg_issue(self):
        p=self._pages["issue"]; p.columnconfigure(0,weight=1); p.rowconfigure(0,weight=1)
        outer=tk.Frame(p,bg=BG); outer.place(relx=0.5,rely=0.45,anchor="center")
        card=tk.Frame(outer,bg=SURFACE); card.pack()
        hd=tk.Frame(card,bg=TEAL); hd.pack(fill="x")
        tk.Label(hd,text="Issue a Book",bg=TEAL,fg="#ffffff",font=("Georgia",20,"bold")).pack(anchor="w",padx=28,pady=(18,4))
        tk.Label(hd,text="Select a member and an available book",bg=TEAL,fg=TEAL_PAL,font=("Segoe UI",11)).pack(anchor="w",padx=28,pady=(0,16))
        body=tk.Frame(card,bg=SURFACE); body.pack(fill="both",padx=30,pady=20)
        tk.Label(body,text="SELECT MEMBER",bg=SURFACE,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(0,4))
        self._iss_mem=ttk.Combobox(body,state="readonly",font=("Segoe UI",11),width=54); self._iss_mem.pack(fill="x",pady=(0,14))
        tk.Label(body,text="SELECT BOOK (available only)",bg=SURFACE,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(0,4))
        self._iss_bk=ttk.Combobox(body,state="readonly",font=("Segoe UI",11),width=54); self._iss_bk.pack(fill="x",pady=(0,14))
        dr=tk.Frame(body,bg=SURFACE); dr.pack(fill="x",pady=(0,14))
        for lbl,attr in (("ISSUE DATE","_idt"),("DUE DATE","_idue")):
            df=tk.Frame(dr,bg=SURFACE); df.pack(side="left",expand=True,fill="x",padx=(0,10))
            tk.Label(df,text=lbl,bg=SURFACE,fg=MUTED,font=("Courier",8)).pack(anchor="w",pady=(0,4))
            e=mkEntry(df,bg=MIST,width=18); e.pack(fill="x",pady=3); setattr(self,attr,e)
        self._iss_err=tk.Label(body,text="",bg=SURFACE,fg=ROSE,font=("Segoe UI",10)); self._iss_err.pack(pady=4)
        Btn(body,"   Issue Book   ",cmd=self._do_issue,kind="primary").pack(fill="x",ipady=6,pady=(4,4))
        avail=[b for b in self.data["books"] if b["available"]>0]; self._avail_books=avail
        self._iss_mem["values"]=[f"{m['fname']} {m['lname']} - {m.get('type','')}" for m in self.data["members"]]
        self._iss_bk["values"]=[f"{b['title']} - {b['author']} ({b['available']} left)" for b in avail] or ["No books available"]
        if self._iss_mem["values"]: self._iss_mem.current(0)
        if avail: self._iss_bk.current(0)
        self._idt.insert(0,today()); self._idue.insert(0,(datetime.date.today()+datetime.timedelta(days=14)).isoformat())

    def _do_issue(self):
        self._iss_err.config(text="")
        mi=self._iss_mem.current(); bi=self._iss_bk.current()
        id_=self._idt.get().strip(); due=self._idue.get().strip()
        if mi<0: self._iss_err.config(text="Select a member"); return
        if bi<0 or not self._avail_books: self._iss_err.config(text="No available book selected"); return
        if not id_ or not due: self._iss_err.config(text="Enter both dates"); return
        if due<=id_: self._iss_err.config(text="Due date must be after issue date"); return
        mem=self.data["members"][mi]; book=self._avail_books[bi]
        if book["available"]<1: self._iss_err.config(text="Book no longer available"); return
        book["available"]-=1; mem["issued"]+=1
        self.data["issues"].append({"id":int(datetime.datetime.now().timestamp()),
            "book_id":book["id"],"member_id":mem["id"],"book_title":book["title"],
            "member_name":f"{mem['fname']} {mem['lname']}","issued":id_,"due":due,"returned":False,"fine":0})
        self.data["activity"].insert(0,{"txt":f'"{book["title"]}" issued to {mem["fname"]} {mem["lname"]}',"time":"just now"})
        save_data(self.data); self.toast(f'"{book["title"]}" issued!',"success"); self.navigate("returns")

    def _pg_returns(self):
        p=self._pages["returns"]; p.rowconfigure(1,weight=1); p.columnconfigure(0,weight=1)
        hd=tk.Frame(p,bg=BG); hd.grid(row=0,column=0,sticky="ew",padx=16,pady=(14,8))
        tk.Label(hd,text="Active Issues & Returns",bg=BG,fg=TXT,font=("Georgia",14,"bold")).pack(side="left")
        tk.Label(hd,text="Fine: Rs.2 / overdue day",bg=BG,fg=MUTED,font=("Courier",9)).pack(side="right")
        wrap=tk.Frame(p,bg=BG); wrap.grid(row=1,column=0,sticky="nsew",padx=16,pady=(0,16))
        wrap.rowconfigure(0,weight=1); wrap.columnconfigure(0,weight=1)
        self._rtree=mktree(wrap,("Book","Member","Issued","Due","Status","Fine","Action"),[215,155,95,95,95,70,90],height=18)
        self._rtree.bind("<Double-1>",self._do_return)
        active=[i for i in self.data["issues"] if not i["returned"]]
        if not active:
            self._rtree.insert("","end",values=("No active issues","","","","","",""),tags=("avail",))
        else:
            for iss in active:
                od=iss["due"]<today(); f=calc_fine(iss); d=days_diff(iss["due"],today()) if od else 0
                tag="overdue" if od else "issued"
                self._rtree.insert("","end",iid=str(iss["id"]),
                    values=(iss["book_title"],iss["member_name"],iss["issued"],iss["due"],
                            f"{d}d overdue" if od else "Active",f"Rs.{f}" if f else "--","Return"),
                    tags=(tag,))
        tk.Label(p,text="Double-click a row to return",bg=BG,fg=MUTED,font=("Courier",8)).grid(row=2,column=0,sticky="w",padx=16,pady=(0,4))

    def _do_return(self,_e=None):
        sel=self._rtree.selection()
        if not sel: return
        iid=int(sel[0]); iss=next((i for i in self.data["issues"] if i["id"]==iid),None)
        if not iss or iss["returned"]: return
        f=calc_fine(iss); msg=f'Return "{iss["book_title"]}"?'
        if f: msg+=f"\n\nOverdue fine: Rs.{f}"
        if not messagebox.askyesno("Confirm Return",msg): return
        iss["returned"]=True; iss["fine"]=f
        bk=next((b for b in self.data["books"] if b["id"]==iss["book_id"]),None)
        mem=next((m for m in self.data["members"] if m["id"]==iss["member_id"]),None)
        if bk:  bk["available"]=min(bk["copies"],bk["available"]+1)
        if mem: mem["issued"]=max(0,mem["issued"]-1)
        txt=f'"{iss["book_title"]}" returned'+(f" - Fine Rs.{f}" if f else "")
        self.data["activity"].insert(0,{"txt":txt,"time":"just now"})
        save_data(self.data); self.toast(txt,"success" if not f else "error"); self._pg_returns()

    def _pg_reports(self):
        p=self._pages["reports"]; p.rowconfigure(0,weight=1); p.columnconfigure(0,weight=1)
        inner=self._scroll_frame(p); inner.columnconfigure((0,1,2,3),weight=1)
        bks=self.data["books"]; iss=self.data["issues"]; mems=self.data["members"]
        ti=len(iss); ft=sum(calc_fine(i) for i in iss)
        am=len([m for m in mems if m["issued"]>0]); ret=len([i for i in iss if i["returned"]])
        for col,(ico,val,lbl,acc) in enumerate([("Issues",str(ti),"Total Issues",TEAL),("Fine",f"Rs.{ft}","Fines Collected",ROSE),("Members",str(am),"Active Members",EMERALD),("Ret.",str(ret),"Books Returned",CYAN)]):
            self._stat_card(inner,ico,val,lbl,acc,col)
        if HAS_MPL: self._draw_charts(inner,bks,iss,mems)
        else:
            lf=self._cframe(inner,1,0,4,"Top Issued Books",TEAL)
            cnts={}
            for i in iss: cnts[i["book_title"]]=cnts.get(i["book_title"],0)+1
            for title,count in sorted(cnts.items(),key=lambda x:-x[1])[:8]:
                r=tk.Frame(lf,bg=SURFACE); r.pack(fill="x",padx=16,pady=2)
                tk.Label(r,text=title,bg=SURFACE,fg=TXT,font=("Segoe UI",11)).pack(side="left")
                tk.Label(r,text=f"{count}x",bg=TEAL_PAL,fg=TEAL2,font=("Courier",10),padx=8).pack(side="right")
            msg=tk.Frame(inner,bg=TEAL_PAL); msg.grid(row=2,column=0,columnspan=4,sticky="ew",padx=16,pady=8)
            tk.Label(msg,text="  Install matplotlib for charts:  pip install matplotlib",bg=TEAL_PAL,fg=TEAL2,font=("Segoe UI",11),pady=10).pack(anchor="w")

    def _cframe(self,parent,row,col,colspan,title,accent):
        f=tk.Frame(parent,bg=SURFACE)
        f.grid(row=row,column=col,columnspan=colspan,
               padx=(16 if col==0 else 8,16 if col+colspan==4 else 8),
               pady=(8,8),sticky="nsew")
        tk.Frame(f,bg=accent,height=3).pack(fill="x")
        tk.Label(f,text=title,bg=SURFACE,fg=TXT,font=("Georgia",13,"bold")).pack(anchor="w",padx=16,pady=(10,4))
        return f

    def _draw_charts(self,parent,bks,iss,mems):
        # Genre Pie
        gf=self._cframe(parent,1,0,2,"Genre Distribution",TEAL)
        genres={}
        for b in bks: genres[b.get("genre","?")]=genres.get(b.get("genre","?"),0)+1
        fig1=Figure(figsize=(5,3.4),dpi=88,facecolor=SURFACE)
        ax1=fig1.add_subplot(111)
        ax1.pie(list(genres.values()),labels=list(genres.keys()),colors=CHART_COLORS[:len(genres)],
                autopct="%1.0f%%",startangle=140,textprops={"fontsize":8,"color":TXT},
                wedgeprops={"linewidth":2,"edgecolor":SURFACE})
        ax1.set_facecolor(SURFACE); fig1.tight_layout(pad=1.0)
        FigureCanvasTkAgg(fig1,master=gf).get_tk_widget().pack(fill="both",expand=True,padx=10,pady=(0,10))

        # Status Donut
        sf=self._cframe(parent,1,2,2,"Book Status",EMERALD)
        av_n=sum(b["available"] for b in bks)
        od_n=sum(1 for i in iss if not i["returned"] and i["due"]<today())
        is_n=max(0,sum(1 for i in iss if not i["returned"])-od_n)
        d_items=[(v,l,c) for v,l,c in [(av_n,"Available",TEAL),(is_n,"Issued",AMBER),(od_n,"Overdue",ROSE)] if v>0]
        fig2=Figure(figsize=(5,3.4),dpi=88,facecolor=SURFACE)
        ax2=fig2.add_subplot(111)
        if d_items:
            sz,lb,cl=zip(*d_items)
            ax2.pie(sz,labels=lb,colors=cl,autopct="%1.0f%%",startangle=90,pctdistance=0.75,
                    textprops={"fontsize":8},wedgeprops={"linewidth":2,"edgecolor":SURFACE,"width":0.52})
            tot=sum(b["copies"] for b in bks)
            ax2.text(0,0,str(tot),ha="center",va="center",fontsize=18,fontweight="bold",color=TXT)
            ax2.text(0,-0.28,"TOTAL",ha="center",va="center",fontsize=8,color=MUTED)
        ax2.set_facecolor(SURFACE); fig2.tight_layout(pad=1.0)
        FigureCanvasTkAgg(fig2,master=sf).get_tk_widget().pack(fill="both",expand=True,padx=10,pady=(0,10))

        # Bar chart
        bf=self._cframe(parent,2,0,4,"Top Issued Books",CYAN)
        cnts={}
        for i in iss: cnts[i["book_title"]]=cnts.get(i["book_title"],0)+1
        top=sorted(cnts.items(),key=lambda x:-x[1])[:7]
        fig3=Figure(figsize=(11,3.2),dpi=88,facecolor=SURFACE)
        ax3=fig3.add_subplot(111); ax3.set_facecolor(MIST)
        if top:
            xlbls=[t[:16]+"..." if len(t)>16 else t for t,_ in top]; vals=[v for _,v in top]
            bars=ax3.bar(xlbls,vals,color=CHART_COLORS[:len(xlbls)],edgecolor=SURFACE,linewidth=1.5,width=0.55)
            for bar,v in zip(bars,vals):
                ax3.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.04,str(v),ha="center",va="bottom",fontsize=9,fontweight="bold",color=TXT)
            ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)
            ax3.tick_params(axis="x",labelsize=8,colors=MUTED); ax3.tick_params(axis="y",labelsize=8,colors=MUTED)
            ax3.set_ylabel("Times Issued",fontsize=8,color=MUTED)
        else:
            ax3.text(0.5,0.5,"No data yet",ha="center",va="center",transform=ax3.transAxes,fontsize=12,color=MUTED)
        fig3.tight_layout(pad=1.0)
        FigureCanvasTkAgg(fig3,master=bf).get_tk_widget().pack(fill="both",expand=True,padx=10,pady=(0,10))

        # Member types pie
        mf=self._cframe(parent,3,0,2,"Member Types",VIOLET)
        mtypes={}
        for m in mems: mtypes[m.get("type","?")]=mtypes.get(m.get("type","?"),0)+1
        fig4=Figure(figsize=(5,3.0),dpi=88,facecolor=SURFACE)
        ax4=fig4.add_subplot(111)
        if mtypes:
            ax4.pie(list(mtypes.values()),labels=list(mtypes.keys()),colors=CHART_COLORS[:len(mtypes)],
                    autopct="%1.0f%%",startangle=140,textprops={"fontsize":8},
                    wedgeprops={"linewidth":2,"edgecolor":SURFACE})
        ax4.set_facecolor(SURFACE); fig4.tight_layout(pad=1.0)
        FigureCanvasTkAgg(fig4,master=mf).get_tk_widget().pack(fill="both",expand=True,padx=10,pady=(0,10))

        # Fines bar
        ff=self._cframe(parent,3,2,2,"Top Members by Fine",ROSE)
        fine_by={}
        for i in iss:
            f=calc_fine(i)
            if f: fine_by[i["member_name"]]=fine_by.get(i["member_name"],0)+f
        top_f=sorted(fine_by.items(),key=lambda x:-x[1])[:6]
        fig5=Figure(figsize=(5,3.0),dpi=88,facecolor=SURFACE)
        ax5=fig5.add_subplot(111); ax5.set_facecolor(MIST)
        if top_f:
            names=[n[:14] for n,_ in top_f]; fines=[v for _,v in top_f]
            hbars=ax5.barh(names,fines,color=ROSE,edgecolor=SURFACE,linewidth=1.5)
            for bar,v in zip(hbars,fines):
                ax5.text(v+0.2,bar.get_y()+bar.get_height()/2,f"Rs.{v}",va="center",fontsize=8,color=TXT)
            ax5.spines["top"].set_visible(False); ax5.spines["right"].set_visible(False)
            ax5.tick_params(labelsize=8,colors=MUTED); ax5.set_xlabel("Fine (Rs.)",fontsize=8,color=MUTED)
        else:
            ax5.text(0.5,0.5,"No fines yet",ha="center",va="center",transform=ax5.transAxes,fontsize=11,color=MUTED)
        fig5.tight_layout(pad=1.0)
        FigureCanvasTkAgg(fig5,master=ff).get_tk_widget().pack(fill="both",expand=True,padx=10,pady=(0,10))


if __name__=="__main__":
    login=LoginWindow()
    login.mainloop()
    if not login.current_user:
        raise SystemExit(0)
    app=App(login.current_user,login.data)
    app.mainloop()
