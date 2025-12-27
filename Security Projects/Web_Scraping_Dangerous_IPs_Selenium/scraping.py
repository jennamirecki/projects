from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import pandas as pd
import csv
import streamlit as st
import folium
import country_converter as coco
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize, to_hex
from folium.plugins import HeatMap

#Use abuseipdb API to get 150 recent suspicious IP addresses
url_abuse= "https://api.abuseipdb.com/api/v2/blacklist"
key_abuse = "3a12d1a12b6d6b94c479ba2a995b4bf3bd3b9f303752f6f9f307acb9641bef58b30e6717f7470024"
headers_abuse = {
    
    "Accept":"application/json",
    "Key": key_abuse
}
response_abuse = requests.get(url_abuse, headers=headers_abuse)
response_abuse.raise_for_status()
data_abuse = response_abuse.json()['data']
with open('my_ips.json','r') as f:
    data=json.load(f)
    for i in data:
        list_ip.append(i['ipAddress'])
        last_reported.append(i['lastReportedAt'])     
with open("my_ips.json","r") as f:
        writer = csv.writer(data_abuse,f)

#Use Selenium to scrape ipinfo.io website to get hostname, company name, and score
url_info = "https://ipinfo.io/"
df["IP Address"] = list_ip[:150]
df=df.set_axis(range(1,len(df)+1))
ASNS_List = []
Hostname_list =[]
Company_list = []
Abuse_Score = []
driver=webdriver.Chrome()
driver.implicitly_wait(10)
df=pd.DataFrame()
list_ip = []
last_reported = []
for x in list_ip[:150]:
    try:
            driver.get(f"{url_info}{x}")
            table=driver.find_element(By.TAG_NAME, "table")   
            ASN = table.find_element(By.XPATH, ".//tbody/tr[1]/td[2]").text
            hostname = table.find_element(By.XPATH, ".//tbody/tr[2]/td[2]").text
            Company = table.find_element(By.XPATH, ".//tbody/tr[4]/td[2]").text
            ASNS_List.append(ASN[:6])
            Hostname_list.append(hostname)
            Company_list.append(Company)
            Abuse_Score.append(abuseConfidenceScore)
    except:
            ASNS_List.append("None")
            Hostname_list.append("None")
            Company_list.append("None")
            Abuse_Score.append("None")

df["ASN"] = ASNS_List
df["Hostname"] = Hostname_list
df["Company Name"] = Company_list
df["Last Reported Date"] = last_reported[:150]
df["Abuse IPDB Score"] =Abuse_Score[:150]
#Write the info to df1 CSV file
df.to_csv("df1.csv")
driver.quit()
                
#Create dataframe from df1 CSV file that contains 150 IPs
df=pd.read_csv("df1.csv")
df=df.drop("Unnamed: 0",axis=1)

df["Last Reported Date"]= pd.to_datetime(df["Last Reported Date"]).dt.date

#Use Country Converter to convert country code in iso2 to iso3
cc=coco.CountryConverter()
df["id"] = cc.pandas_convert(df["Country Code"],to="ISO3")
pd.set_option("display.max_columns",20, "display.max_rows",400,"display.width",1500)

with open("df1.csv","r") as f:
    reader=csv.reader(f)
    cols = [col for col in next(reader) if not col ==""]

#Create column that counts IPs by country and append to table
country_count = df.groupby("id")["IP Address"].count().reset_index(name="Count")
df["Country Count"] = df.groupby("id")["IP Address"].transform("count")

#Find max and min country count for heatmap
vmax=df['Country Count'].max()
vmin=df["Country Count"].min()
norm=Normalize(vmin=vmin, vmax=vmax)

#Create folium heatmap
cmap=cm.get_cmap("Spectral")
heat_data = df[["Latitude","Longitude","Country Count"]].values.tolist()
map_center = [df["Latitude"].mean(),df["Longitude"].mean()]
m2=folium.Map(location=map_center,zoom_start=2)
HeatMap(heat_data,
        radius=6,
        blur=2,
        max_val=float(df['Country Count'].max()),
).add_to(m2)

#Make the rows in IP table match the spectral colormap and add markers for heat map overlay
for index, row in df.iterrows():
    one = to_hex(cmap(norm(row["Country Count"])))
    star_icon= folium.DivIcon(html=f"<span class='fa fa-star' style='color:{one}; font-size:12px;'></span>")
    tooltip_text= f"IP Address:{row['IP Address']} City:{row['City']}, Country:{row['Country']}"   
     
#Create heatmap with marker overlay
    folium.Marker(
        location = [row["Latitude"],row["Longitude"]],
        tooltip=tooltip_text,
        icon=star_icon,
        popup=f"Click here for {row['IP Address']} details"
               
).add_to(m2)

#Use Pandas styler to style the IP table but it doesn't show because of Streamlit    
styler=df.style
header_styles = [{
    
    'selector':'th',
    'props':[
        ('font-family','Tahoma, sans-serif'),
        ('font-size','8pt'),
        ('font-weight','bold'),
        ('color','black')
    ]
}
]
styler=styler.background_gradient(cmap="Spectral", subset=["Country Count"],vmin=vmin,vmax=vmax,axis=1)
style=styler.apply(lambda x: [f"background-color: {to_hex(cmap(norm(x['Country Count'])))}"]*len(x),
axis=1)
styler.set_properties(**{'color':'white','font-weight':'bold'})
styler=styler.set_table_styles(header_styles)

#Write title for IP table on Streamlit application
st.write('<h2 style="text-align: center; font-size:32px;color:royalblue; text-decoration: underline">150 Most Recent Dangerous IP Addresses</h2>',unsafe_allow_html=True)
m= folium.Map(location=[20,0],zoom_start=1.2,tiles="cartodbpositron")
geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
folium.Choropleth(
    geo_data = geo_url,
    name = "Choropleth",
    data= country_count,
    columns = ["id","Count"],
    key_on="feature.id",
    fill_color = "Spectral",
    fill_opacity=0.8,
    line_opacity=0.3,
    nan_fill_color="#f0f0f0",
    legend_name = "Number of Dangerous IP Addresses"
    
).add_to(m)

#Write IP table to Streamlit application
st.dataframe(styler, width=2000, height = 500)

#Create Summary Stats tables
common_ASN = df["ASN"].mode()[0]
ASN_value = df["ASN"].value_counts()[common_ASN]
common_ISP = df["ISP"].mode()[0]
ISP_value = df["ISP"].value_counts()[common_ISP]
common_country = df["Country"].mode()[0]
Country_value = df["Country"].value_counts()[common_country]
sum_stats = {
    "Category":["ASN","ISP","Country"],
    "Most Frequent Value":[{common_ASN},{common_ISP},{common_country}],
    "Occurrences":[{ASN_value},{ISP_value},{Country_value}]
}
r=pd.DataFrame(sum_stats)
r=r.reset_index(drop=True)
st.write('<h2 style="text-align: center; font-size:32px;color:royalblue; text-decoration: underline">Statistics</h2>',unsafe_allow_html=True)
st.dataframe(r,hide_index=True, width=2000)

#Make the h2 heatmaps take up half of width of page on Streamlit application 
col1,col2 = st.columns(2)
with col1:
    st.markdown('<h2 style="text-align: center; font-size:32px; color:royalblue; text-decoration: underline">Heat Map of Dangerous IP Addresses</h2>',unsafe_allow_html=True)
    st.components.v1.html(m._repr_html_(), height=800)
with col2:
    st.markdown('<h2 style="text-align: center; font-size:32px; color:royalblue;text-decoration: underline">Dangerous IP Addresses by City</h2>',unsafe_allow_html=True)
    st.components.v1.html(m2._repr_html_(), height=800)
