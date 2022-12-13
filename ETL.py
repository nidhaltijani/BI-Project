from pygrametl.datasources import CSVSource,FilteringSource,TransformingSource
from pygrametl.tables import Dimension,FactTable
from pygrametl import ConnectionWrapper
import psycopg2 

f=CSVSource(open('data.csv', 'r', 16384),delimiter=",")

def filter_blank(row):
    """check for blank values in every column of every row 
    """
    for key in row.keys():
        if row[key]=="":
            return False
    return True


data_cleaned=FilteringSource(f,filter_blank)

def transform_tarif(row):
    l=row['Tarif_logement'].split("|")
    row['Tarif_logement']=int(l[-1])
    
    l=row['Tarif_SERVICES'].split("|")
    row['Tarif_SERVICES']=int(l[-1])

def transform_classement(row):
    l=row['CLASSEMENT'].split(" ")
    row['CLASSEMENT']=l[0]

def transform_date(row):
    l=row["Date"].split("|")
    row["Date_début"]=l[0]
    row["Date_fin"]=l[1]
    del row["Date"]

def get_year(row):
    l=row["Date_début"].split("/")
    row['année']=l[-1]

def transform_semaines(row):
    row["Nombre_Semaine_Heberge"]=int(int(row["Nombre_Semaine_Heberge"])/1200)



def transform_infos(row):
    l=row['INFOS_COMPLEMENTAIRES']
    l=l.split("#")
    for i in range(len(l)):
        if 'Ã¯Â¿Â½' in l[i]:
            l[i]=l[i].replace('Ã¯Â¿Â½', 'e')
        if "Ceble" in l[i]:
            l[i]=l[i].replace("Ceble", 'Cable')
    row['INFOS_COMPLEMENTAIRES']=l
    
def transform_infos2(row):
    l=row['NOM_OFFRE']
    l=l.split(" ")
    for i in range(len(l)):
        if 'Ã¯Â¿Â½' in l[i]:
            l [i]=l[i].replace('Ã¯Â¿Â½', 'e')
     
    row['NOM_OFFRE']=' '.join(l)

def transform_infos3(row):
    l=row['RUE']
    l=l.split(" ")
    for i in range(len(l)):
        if 'Ã¯Â¿Â½' in l[i]:
            l [i]=l[i].replace('Ã¯Â¿Â½', 'e')
    
    row['RUE']=' '.join(l)


    
data_transformed=TransformingSource(data_cleaned,transform_tarif)
data_transformed=TransformingSource(data_transformed,transform_classement)
data_transformed=TransformingSource(data_transformed,transform_date)
data_transformed=TransformingSource(data_transformed,transform_semaines)
data_transformed=TransformingSource(data_transformed,get_year)
data_transformed=TransformingSource(data_transformed,transform_infos)
data_transformed=TransformingSource(data_transformed,transform_infos2)
data_transformed=TransformingSource(data_transformed,transform_infos3)


"""
for row in data_transformed:
    print(row)
    """


con=psycopg2.connect(dbname='BI_project',user='postgres',password='admin')   
connection=ConnectionWrapper(con)
connection.setasdefault()
connection.execute("set search_path to dw_schema")


#trouvez une solution pour les chars spéciaux
dim_addresse=Dimension(
    name="dim_addresse",
    key="ADDRESS_ID",
    attributes=["CODE_POSTAL","RUE","COMMUNE"]
)


dim_date=Dimension(
    name="dim_date",
    key="DATE_ID",
    attributes=["Date_début","Date_fin","année"]
)


dim_hotel=Dimension(
    name="dim_hotel",
    key="Id",
    attributes=["NOM_OFFRE","CLASSEMENT","CAPACITE_NBRE_PERS"]
)


fact_hebergement=FactTable(
    name="fact_hebergement",
    keyrefs=["ADDRESS_ID","DATE_ID","Id"],
    measures=["Tarif_logement","Tarif_SERVICES","Nombre_Semaine_Heberge"]
)



for row in data_transformed:
    
    row['ADDRESS_ID']=row['CODE_POSTAL'][:3]+row['RUE'][:3]+row['COMMUNE'][:3]
    row['ADDRESS_ID'] = dim_addresse.ensure(row)
    
    
    row['DATE_ID']=row['année']
    row['DATE_ID'] = dim_date.ensure(row)
    

    row['Id'] = row['Id']
    row['Id']=dim_hotel.ensure(row)


    fact_hebergement.ensure(row)

    
    

connection.commit()
print("success")
