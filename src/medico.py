import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

Debug = False

# TODO : test, refactor; docs

class Medico(tk.Toplevel):
    def __init__(self, db=None, lang = 0):
        super().__init__()
        # self.parent = parent
        if db is None:
            self.destroy()
        self.db = db
        self.cur = self.db.cursor()
        self.cur.execute('SELECT nome FROM medicos ORDER BY nome')
        self.db.commit()
        self.lis = []
        for c in self.cur:
            self.lis.append(c[0])
        self.lang = lang
        self.id = 1        
        self.title(['Cadastro de Médicos', 'Physicians Register'][self.lang])
        self.wm_minsize(width=440, height=440)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid()
        
        
        # self.msg = ''

        # JANELA PACIENTES
        ttk.Label(self.frm, text=['C A D A S T R O   D E   M É D I C O S', 'P H Y S I C I A N S   R E G I S T E R'][self.lang]).grid(
            row=0, column=0, columnspan=4, pady=10)
        # ttk.Button(self.frm, text=['PT','EN'][self.lg.get()], textvariable =self.lg.get(), command=self.change_lang(), width=5).grid(row=0, column=4)
        

        # nome:
        ttk.Label(self.frm, text=['Nome: ','Name: '][self.lang]).grid(
            row=1, column=0, pady=10, sticky=tk.W)
        self.nome = tk.StringVar()
        self.nome_entry = ttk.Combobox(
            self.frm, width=54, textvariable=self.nome)
        self.nome_entry.grid(row=1, column=1, columnspan=3, sticky=tk.EW)
        self.nome_entry['values'] = self.lis
        self.nome_entry.bind('<<ComboboxSelected>>', self.get_by_nome)
        self.nome_entry.bind('<KeyRelease>', self.msg_press_new_doctor)     

        # fone:
        ttk.Label(self.frm, text=['Fone: ','Phone: '][self.lang]).grid(row=2, column=0, pady=10, sticky=tk.W)
        self.fone = tk.StringVar()
        ttk.Entry(self.frm,width=20, textvariable=self.fone).grid(row=2, column=1, sticky=tk.W)

        # especialidade:
        ttk.Label(self.frm, text=['Especialidade: ','Expertise: '][self.lang]).grid(row=3, column=0, pady=10, sticky=tk.W)
        self.especialidade = tk.StringVar()
        ttk.Entry(self.frm,width=64, textvariable=self.especialidade).grid(row=3, column=1,columnspan=3, sticky=tk.W)
        

        # crm:
        ttk.Label(self.frm, text=['CRM: ','MR:'][self.lang]).grid(row=2, column=2,  padx=5, pady=10, sticky=tk.E)
        self.crm = tk.StringVar()
        ttk.Entry(self.frm,width=20, textvariable=self.crm).grid(row=2, column=3, sticky=tk.W)

        # obs:
        ttk.Label(self.frm, text=['Obs: ','Note:'][self.lang]).grid(row=4, column=0, pady=10, sticky=tk.W)
        self.obs = tk.StringVar()
        ttk.Entry(self.frm,width=64, textvariable=self.obs).grid(row=4, column=1,columnspan=3, sticky=tk.W)

        # messages
        # ttk.Label(self.frm, textvariable=self.msg).grid(row=5, column=1, columnspan=3, pady=15, sticky=tk.W)
        
        # novo :
        ttk.Button(self.frm, text=['Novo Médico','New Doctor'][self.lang], width=15, command=self.novo_medico).grid(
            row=8, column=1, pady=50, sticky=tk.W)
        # salvar :
        ttk.Button(self.frm, text=['Salvar Médico','Save Doctor'][self.lang], width=15,  command=self.salvar_medico).grid(
            row=8, column=2, padx=15, pady=50, sticky=tk.S)
        # apagar:
        ttk.Button(self.frm, text=['Apagar Médico','Delete Doctor'][self.lang], width=15,  command=self.apagar_medico).grid(
            row=8, column=3, padx=5, pady=50, sticky=tk.E)
        # voltar:
        ttk.Button(self.frm, text=['Voltar','Exit'][self.lang], width=15, command=self.destroy).grid(
            row=9, column=2, padx=15, sticky=tk.S)

    # def change_lang(self):
    #     self.lg.set( 1 if self.lg.get() == 0 else 0) 
    #     print(self.lg.get())    

    def msg_press_new_doctor(self, *ignore):
        if self.id == 1:
            messagebox.showinfo(['Por favor','Please'][self.lang],['Digite: Novo Médico', 'Press: New Doctor.'][self.lang], parent = self)
        return

    def listar_medicos(self):
        self.cur.execute('SELECT nome FROM medicos ORDER BY nome')
        self.db.commit()
        self.lis.clear()
        for c in self.cur:
            self.lis.append(c[0])
        self.nome_entry['values'] = self.lis

    def get_by_nome(self, *ignore):
        medico = self.nome.get()
        self.cur.execute(
            'SELECT nome, id FROM medicos WHERE nome =?', (medico,))
        self.db.commit()
        regs = self.cur.fetchall()
        self.id = regs[0][1]
        self.get_by_id(self.id)

    def get_by_id(self, id):   
        debug = False
        self.cur.execute('''SELECT m.*
                    FROM medicos m
                    WHERE
                    m.id = ?                                              
                    ''', (id,))
        self.db.commit()
        regs = self.cur.fetchall()
        print('Doctors: ',regs) if debug or Debug else ...
        regs = regs[0]
        self.id = id
        self.nome.set(regs[1])
        self.fone.set(regs[2])
        self.especialidade.set(regs[3])
        self.crm.set(regs[4])
        self.obs.set(regs[5])

    # def limpar_campos(self):
    #     self.get_by_id(1)

    def novo_medico(self):
        debug= True
        txt = ['INSIRA O NOME DO MÉDICO','iNSERT DOCTOR\'S NAME'][self.lang]
        self.cur.execute("INSERT INTO medicos (nome, fone, especialidade, crm, obs) VALUES (?,' ','','','')",(txt,))
        self.db.commit()
        self.cur.execute("SELECT * FROM medicos WHERE id = ( SELECT MAX(id) FROM medicos)")
        # self.db.commit()
        # print(f'New doctor: {self.cur.fetchall()}') if debug or Debug else ...
        self.id = self.cur.fetchall()[0][0]
        self.get_by_id(self.id)

    def apagar_medico(self):
        resp = messagebox.askyesno(['Apagar','Delete'][self.lang], 
        ['Deseja realmente apagar o médico %s do Banco de Dados?'%(self.nome.get()),'Do you really want to delete the doctor %s to the database?'%(self.nome.get())][self.lang], parent=self)
        if not resp or self.id == 1 :
            return
        self.cur = self.db.cursor()
        self.cur.execute('DELETE FROM medicos WHERE id = ?', (self.id,))
        self.db.commit()        
        self.listar_medicos()        
        self.get_by_id(1)

    def salvar_medico(self):        
        if self.id == 1: return
        self.cur.execute('''UPDATE medicos SET
                nome = ?, fone = ?, especialidade =?, crm = ?, obs = ?
                WHERE id = ?''', 
                (self.nome.get(), self.fone.get(), self.especialidade.get(), 
                self.crm.get(), self.obs.get(),self.id))
        self.db.commit()
        self.cur.execute('SELECT nome FROM medicos ORDER BY nome')
        self.db.commit()
        self.lis = []
        for c in self.cur:
            self.lis.append(c[0])
        self.nome_entry['values'] = self.lis        
        self.get_by_id(1)

    

