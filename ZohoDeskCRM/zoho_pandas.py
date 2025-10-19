import pandas
#Contacts
df1=pandas.read_csv(r"C:\Users\jenna\Documents\Contacts__1.csv")
cols=(df1.columns).tolist()
print(f"The properties of Contacts are: {", ".join(cols)}")
print(f"There are {len(cols)} Contacts at Rita's Realty")

df2=pandas.read_csv(r"C:\Users\jenna\Documents\Cases__1.csv")
#Tickets
print(f"There are {len(df2)} tickets total for the IT support Department at Rita's Realty: {len(df2[df2["Status"]=="Open"])} open, {len(df2[df2["Status"]=="Closed"])} closed, {len(df2[df2["Status"]=="Escalated"])} escalated, and {len(df2[df2["Status"]=="On Hold"])} on hold")
most_common_classification=df2["Classifications"].mode()[0]
print(f'The most common classification of ticket is "{most_common_classification}"')