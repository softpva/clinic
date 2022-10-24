

from multiprocessing import parent_process
import tkinter as tk
# import datetime as dt
from tkinter import Toplevel, ttk
from tkinter import messagebox
from iso8601 import from_iso8601, to_iso8601, weekday

Debug = False



# TODO : test, refactor; docs


class Consultas(tk.Toplevel):
    '''
        This is a toplevel class to class MainWin os main.py


        Its constructor receives:
        db: str -> database's name
        lang: int -> 0:pt, 1:en
        id_paciente: int -> patient id from the database    
    '''
    def __init__(self, db=None, lang=0, id_paciente=1):
        super().__init__()
        if db is None:
            self.destroy()
        self.db = db

        self.lang = lang
        self.id_consulta = 1
        self.id_medico = 1
        self.id_pac = id_paciente
        self.cur = self.db.cursor()
        self.lis = []              
        self.nome_pac = ''

        self.title(['C O N S U L T A S', 'A P P O I N T M E N T S'][self.lang])
        self.wm_minsize(width=440, height=440)
        self.frm = ttk.Frame(self, padding=10)
        self.frm.grid()   

        # JANELA CONSULTAS
        ttk.Label(self.frm, text=['C O N S U L T A S', 'A P P O I N T M E N T S'][self.lang]).grid(row=0, column=0, columnspan=4, pady=10)

        # Patient data:
        self.cur.execute("SELECT nome FROM pacientes WHERE id = ?",(self.id_pac,))
        self.nome_pac = self.cur.fetchall()[0][0]
        self.db.commit()
        self.lis.clear()
        self.cur.execute('''SELECT c.data_consulta FROM consultas c
                            WHERE c.paciente_id = ?
                            ORDER BY c.data_consulta''',(self.id_pac,))
        self.db.commit()        
        for c in self.cur:
            self.lis.append(c[0])  
        # print(self.nome_pac)
        ttk.Label(self.frm, text=['Paciente: ','Patient: '][self.lang]).grid(row=1, column=0, pady=10, sticky=tk.W)
        ttk.Label(self.frm, text=self.nome_pac).grid(row=1, column=1, pady=10, sticky=tk.W)

        # Choose the Doctor:
        ttk.Label(self.frm, text=['Médico: ','Doctor: '][self.lang]).grid(row=2, column=0, pady=10, sticky=tk.W)        
        self.medico = tk.StringVar()
        self.medico_entry = ttk.Combobox(
            self.frm, width=54, textvariable=self.medico)
        self.medico_entry.grid(row=2, column=1, columnspan=3, sticky=tk.EW)        
        self.get_medicos()
        self.medico_entry['values'] = self.lis
        self.medico_entry.bind('<<ComboboxSelected>>', self.get_medicos)   

        # consulta:
        ttk.Label(self.frm, text=['Consulta: ','Appointment: '][self.lang]).grid(row=3, column=0, pady=10, sticky=tk.W)
        self.consulta = tk.StringVar()
        self.weekday = tk.StringVar()
        self.weekday.set('')
        self.consulta.set(['dd/mm/aaaa hh:mm','mm-dd-yyyy hh:mm'][self.lang]) 
        self.consulta_entry = ttk.Combobox(
            self.frm, width=40, textvariable=self.consulta)
        self.consulta_entry.grid(row=3, column=1, columnspan=2, sticky=tk.EW)
        self.listar_consulta()        
        self.consulta_entry.bind('<<ComboboxSelected>>', self.get_consulta)
        # self.consulta_entry.bind('<KeyRelease>', self.alter_weekday)
        self.consulta_entry.bind('<KeyRelease>', self.msg_press_new_appointment)


        self.weekday_label = tk.Label(self.frm, text = '')
        self.weekday_label.grid(row=3,column=3,padx=15,sticky=tk.W)        
        print('wd:',self.weekday.get())  if Debug else ...
        

        # status:
        ttk.Label(self.frm, text=['Estado: ','Status: '][self.lang]).grid(row=4, column=0, pady=10, sticky=tk.W)
        self.status = tk.StringVar()
        self.status_entry = ttk.Combobox(self.frm, width=19, textvariable=self.status)
        self.status_entry.grid(row=4, column=1, sticky=tk.EW)
        self.status_entry['values'] = [('A AGENDAR', 'AGENDADA', 'CANCELADA', 'FEITA'),('To Schedule', 'Scheduled', 'Canceled', 'Done')][self.lang]        

        # observacao:
        ttk.Label(self.frm, text=['Observações: ','Note:'][self.lang]).grid(row=7, column=0, pady=5, sticky=tk.W)
        self.obs = tk.StringVar()
        ttk.Entry(self.frm,width=57, textvariable=self.obs).grid(row=7, column=1, columnspan=3, sticky=tk.EW)        
    
        # novo :
        ttk.Button(self.frm, text=['Nova Consulta','New Appoint.'][self.lang], width=15, command=self.nova_consulta).grid(
            row=8, column=1, pady=50, sticky=tk.W)
        # salvar :
        ttk.Button(self.frm, text=['Salvar Cosulta','Save Appoint.'][self.lang], width=15, command=self.salvar_consulta).grid(
            row=8, column=2, padx=15, pady=50, sticky=tk.S)
        # apagar:
        ttk.Button(self.frm, text=['Apagar Consulta','Delete Appoint.'][self.lang], width=15, command=self.apagar_consulta).grid(
            row=8, column=3, padx=5, pady=50, sticky=tk.E)
        # voltar:
        ttk.Button(self.frm, text=['Voltar','Exit'][self.lang], width=15, command=self.destroy).grid(
            row=9, column=2, padx=15, sticky=tk.S)

    def msg_press_new_appointment(self, *ignore):
        if self.id_consulta == 1:
            messagebox.showinfo(['Por favor','Please'][self.lang],['Digite: Nova Consulta', 'Press: New Appoint.'][self.lang], parent = self)
            return
        else:
            self.alter_weekday()

    def salvar_consulta(self, *ignore):        
        debug = False
        if self.id_consulta == 1: return
        print('Appoint: ',self.consulta.get()) if debug or Debug else ...
        if self.id_consulta == 0 : 
            messagebox.showinfo(['Por favor','Please'][self.lang],['Digite: Nova Consulta', 'Press: New Appoint.'][self.lang],parent = self)
            return
        self.cur.execute('''UPDATE consultas SET data_consulta = ?, status = ?, obs = ?, medico_id = ? WHERE id = ?''',
        (to_iso8601(self.consulta.get(),['D','M'][self.lang])[1],self.status.get(), self.obs.get(), self.id_medico, self.id_consulta ))
        print('saved appoint to_iso8601',to_iso8601(self.consulta.get(),['D','M'][self.lang])[1]) if debug == True or Debug == True else ...
        self.db.commit()
        self.listar_consulta()
        self.apagar_campos()

        

    def apagar_consulta(self):
        resp = messagebox.askyesno(['Apagar','Delete'][self.lang], 
        ['Deseja realmente apagar a consulta de %s do Banco de Dados?'%(self.consulta.get()),'Do you really want to delete the appointment %s to the database?'%(self.consulta.get())][self.lang], parent=self)
        if not resp or self.id_consulta == 1 :
            return
        self.cur.execute('DELETE FROM consultas WHERE id = ?', (self.id_consulta,))
        self.db.commit()  
        # self.id_consulta = 1
        self.listar_consulta()
        self.apagar_campos()      
        
        
    def listar_consulta(self, *ignore):
        debug = False
        self.lis.clear()
        self.cur.execute('''SELECT c.data_consulta FROM consultas c
                            WHERE (c.paciente_id = ?
                            AND c.medico_id = ?)
                            ORDER BY c.data_consulta''',(self.id_pac, self.id_medico,))
        self.db.commit()        
        for c in self.cur:
            self.lis.append(from_iso8601(c[0],['D/','M-'][self.lang])[1])
        self.consulta_entry['values'] = self.lis
        print('Appointmentes: ', self.lis) if debug or Debug else ...

    def nova_consulta(self):   
        debug = False   
        self.cur.execute("INSERT INTO consultas (data_consulta, status, obs, paciente_id,medico_id ) VALUES (strftime('%Y-%m-%dT%H:%M','now'),?,'',?,?)",('',self.id_pac, self.id_medico))
        self.db.commit()
        self.cur.execute(" SELECT * FROM consultas WHERE id = ( SELECT MAX(id) FROM consultas)")
        regs = self.cur.fetchall()[0]
        self.consulta.set(from_iso8601(regs[1],['D/','M-'][self.lang])[1])
        print('New appointment insert into db : ',regs) if debug or Debug else ...
        self.get_consulta()        
    
    def get_consulta(self, *ignore):
        debug = False
        consulta = to_iso8601(self.consulta.get(),['D','M'][self.lang])[1]
        print('Appointment caught from ui: ',consulta) if debug or Debug else ...
        self.cur.execute(
            'SELECT id, data_consulta, status, obs FROM consultas WHERE data_consulta =?', (consulta,))
        self.db.commit()
        regs = self.cur.fetchall()
        print('Appointment read from db: ', regs) if debug or Debug else ...
        regs = regs[0]
        self.id_consulta = regs[0]        
        self.consulta.set(from_iso8601(regs[1],['D/','M-'][self.lang])[1])
        self.weekday.set(from_iso8601(regs[1],['D/','M-'][self.lang])[2])
        print(regs[1])
        print(self.weekday.get())
        self.alter_weekday()        
        self.show_weekday()
        self.status.set(regs[2])
        self.obs.set(regs[3])
    
    def show_weekday(self):
        wd = self.weekday.get()
        txt = f"{self.weekday.get()}   Reg: {self.id_consulta}" if wd != '' else ''
        color = '#FF0000' if wd == ['Sábado','Saturday'][self.lang] or wd == ['Domingo','Sunday'][self.lang] else '#0000FF'        
        self.weekday_label.destroy()
        self.weekday_label = tk.Label(self.frm, text = txt , foreground= color)
        self.weekday_label.grid(row=3,column=3,padx=15,sticky=tk.W)

    def alter_weekday(self, *ignore):
        debug = False
        date = self.consulta.get()
        date = to_iso8601(date,['D','M'][self.lang])
        if date[0] == True:
            date = date[1]
            date = from_iso8601(date,['D/','M-'][self.lang],self.lang)
            print(date) if debug or Debug else ...
            if date[0] == True:
                date = date[2]
            else:
                date = ''
        else:
            date = ''
        print(date) if debug or Debug else ...  
        print('self.lang= ',self.lang) if debug or Debug else ...
        self.weekday.set(date)  
        self.show_weekday()

    def apagar_campos(self):
        self.medico.set('')
        self.id_medico = 1
        self.id_consulta = 1        
        self.consulta.set('')
        self.status.set('')
        self.obs.set('')
        self.weekday.set('')
        self.listar_consulta()
        self.show_weekday()       
                    

    def get_medicos(self, *ignore):
        debug = False
        self.lis.clear()
        self.cur.execute('''SELECT m.nome FROM medicos m 
                           ORDER BY m.nome''')                           
        self.db.commit()        
        for c in self.cur:
            self.lis.append(c[0])
        self.medico_entry['values'] = self.lis
        print('medical list: ',self.lis) if debug or Debug else ...
        self.cur.execute("SELECT m.id FROM medicos m WHERE m.nome = ?",(self.medico.get(),))
        self.id_medico = self.cur.fetchall()[0][0]
        print('Medico: %s, id: %s' % (self.medico.get(),self.id_medico)) if debug or Debug else ...
        if self.id_medico != 1:
            self.listar_consulta()
        

        

