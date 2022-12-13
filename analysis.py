import matplotlib.pyplot as plt  
import psycopg2 
import numpy as np
#nb semaines heberges et la charge paye dans une date donnée

con=psycopg2.connect(dbname='BI_project',user='postgres',password='admin')
cur=con.cursor()
cur.execute("set search_path to dw_schema")
# evolution des tarifs par rapport aux années 
cur.execute("SELECT d.année , SUM((f.tarif_services+f.tarif_logement)* f.nombre_semaine_heberge) AS charge \
            from fact_hebergement as f \
            JOIN dim_date as d \
            on f.date_id=d.date_id\
            GROUP BY d.année")


year=[]
total=[]
for record in cur.fetchall():
    year.append(record[0])
    total.append(record[1])
year.reverse()
total.reverse()

plt.bar(x=year,height=total)
plt.title("Evolution du total des tarifs par rapport aux années")
plt.xlabel('Année')
plt.ylabel('Totaux des tarifs')
plt.savefig('fig1.png')
plt.show()

#nbr de semaines hebergees par classement  PIE CHART %
cur.execute("SELECT SUM(nombre_semaine_heberge) from fact_hebergement")
total_semaines=cur.fetchone()
total_semaines=total_semaines[0]
print(total_semaines)
cur.execute("SELECT h.classement, SUM(f.nombre_semaine_heberge) \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id\
    GROUP BY h.classement\
    ORDER BY h.classement")
result=cur.fetchall()
classement=[]
prcntg=[]

for record in result :
    classement.append(record[0]+" "+"étoiles")
    prcntg.append("%.2f" % (record[1]/total_semaines))
print(prcntg)
plt.pie(prcntg,labels=classement,autopct='%1.1f%%',colors=['darkcyan','peachpuff','plum','lightcoral'])
plt.title("Pourcentage de nombre de semaines hébergées par classement d'hôtel")
plt.savefig('fig2.png')
plt.show()

#charge par classement

cur.execute("SELECT  (f.tarif_services+f.tarif_logement)*f.nombre_semaine_heberge AS charge \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id\
    WHERE h.classement='1'")

classement1=[]
for record in cur.fetchall():
    classement1.append(record[0])
#classement1=np.array(classement1)

cur.execute("SELECT  (f.tarif_services+f.tarif_logement)*f.nombre_semaine_heberge AS charge \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id\
    WHERE h.classement='2'")

classement2=[]
for record in cur.fetchall():
    classement2.append(record[0])
#classement2=np.array(classement2)
cur.execute("SELECT  (f.tarif_services+f.tarif_logement)*f.nombre_semaine_heberge AS charge \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id\
    WHERE h.classement='3'")

classement3=[]
for record in cur.fetchall():
    classement3.append(record[0])
#classement3=np.array(classement3)
cur.execute("SELECT  (f.tarif_services+f.tarif_logement)*f.nombre_semaine_heberge AS charge \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id\
    WHERE h.classement='4'")

classement4=[]
for record in cur.fetchall():
    classement4.append(record[0])
#classement4=np.array(classement4)
charge=[classement1,classement2,classement3,classement4]
print(charge)


plt.boxplot(charge,patch_artist=True)
plt.title("La distribution de la charge par rapport au classement")
plt.xlabel("Classement d'hôtel")
plt.ylabel("Charge payée")
plt.savefig('fig3.png')
plt.show()

#nb de semaines par rapp a la capacité scatter plot ..

cur.execute("SELECT f.nombre_semaine_heberge ,h.capacite_nbre_pers ,f.tarif_logement+f.tarif_services \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id\
    ORDER BY h.capacite_nbre_pers")
nb_semaines=[]
cap=[]
size=[]
for record in cur.fetchall():
    nb_semaines.append(record[0])
    cap.append(int(record[1]))
    size.append(float(record[2])*0.2)

plt.scatter(cap,nb_semaines,s=size)
plt.title("Nombre de semaines par rapport à la capacité d'un hôtel")
plt.xlabel("Capacité")
plt.ylabel("Nombre de semaines")

plt.savefig('fig4.png')
plt.show()

#check

cur.execute("SELECT SUM(f.nombre_semaine_heberge),a.commune\
    from fact_hebergement as f\
    JOIN dim_addresse as a\
    on f.address_id=a.address_id \
    GROUP BY a.commune,f.nombre_semaine_heberge\
    ORDER BY SUM(f.nombre_semaine_heberge) DESC")
nbr=[]
com=[]
for record in cur.fetchall():
    print(record)
    nbr.append(record[0])
    com.append(record[1])

plt.barh(com,nbr,color='#98C2E6')
plt.grid()
plt.title("Nombre de semaines hébergées par communes")
plt.xlabel("Nombre de semaines")
plt.ylabel("Commune")
plt.savefig("fig5.png")
plt.show()


"""#capacité vs classement 
cur.execute("SELECT classement,capacite_nbre_pers from dim_hotel ORDER BY classement")
clas=[]
nbre=[]
for record in cur.fetchall():
    clas.append(record[0])
    nbre.append(record[1])
plt.plot(clas,nbre)
plt.show()"""