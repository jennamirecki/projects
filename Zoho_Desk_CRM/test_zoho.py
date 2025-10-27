import requests,json
client_ID="1000.R92E6LX9OPCNPH9OJ65ZFTDT8IN7SH"
ORG_ID="898147004"
secret='cf701db4e7a142c29f1eb895cbe2f1e3a5c80f6134'
auth_code="1000.b6d2943566667d2578b55a050c4442f7.7d86f89437d5ad01f69578fe1fd53027"
URL= 'https://desk.zoho.com'
token_url='https://accounts.zoho.com/oauth/v2/token'
"""
#use authorization code to generate refresh token
temp_params={
    'grant_type':'authorization_code',
    'client_id':client_ID,
    'client_secret':secret,
    'code':auth_code  
    }

temp_response=requests.post(token_url,params=temp_params)
temp_data=temp_response.json()
refresh_token=temp_data.get('refresh_token')
print(refresh_token)
"""
refresh_token_real="1000.b1f91dce41fdb5f78aa9ee61bd9c3a54.38852603cb76b2f9b9f3087feaf6f49b"
#access_token=temp_data.get('access_token')

#use refresh token to generate new access token
token_params={
    'grant_type':'refresh_token',
    'refresh_token':refresh_token_real,
    'client_id':client_ID,
    'client_secret':secret
    }

token_response=requests.post(token_url, params=token_params)
token_data=token_response.json()
access_token=token_data.get('access_token')
#add ticket to Zoho Desk
dept_ID="1182821000000006907"
ticket_url='https://desk.zoho.com/api/v1/tickets'
ticket_data={
    'subject':"Network Outage",
    'departmentId':dept_ID,
    'contactId':'1182821000000475001',
    'description':'Network outage in Main Data Center',
    'priority':"High",
    'status':"Open",
    'channel':'phone'
}
headers1={
    'Authorization':f'Zoho-oauthtoken {access_token}',
    'orgId':ORG_ID,
    'Content-Type':'application/json' 
}
response_send_ticket=requests.post(ticket_url, json=ticket_data,headers=headers1)

#retrieve tickets from Zoho Desk
ticket_url=f'{URL}/api/v1/tickets?limit=10'
headers={
    'Authorization':f'Zoho-oauthtoken {access_token}',
    'orgId':ORG_ID
        
}
tickets_response=requests.get(ticket_url, headers=headers)
ticket_data=tickets_response.json()
tickets=ticket_data.get('data')
print(f"{'#'*10} Rita's Realty Tickets {'#'*10}")
n1=len(tickets)
num1=1
while num1 <=n1:
    for x in tickets:
        print(f"Ticket {num1}. ID:{x.get('id')} Subject: {x.get('subject')}")
        num1+=1

contacts_url=f'{URL}/api/v1/contacts?limit=10'
headers={
    'Authorization':f'Zoho-oauthtoken {access_token}',
    'orgId':ORG_ID
      }
contacts_response=requests.get(contacts_url, headers=headers)
contacts_data=contacts_response.json()
contacts=contacts_data.get('data')
print(f"{'#'*10} Rita's Realty Contacts {'#'*10}")
n=len(contacts)
num=1
while num <=n:
    for x in contacts:
        print(f"Contact {num}. ID:{x.get('id')} Name: {x.get('firstName')+" "+x.get('lastName')}")
        num+=1
