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


csv_file = 'sample test file - sheet1.csv'
csv_list = csv_to_list(csv_file)

# Se obtienen los campos de la cabecera
header = get_header(csv_list)

# Se quita la cabecera de la lista csv
csv_list.remove(csv_list[0])

names = get_full_names(csv_list,header)

# Se eliminan las tiles para poder ordenarlo alfabeticamente

sorted_names = sorted(names, key = sinAcentos)  


