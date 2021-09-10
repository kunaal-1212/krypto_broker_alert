import requests
import smtplib
from email.message import EmailMessage
import keys
import pandas as pd
from time import sleep

def email_alert(subject,body,to):
    msg=EmailMessage()
    msg.set_content(body)
    
    msg['subject']=subject
    msg['to']=to
    
    user="kunaalcool12269@gmail.com"
    msg['from']=user
    password="ysevjedqwrquehlj"
    
    server=smtplib.SMTP("smpt.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()
    
    if __name__=='__main__':
        
        
    
       
def get_crypto_rates(base_currency='EUR',assets='BTC'):
    url = 'https://api.nomics.com/v1/currencies/ticker'
    
    payload={'key':keys.NOMICS_API_KEY,'convert':base_currency,'ids':assets,'interval':'1d'}
    response = requests.get(url,params=payload)
    data=response.json()
    
    crypto_currency,crypto_price,crypto_timestamp=[],[],[]
    
    for asset in data:
        crypto_currency.append(asset['currency'])
        crypto_price.append(asset['price'])
        crypto_timestamp.append(asset['price_timestamp'])
        
    raw_data={
        'asset' : crypto_currency,
        'rates' : crypto_price,
        'timestamp':crypto_timestamp
        }
    
    df=pd.DataFrame(raw_data)
    return df


def set_alert(dataframe,asset,alert_high_price):
    crypto_value=float(dataframe[dataframe['asset']==asset]['rates'].item())
    
    details=f'{asset}:{crypto_value}, Target:{alert_high_price}'
    
    if crypto_value>=alert_high_price:
        print(details + '<<TARGET VALUE REACHED!!')
        email_alert("target status","target reached","kushaalbok122@gmail.com")

    else:
        print(details)
        
        
#alert While loop
loop=0
while True:
    print(f'-------------------------------({loop})----------------------')

    try:
        df=get_crypto_rates()
        
        set_alert(df,'BTC',33000)
    except Exception as e:
        print('Couldn\'t retrieve the data...trying again.')
        
    loop+=1
    sleep(30)
        
    
    
    
