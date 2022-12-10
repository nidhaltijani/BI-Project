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

"""def transform_infos(row):
    l=row['INFOS_COMPLEMENTAIRES'].split("#")
    l1=[i for i in l if i..isprintable()]
    row['INFOS_COMPLEMENTAIRES']=l1
    #row['INFOS_COMPLEMENTAIRES']=re.sub(r'[\W_]', '', row['INFOS_COMPLEMENTAIRES'])"""


    
data_transformed=TransformingSource(data_cleaned,transform_tarif)
data_transformed=TransformingSource(data_transformed,transform_classement)
data_transformed=TransformingSource(data_transformed,transform_date)
data_transformed=TransformingSource(data_transformed,transform_semaines)
data_transformed=TransformingSource(data_transformed,get_year)
#data_transformed=TransformingSource(data_transformed,transform_infos)

i=1
for row in data_transformed:
    print(row)
    i+=1
    if i==5:
        break
con=psycopg2.connect(dbname='BI_project',user='postgres',password='admin')   
connection=ConnectionWrapper(con)
connection.setasdefault()
connection.execute("set search_path to dw_schema")

#trouvez une solution pour les chars spéciaux
dim_commune=Dimension(
    name="dim_commune",
    key="COMMUNE_ID",
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


fact_hébergement=FactTable(
    name="fact_hébergement",
    keyrefs=["DATE_ID","COMMUNE_ID","Id"],
    measures=["Tarif_logement","Tarif_SERVICES"]
)

for row in data_transformed:
    i={}
    i["CODE_POSTAL"]=row["CODE_POSTAL"]
    i["RUE"]=row["RUE"]
    i["COMMUNE"]=row["COMMUNE"]
    dim_commune.ensure(i)
    
    i={}
    i["Date_début"]=row["Date_début"]
    i["Date_fin"]=row["Date_fin"]
    i["année"]=row["année"]
    dim_date.ensure(i)
    
    i={}
    i["NOM_OFFRE"]=row["NOM_OFFRE"]
    i["CLASSEMENT"]=row["CLASSEMENT"]
    i["CAPACITE_NBRE_PERS"]=row["CAPACITE_NBRE_PERS"]
    dim_hotel.ensure(i)
    
    #TODO
    #fact table et chars spéciauxx id hotel 

connection.commit()
#print("success")