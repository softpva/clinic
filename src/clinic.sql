BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "pacientes" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nome"	TEXT NOT NULL,
	"fone"	TEXT NOT NULL,
	"convenio"	TEXT,
	"cartao"	TEXT,
	"sexo"	TEXT,
	"email"	TEXT,
	"data_nasc"	TEXT,
	"endereco"	TEXT,
	"cidade"	TEXT,
	"cep"	TEXT,
	"obs"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "consultas" (
	"id"	INTEGER NOT NULL UNIQUE,
	"data_consulta"	TEXT,
	"status"	TEXT NOT NULL,
	"obs"	TEXT,
	"paciente_id"	INTEGER NOT NULL,
	"medico_id"	INTEGER NOT NULL,
	FOREIGN KEY("medico_id") REFERENCES "medicos"("id"),
	FOREIGN KEY("paciente_id") REFERENCES "pacientes"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "medicos" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nome"	TEXT NOT NULL,
	"fone"	TEXT NOT NULL,
	"especialidade"	TEXT,
	"crm"	TEXT,
	"obs"	TEXT,
	PRIMARY KEY("id")
);

