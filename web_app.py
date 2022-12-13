import streamlit as st

import matplotlib.pyplot as plt  
import psycopg2 
from streamlit_card import card

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

fig,ax=plt.subplots(figsize=(6,3))
ax.bar(x=year,height=total)
plt.title("Evolution du total des tarifs par rapport aux années")
plt.xlabel('Année')
plt.ylabel('Totaux des tarifs')


#nbr de semaines hebergees par classement  PIE CHART %
cur.execute("SELECT SUM(nombre_semaine_heberge) from fact_hebergement")
total_semaines=cur.fetchone()
total_semaines=total_semaines[0]
#print(total_semaines)
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
#print(prcntg)

fig1,ax1=plt.subplots(figsize=(6,3))

ax1.pie(prcntg,labels=classement,autopct='%1.1f%%',colors=['darkcyan','peachpuff','plum','lightcoral'])
plt.title("Pourcentage de nombre de semaines hébergées par classement d'hôtel")


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
#print(charge)



fig2,ax2=plt.subplots(figsize=(6,3))
plt.title("La distribution de la charge par rapport au classement")
plt.xlabel("Classement d'hôtel")
plt.ylabel("Charge payée")
ax2.boxplot(charge,patch_artist=True)



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

fig3,ax3=plt.subplots(figsize=(7,3))

ax3.scatter(cap,nb_semaines,s=size)
plt.title("Nombre de semaines par rapport à la capacité d'un hôtel")
plt.xlabel("Capacité")
plt.ylabel("Nombre de semaines")




#check

cur.execute("SELECT SUM(f.nombre_semaine_heberge),a.commune\
    from fact_hebergement as f\
    JOIN dim_addresse as a\
    on f.address_id=a.address_id \
    GROUP BY a.commune,f.nombre_semaine_heberge\
    ORDER BY SUM(f.nombre_semaine_heberge) DESC\
    limit 30")
nbr=[]
com=[]
for record in cur.fetchall():
    print(record)
    nbr.append(record[0])
    com.append(record[1])
fig4,ax4=plt.subplots(figsize=(7,3))
ax4.barh(com,nbr,color='#98C2E6')
#plt.grid()
plt.title("Nombre de semaines hébergées par communes")
plt.xlabel("Nombre de semaines")
plt.ylabel("Commune")



#capacité vs classement 
cur.execute("SELECT classement,capacite_nbre_pers from dim_hotel ORDER BY classement")
clas=[]
nbre=[]
for record in cur.fetchall():
    clas.append(record[0])
    nbre.append(record[1])
#plt.plot(clas,nbre)


cur.execute("SELECT  (f.tarif_services+f.tarif_logement)*f.nombre_semaine_heberge AS charge \
    from fact_hebergement as f\
    JOIN dim_hotel as h\
    on f.id=h.id")
charge_totale=cur.fetchall()
charge_totale=charge_totale[0][0]

#starting the dashboard
st.set_page_config(
    page_title="Dashboard",
    page_icon="✅",
    layout="wide",
)

st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
#st.title("Tableau de bord d'hébergements touristiques")
st.markdown("<h1 style='text-align: center; color: grey;'>Tableau de bord d'hébergements touristiques</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: grey;
  
}
</style>
"""
, unsafe_allow_html=True)

kpi1, kpi2 = st.columns(2)

kpi1.metric(
    label="Nombre de semaines hébergées",
    value=total_semaines,
    #delta=total_semaines - 10,
)
kpi2.metric(
    label="Charge totale",
    value=charge_totale, 
)


chart1,chart2,chart3=st.columns(3)
with chart1:
    #st.markdown(" ## first chart")
    st.pyplot(fig)
with chart2:
    st.pyplot(fig1)
with chart3:
    st.pyplot(fig2)
chart4,chart5=st.columns(2)
with chart4:
    st.pyplot(fig3)
with chart5:
    st.pyplot(fig4)