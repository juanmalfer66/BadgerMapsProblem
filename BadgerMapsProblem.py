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




