import csv


# Transforma un fichero csv en una lista
def csv_to_list(file_name):
    csv_list = []
    with open('sample test file - sheet1.csv', newline='\n',encoding='utf-8') as file_name: 
        reader = csv.reader(file_name,delimiter=",")
        for i in reader:
            csv_list.append(i)  
    return csv_list

# Obtiene la cabecera de una lista
def get_header(csv_list):
    aux = list(range(0,len(csv_list[0])))
    header = dict(zip(csv_list[0],aux))
    return header

# A partir de un string con tildes, devuelve el mismo sin tildes
def sinAcentos(word):
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    word_wto_accent = unicodedata.normalize('NFKC', 
                         unicodedata.normalize('NFKD', word).translate(trans_tab))  
    return(word_wto_accent)

# Obtiene la una lista con todos los nombres
def get_full_names(csv_list,header):
    names = list()
    for i in range(len(csv_list)):
        if (csv_list[i][header['First Name']] == '') and (csv_list[i][header['Last Name']] == ''):
            names.append('')
        else:
            names.append(csv_list[i][header['First Name']] + " " + 
                         csv_list[i][header['Last Name']])
    return names

# Devuelve una lista de datos a partir de unos parametros de entrada requeridos
def get_Required_Data(csv_list,header,required_fields):
    required_data = list()
    for i in range(len(csv_list)):
        aux = list()
        for field in required_fields:
            aux.append(csv_list[i][header[field]])
        required_data.append(aux)
    return required_data

# Salta una excepción al encontrar un campo vacío
def empty_field(used_list,position):
    # Si divide entre 0, salta la excepción al estar el campo vacio
    try:
        1/len(used_list[position])
    except:
        print("NOT KNOWN") 



csv_file = 'sample test file - sheet1.csv'
csv_list = csv_to_list(csv_file)

# Se obtienen los campos de la cabecera
header = get_header(csv_list)

# Se quita la cabecera de la lista csv
csv_list.remove(csv_list[0])

names = get_full_names(csv_list,header)

# Se eliminan las tiles para poder ordenarlo alfabeticamente

sorted_names = sorted(names, key = sinAcentos)  


# Los datos requeridos son los siguientes
required_fields = ['First Name', 'Last Name', 'Street', 'Zip', 'City', 
                   'Last Check-In Date', 'Company']

# Se obtienen los datos relevantes del usuario
costumer_data = get_Required_Data(csv_list,header,required_fields)

# Obtener check-in date más antiguo

date_list = list()
for i in range(len(csv_list)):
    if csv_list[i][header['Last Check-In Date']] == '' :
        date_list.append('')
    else:
        date_list.append(datetime.strptime(
            csv_list[i][header['Last Check-In Date']],"%d/%m/%Y").timestamp())


print("\nLISTA DE LOS CLIENTES ORDENADOS ALFABÉTICAMENTE: \n")

for i in range(len(names)):
    if len(names[i]) == 0:
        # Llama a la excepción
        empty_field(names,i)
    else:
        print(names[i])

# Crear un registro logging para registrar las excepciones de filas vacías

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logfile_exceptions.log",
                    filemode = "w",
                    format = Log_Format)
logger = logging.getLogger()

        
# Se imprimen los datos solicitados

        
print("\nLISTA DE LOS CLIENTES:")

# Con aux_first y aux_last se obtiene el cliente que corresponde a los valores temporales
last_check = datetime.strptime(csv_list[0][header['Last Check-In Date']],"%d/%m/%Y").timestamp()
aux_last = 0
first_check = datetime.strptime(csv_list[0][header['Last Check-In Date']],"%d/%m/%Y").timestamp()
aux_first = 0

for i in range(len(costumer_data)):
    print("\nCliente " + str(i+1) + "\n")
    # Excepción si una fila contiene menos campos de los esperados del csv completo
    if len(header) > len(csv_list[i]):
        try: 1/0
        except:
            print("No se poseen todos los datos de este cliente")
     
    # Comparar marca temporal con el cliente anterior y actualizar si es necesario
    if csv_list[i][header['Last Check-In Date']] != '':
        if last_check < datetime.strptime(csv_list[i][header['Last Check-In Date']],"%d/%m/%Y").timestamp():
            last_check = datetime.strptime(csv_list[i][header['Last Check-In Date']],"%d/%m/%Y").timestamp()
            aux_last = i
        if first_check > datetime.strptime(csv_list[i][header['Last Check-In Date']],"%d/%m/%Y").timestamp():
            first_check = datetime.strptime(csv_list[i][header['Last Check-In Date']],"%d/%m/%Y").timestamp()
            aux_first = i
    
    aux_sum = 0    
    for j in range(len(costumer_data[i])):
        if len(costumer_data[i][j]) == 0:
            # Excepción si un field está vacío
            print(required_fields[j] + ": ", end="")
            empty_field(costumer_data[i],j)
        else:   
            print(required_fields[j] + ": " + costumer_data[i][j])
        
        # Salta una excepción cuando el numero de campos del csv es menor de lo requerido
        aux_sum = aux_sum + len(costumer_data[i][j])
        if aux_sum == 0 and j == len(required_fields)-1:
            logging.exception("All fields are empties in this row")


print("\nEl cliente que ingresó por última vez fue " + names[aux_last])
print("\nEl cliente que ingresó por primera vez fue " + names[aux_first] + "\n")




