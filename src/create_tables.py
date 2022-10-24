import sqlite3 as sq


# CREATE DATA BASE


def create_tables(db_name):

    con = sq.connect(db_name)
    cur = con.cursor()

    # CREATE TABLES
    cur.execute(
        '''
        CREATE TABLE pacientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            nome TEXT NOT NULL,            
            fone TEXT  NOT NULL,
            convenio TEXT, 
            cartao TEXT,
            sexo TEXT,
            email TEXT,
            data_nasc TEXT,            
            endereco TEXT,
            cidade TEXT,
            cep TXT,            
            obs TEXT            
            )'''
    )
    cur.execute(
        '''
        CREATE TABLE consultas(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,   
            data_consulta TEXT,
            status TEXT NOT NULL,
            obs TEXT,
            paciente_id INTEGER NOT NULL,
            medico_id INTEGER NOT NULL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
            FOREIGN KEY (medico_id) REFERENCES medicos(id)
        )'''
    )
    cur.execute(
        '''
        CREATE TABLE medicos(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            nome TEXT NOT NULL,            
            fone TEXT NOT NULL,
            especialidade TEXT,
            crm TEXT,
            obs TEXT
        )'''
    )    
    con.commit()
    con.close()


def populate_tables(db_name):
    con = sq.connect(db_name)
    cur = con.cursor()
    cur.execute('''
        INSERT INTO medicos
        ("id", "nome", "fone", "especialidade", "crm","obs")
        VALUES 
        ('1', '', '', '', '', ''),
        ('2', 'Dr. John Smith Test', '1234.5678', 'Cardiologist ', '123.456', 'Only Private'),
        ('3', 'Dr. Lucas Test', '1111.2222', 'Dermatologist', '111.222', 'United'),
        ('4', 'Dr. Paul Test', ' 3333.4444', 'Geriatric', '333.444', 'All'),
        ('5', 'Dr. Joe Smith Test', ' 5555.6666', 'Urologist', '555.666', 'Kaiser and Anthem');
    ''')
    cur.execute('''
        INSERT INTO pacientes  
        ("id", "nome", "fone", "convenio", "cartao", "sexo", "email", "data_nasc", "endereco", "cidade", "cep", "obs")     
        VALUES 
        ('1', '', '', '', '', '', '', '', '', '', '', ''),
        ('2', 'Mr. Peter Test', '1234.5678', 'Private', '123.456', 'Male', 'peter@email.com', '1969-06-25T00:00', '123, Main Street', 'Pflugerville TX', '78691', ''),
        ('3', 'Ms. Mary Test', '1234.9999', 'Private', '123.123', 'Female', 'mary@email.com', '1979-06-25T00:00', '123, Main Street', 'Pflugerville TX', '78691', ''),
        ('4', 'Mr John Test', '1111.9999', 'United', '985.258', 'Male', 'john@email.com', '2000-12-30T00:00', 'Empire State Building, apt 3020', 'New York City NY', '10118', ''),
        ('5', 'Ms. Philip Test', '9876.5432', 'Anthem', '444.522', 'Female', 'philip@email.com', '2000-05-25T00:00', 'Park Avenue, apt 222', 'New York City NY', '10178', 'Allergic to dipirone');
    ''')
    cur.execute('''
        INSERT INTO consultas
        ("id","data_consulta", "status", "obs", "paciente_id", "medico_id")
        VALUES         
        ('1', '', '', '', '1', '1'),
        ('2', '2022-11-24T12:41', 'Scheduled', 'He will need to bring an echocardiogram', '2', '2'),
        ('3', '2022-10-28T14:17', 'Scheduled', '', '5', '3'),
        ('4', '2022-11-22T14:00', 'Scheduled', '', '5', '4'),
        ('5', '2022-10-28T14:46', 'Scheduled', '', '4', '2'),
        ('6', '2022-11-22T14:00', 'Scheduled', '', '4', '3'),
        ('7', '2022-12-20T14:00', 'Scheduled', '', '2', '4'),
        ('8', '2023-01-22T10:00', 'Scheduled', '', '2', '5'),
        ('9', '2023-02-22T14:50', 'Scheduled', '', '2', '2'),
        ('10', '2022-11-30T09:00', 'Scheduled', '', '2', '3'),
        ('11', '2022-12-20T14:00', 'To Schedule', '', '5', '5'),
        ('12', '2022-10-20T14:54', 'Canceled', '', '5', '4'),
        ('13', '2022-11-22T14:55', 'Scheduled', '', '5', '3'),
        ('14', '2022-11-30T17:48', 'Scheduled', '', '2', '5'),
        ('15', '2022-11-30T10:00', 'Scheduled', '', '3', '5');
    ''')
    con.commit()
    con.close()



if __name__ == "__main__":
    db_name = './src/test1.db'
    create_tables(db_name)
    populate_tables(db_name)

