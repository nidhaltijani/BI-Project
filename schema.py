import psycopg2 

con=psycopg2.connect(dbname='BI_project',user='postgres',password='admin')
cur=con.cursor()

cur.execute('CREATE SCHEMA dw_schema_test')
cur.execute("set search_path to dw_schema_test")

cur.execute('CREATE TABLE dim_addresse (ADDRESS_ID VARCHAR(50) ,CODE_POSTAL VARCHAR(50),RUE VARCHAR(50),COMMUNE VARCHAR(50))')
cur.execute('ALTER TABLE dim_addresse ADD CONSTRAINT pk_com PRIMARY KEY (ADDRESS_ID)')
cur.execute('CREATE TABLE dim_date (DATE_ID VARCHAR(50) ,Date_début VARCHAR(50),Date_fin VARCHAR(50),année VARCHAR(4))')
cur.execute('ALTER TABLE dim_date ADD CONSTRAINT pk_date PRIMARY KEY (DATE_ID)')
cur.execute('CREATE TABLE dim_hotel (Id VARCHAR(50),NOM_OFFRE VARCHAR(150),CLASSEMENT VARCHAR(1),CAPACITE_NBRE_PERS VARCHAR(10))')
cur.execute('ALTER TABLE dim_hotel ADD CONSTRAINT pk_hotel PRIMARY KEY (Id)')
cur.execute('CREATE TABLE fact_hebergement (ADDRESS_ID VARCHAR(50),DATE_ID VARCHAR(50),Id VARCHAR(50),Tarif_logement int,Tarif_SERVICES int,Nombre_Semaine_Heberge int)')
cur.execute('ALTER TABLE fact_hebergement ADD CONSTRAINT fk_com FOREIGN KEY (ADDRESS_ID) REFERENCES dim_addresse(ADDRESS_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_hebergement ADD CONSTRAINT fk_date FOREIGN KEY (DATE_ID) REFERENCES dim_date(DATE_ID) ON DELETE CASCADE')
cur.execute('ALTER TABLE fact_hebergement ADD CONSTRAINT fk_hotel FOREIGN KEY (Id) REFERENCES dim_hotel(Id) ON DELETE CASCADE')

con.commit()
#print("succes")