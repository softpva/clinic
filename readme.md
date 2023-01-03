# **A Simple CRUD Clinic Application in Python**
[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](./README.pt-br.md)
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](./README.es.md)
 
# About
> This simple crud App was written in python 3 (tkinter/tkk) and SQLite, it can register patients, doctors and appointments.  
>
> [![NPM](https://img.shields.io/npm/l/react)](./LICENSE) 

# Features:
> - CRUD (Create,Read,Update,Delete) patients.
> - CRUD doctors.
> - CRUD appointments.
> - Access in English or Portuguese.
> - Use any name to databases, eg: 2023_database
> - Export to excel
> - Search automatically zip code from Brazil and USA.


# Layouts
> ## The main page - Patients Register (in English)
> ![Main Page Image](src/images/main_page.gif)  

> ## The main page - Patients Register (in Portuguese)
> ![Imagem da tela principal](src/images/tela_principal.gif)  

> ## After the doctor button is clicked on main page
> ![Doctors register page](src/images/doctor_page.gif)  

> ## After the Appointments button is clicked on main page
> ![Doctors register page](src/images/appoint_page.gif)  

> ## Save to excel
> And, at the end, if you click on the Save Excel button at the main page, an excel file xlsx will be generated with three tabs
> ### Excel patient registers
> ![patients's sheet](src/images/patients_xlsx.gif)
> ### Excel medical appointments
> ![appointments's sheet](src/images/appointments_xlsx.gif) 
> ### Excel doctor registers
> ![doctors's sheet](src/images/doctors_xlsx.gif)

# Models
> ## Database model
> ![Doctors register page](src/images/model.gif) 

# Tecnologies
> - Python 3
> - Tkinter/tkk
> - SQLite database
> - Pandas
> - No external libraries, own classes for:
>     - SQL commands.
>     - ISO8601.py to date/time manipulation.
>     - Internationalization.

# Kick off
> - The app can be called at command line using the syntax:  
>
>           python main.py 'language'  'database'   
>
> - Where:  
> - 'language' can be: 'en' or 'pt' (if omitted 'pt' it'll be default)  
>    The language option will set several conditions, for example the search of zip code or cep in US or Brazil, respectively, and  the local date configurations.
> - 'database' is the name of SQLite database to be read or to be created. (if omitted 'clinic.db' it'll be used)


# Pro version
> - Personalized for a specific clinic.
> - Login and security features.
> - Specific idiom.
> - Multi users.
> - For web and mobile user.
> - Notifications and reports.
> - Backup and log resources.

# Author
> Pedro Vitor Abreu
>
> <soft.pva@gmail.com>
>
> <https://github.com/softpva>






















