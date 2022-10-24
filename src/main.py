import os
import sys
import tkinter as tk
import sqlite3 as sq
import pandas as pd
import requests as rq
from tkinter import messagebox
from create_tables import create_tables, populate_tables
from tkinter import ttk
from iso8601 import from_iso8601, to_iso8601
from medico import Medico
from consultas import Consultas

Debug = False

# TODO: refactor, docs, upload to GitHub


class MainWin(tk.Tk):
    def __init__(self, args):

        # USE <python main.py en database_name> TO SET LANGUAGE TO ENGLISH and set the database name.
        self.db_name = 'clinic.db'       
        if len(args) > 1:
            # add your language if you need
            match args[1].upper():
                case 'EN':  self.lang= 1 # English                
                case   _ :  self.lang= 0 # Portuguese Pt-Br            
        elif len(args) > 2:
            self.db_name = args[2]
        else:
            self.lang = 0


        # CREATE OR OPEN DATA BASE
        self.db_nome = os.path.join(os.path.dirname(__file__), self.db_name)
        if not os.path.exists(self.db_nome):
            create_tables(self.db_nome)
            populate_tables(self.db_nome)
        self.db = sq.connect(self.db_nome)
        self.id = 1      
       
        # CREATE A MAIN WINDOWS
        tk.Tk.__init__(self)        
        self.wm_title(['Clínica XYZ - Cadastro de Pacientes','XYZ Clinic - Patients Register'][self.lang])
        self.wm_minsize(width=440, height=440)        
        self.frm = ttk.Frame(self, padding=10,  )        
        self.frm.grid()  
        ttk.Label(self.frm, text=['C A D A S T R O   DE   P A C I E N T E S','P A T I E N T S   R E G I S T E R'][self.lang] ).grid(row=0,column=0, columnspan=3, pady=10)        

        # FORM FIELDS:
        # NAME:
        ttk.Label(self.frm, text = ['Nome: ','Name:'][self.lang]).grid(row=1, column=0, pady=5, sticky=tk.W)
        self.nome = tk.StringVar()
        self.nome_entry = ttk.Combobox(self.frm, width=54, textvariable=self.nome)
        self.nome_entry.grid(row=1, column=1, columnspan=3, sticky=tk.EW) 
        self.nome_entry['values'] = self.listar_pacientes()    
        self.nome_entry.bind('<KeyRelease>', self.check_input)           
        self.nome_entry.bind('<<ComboboxSelected>>', self.get_by_nome)        
        # PHONE:
        ttk.Label(self.frm, text=['Fone: ','Phone: '][self.lang]).grid(row=2, column=0, pady=5, sticky=tk.W)
        self.fone = tk.StringVar()
        ttk.Entry(self.frm,width=20, textvariable=self.fone).grid(row=2, column=1, sticky=tk.W)
        # INSURENCE:
        ttk.Label(self.frm, text=['Convenio: ','Insurance: '][self.lang]).grid(row=2, column=2, padx=25, pady=5, sticky=tk.W)
        self.convenio = tk.StringVar()
        self.convenio_entry = ttk.Combobox(self.frm, width=19, textvariable=self.convenio)
        self.convenio_entry.grid(row=2, column=3, sticky=tk.W)
        self.convenio_entry['values'] = [('Particular', 'Unimed', 'Bradesco', 'Cassi'),('Private','United','Kaiser', 'Anthem','Centene', 'Humana','CVS')][self.lang]       
        # GENRE:
        ttk.Label(self.frm, text=['Sexo: ','Genre:'][self.lang]).grid(row=3, column=0, pady=5, sticky=tk.W)
        self.sexo = tk.StringVar()
        self.sexo_entry = ttk.Combobox(self.frm, width=17, textvariable=self.sexo)
        self.sexo_entry.grid(row=3, column=1, sticky=tk.W)
        self.sexo_entry['values'] = [('Masculino', 'Feminino', 'Outro', 'Não informado'),('Male','Female','Other','Not informed')][self.lang]
        # CARD NUMBER:
        ttk.Label(self.frm, text=['Cartao: ','Card Numb:'][self.lang]).grid(row=3, column=2,padx=25, pady=5, sticky=tk.W)
        self.cartao = tk.StringVar()
        ttk.Entry(self.frm,width=22, textvariable=self.cartao).grid(row=3, column=3, sticky=tk.W)        
        # EMAIL:
        ttk.Label(self.frm, text='Email: ').grid(row=4, column=0, pady=5, sticky=tk.W)
        self.email = tk.StringVar()
        ttk.Entry(self.frm,width=20, textvariable=self.email).grid(row=4, column=1, sticky=tk.W)
        # BIRTH DATE:
        ttk.Label(self.frm, text=['Nascimento: ','Birth date:'][self.lang]).grid(row=4, column=2, padx=25, pady=5, sticky=tk.W)
        self.data_nasc = tk.StringVar()    
        self.data_nasc.set(['dd/mm/aaaa','mm-dd-yyyy'][self.lang])  
        self.data_nasc_entry= ttk.Entry(self.frm,width=22, textvariable=self.data_nasc)
        self.data_nasc_entry.grid(row=4, column=3, sticky=tk.W)
        self.data_nasc_entry.bind('<FocusOut>', self.chk_date) 
         # ZIP CODE:
        ttk.Label(self.frm, text=['CEP: ','ZIP Code: '][self.lang]).grid(row=5, column=0,  pady=5, sticky=tk.W)
        self.cep = tk.StringVar()               
        self.cep_entry= ttk.Entry(self.frm,width=20, textvariable=self.cep)
        self.cep_entry.grid(row=5, column=1, sticky=tk.W)
        self.cep_entry.bind('<FocusOut>', self.chk_cep)
        # CITY:
        ttk.Label(self.frm, text=['Cidade: ','City: '][self.lang]).grid(row=5, column=2, pady=5,padx=25, sticky=tk.W)
        self.cidade = tk.StringVar()
        ttk.Entry(self.frm,width=22, textvariable=self.cidade).grid(row=5, column=3, sticky=tk.W)
        # ADDRESS:
        ttk.Label(self.frm, text=['Endereço: ','Address: '][self.lang]).grid(row=6, column=0, pady=5, sticky=tk.W)
        self.endereco = tk.StringVar()
        ttk.Entry(self.frm,width=57, textvariable=self.endereco).grid(row=6, column=1, columnspan=3, sticky=tk.EW)        
        # NOTE:
        ttk.Label(self.frm, text=['Observações: ','Note:'][self.lang]).grid(row=7, column=0, pady=5, sticky=tk.W)
        self.obs = tk.StringVar()
        ttk.Entry(self.frm,width=57, textvariable=self.obs).grid(row=7, column=1, columnspan=3, sticky=tk.EW)
        
        # BUTTONS:        
        ttk.Button(self.frm, text=['Novo Paciente','New Patient'][self.lang], width=15, command=self.novo_paciente).grid(row=8, column=1, pady=50, sticky=tk.W )        
        ttk.Button(self.frm, text=['Consultas','Appointments'][self.lang],width=15,  command=self.consultas).grid(row=9, column=1, sticky=tk.W )        
        ttk.Button(self.frm, text=['Salvar Paciente','Save Patient'][self.lang],width=15,  command=self.salvar_paciente).grid(row=8, column=2,padx=15, pady=50, sticky=tk.S)        
        ttk.Button(self.frm, text=['Salvar Excel','Save Excel'][self.lang], width=15, command=self.salvar_xlsx).grid(row=9, column=2,padx=15, sticky=tk.S )  
        ttk.Button(self.frm, text=['Apagar Paciente','Delete Patient'][self.lang],width=15,  command=self.apagar_paciente).grid(row=8, column=3,padx=5, pady=50, sticky=tk.E )        
        ttk.Button(self.frm, text=['Médicos','Doctors'][self.lang],width=15,  command=self.medicos).grid(row=9, column=3,padx=5, sticky=tk.E)

    def chk_date(self, *ignore):
        debug = False
        print(self.data_nasc.get()) if debug or Debug else ...
        dataNasc: list = to_iso8601(self.data_nasc.get(),['d','m'][self.lang])
        print('dataNasc is valid: ',dataNasc[0]) if debug or Debug else ...
        print('dataNasc: ',dataNasc[1]) if debug or Debug else ...
        if dataNasc[0] == False:
            self.data_nasc.set(dataNasc[1])
        return dataNasc[1]            

    def chk_cep(self, *ignore):
        debug = False
        print(self.cep.get()) if debug or Debug else ...
        req = rq.get([f"https://viacep.com.br/ws/{self.cep.get()}/json/",f"https://api.zippopotam.us/us/{self.cep.get()}"][self.lang])
        try:        
            data = req.json()
        except:
            self.cep.set(['CEP inválido','Invalid ZIP Code'][self.lang])
            self.cidade.set('')    
            self.endereco.set('')
        else:    
            if 'erro' not in data and self.lang !=1:                  
                self.cep.set(data['cep'])  
                self.cidade.set(data['localidade'] + ' '+ data['uf'])  
                self.endereco.set(data['logradouro'] + ' ' + data['complemento'] + ',<INSIRA O NÚMERO> ' + data['bairro'])     
            elif data != {}:
                self.cep.set(data['post code'])  
                self.cidade.set(data['places'][0]['place name']+ ' '+ data['places'][0]['state abbreviation'])  
            else:
                self.cep.set(['CEP inválido','Invalid ZIP Code'][self.lang]) 
                self.cidade.set('')    
                self.endereco.set('')

    def listar_pacientes(self):
        lis = []
        cur = self.db.cursor()
        cur.execute('SELECT nome FROM pacientes ORDER BY nome')
        self.db.commit()        
        for c in cur:
            lis.append(c[0])
        return lis
    
    def check_input(self, event):
        val = event.widget.get()
        lis = self.listar_pacientes()
        if val == '':
            self.nome_entry['values'] = lis
        else:
            lis_pac = []
            for pac in lis:
                if val.lower() in pac.lower():
                    lis_pac.append(pac)
                self.nome_entry['values'] = lis_pac

    def get_by_nome(self, *ignore):
        paciente = self.nome.get()
        cur = self.db.cursor()
        cur.execute('SELECT nome, id FROM pacientes WHERE nome =?',(paciente,))
        self.db.commit()        
        regs = cur.fetchall()
        self.id = regs[0][1]
        self.get_by_id(self.id)
        
    def get_by_id(self, id):        
        debug = False
        cur = self.db.cursor()
        cur.execute('''SELECT p.*
                        FROM pacientes p
                        WHERE
                        p.id = ?                                              
                        ''', (id,))
        self.db.commit()
        regs = cur.fetchall()
        print('patients: ',regs) if debug or Debug else ...
        regs = regs[0]
        self.nome.set(regs[1])
        self.fone.set(regs[2])
        self.convenio.set(regs[3])
        self.cartao.set(regs[4])
        self.sexo.set(regs[5])
        self.email.set(regs[6])
        self.data_nasc.set(from_iso8601((regs[7]),['D/','M-'][self.lang],self.lang)[1][:10])
        self.endereco.set(regs[8])
        self.cidade.set(regs[9])
        self.cep.set(regs[10])
        self.obs.set(regs[11])      
        
    def apagar_paciente(self):
        resp = messagebox.askyesno(['Apagar','Delete'][self.lang], 
        [f'Deseja realmente apagar {self.nome.get()} do Banco de Dados?', f'Do you really want to delete {self.nome.get()} to the database?'][self.lang], parent=self)
        if not resp or self.id == 1 :
            return
        cur = self.db.cursor()
        cur.execute('DELETE FROM pacientes WHERE id = ?', (self.id,))
        self.db.commit()
        self.nome_entry['values'] = self.listar_pacientes()
        self.get_by_id(1) 

    def novo_paciente(self):
        cur = self.db.cursor()
        text = ['SALVE APÓS PREENCHER','SAVE AFTER COMPLETED'][self.lang]
        cur.execute('''INSERT INTO pacientes 
                    (nome , fone , convenio , cartao , sexo , email , data_nasc , endereco , cidade , cep , obs)
                    VALUES                    
                    ( '' , '', '', '', '', '', '', '', '', '', ?)''',(text,))
        cur.execute('SELECT MAX(p.id) FROM pacientes p')
        self.id = cur.fetchall()[0][0]
        self.get_by_id(self.id)

    def medicos(self):
        Medico(self.db, self.lang)   

    def consultas(self):
        Consultas(self.db, self.lang, self.id )

    def salvar_paciente(self):
        debug = False        
        if self.id == 1 or to_iso8601( self.data_nasc.get(),['d','m'][self.lang])[0] == False:
            self.data_nasc_entry.focus()
            return
        print('salvei paciente') if debug or Debug else ...
        cur = self.db.cursor()
        cur.execute('''UPDATE pacientes SET
                nome = ?, fone = ?, convenio =?, cartao = ?, sexo = ?, email = ?,
                data_nasc = ?, endereco = ?, cidade = ?, cep = ?, obs = ?
                WHERE id = ?''', 
                (self.nome.get(), self.fone.get(), self.convenio.get(), 
                self.cartao.get(), self.sexo.get(),self.email.get(),self.chk_date(self.data_nasc.get()),
                self.endereco.get(),self.cidade.get(),self.cep.get(),self.obs.get(),self.id))
        self.db.commit()
        cur.execute('SELECT nome FROM pacientes ORDER BY nome')
        self.db.commit()
        lis = []
        for c in cur:
            lis.append(c[0])
        self.nome_entry['values'] = lis
        self.get_by_id(1)
    
    def salvar_xlsx(self):
        debug = False
        cur = self.db.cursor()
        cur.execute('SELECT * FROM pacientes')
        pacientes_cadastrados = cur.fetchall()
        self.db.commit()
        cur.execute('''SELECT p.nome, m.nome, c.*       
                        FROM pacientes p, medicos m, consultas c
                        WHERE c.paciente_id = p.id
                        AND c.medico_id = m.id''')
        consultas_cadastradas = cur.fetchall()
        self.db.commit() 
        cur.execute('SELECT * FROM medicos')
        medicos_cadastrados = cur.fetchall()
        self.db.commit()       
        pacientes_cadastrados = pd.DataFrame(pacientes_cadastrados, columns=[['id_bd','nome','fone','convenio','cartão','sexo','email','nascimento','endereço','cidade','cep','obs'],['id_bd','name','phone','insurance','card number','genre','email','birth day','address','city','zip','note']][self.lang])
        consultas_cadastradas = pd.DataFrame(consultas_cadastradas, columns=[['paciente','medico','id_db','data','status','observação','id_paciente','id_medico'],['patient','doctor','id_db','date','status','note','id_patient','id_doctor']][self.lang])
        medicos_cadastrados = pd.DataFrame(medicos_cadastrados,columns = [['id_db','nome','fone','especialidade','crm','observações'],['id_db','name','phone','specialty','register','notes']][self.lang])
        print('Appointments: ',consultas_cadastradas) if debug or Debug else ...
        with pd.ExcelWriter([f'registros_pacientes_{self.db_name[:-3]}.xlsx',f'patients_records_{self.db_name[:-3]}.xlsx'][self.lang]) as writer:
            pacientes_cadastrados.to_excel(writer,sheet_name=['pacientes','patients'][self.lang])
            consultas_cadastradas.to_excel(writer,sheet_name=['consultas','appointments'][self.lang] )
            medicos_cadastrados.to_excel(writer,sheet_name=['medicos','doctors'][self.lang])
    
    def __del__(self):
        if self.db is not None:
            self.db.close()

if __name__ == '__main__':    
    app = MainWin(sys.argv)
    app.mainloop()