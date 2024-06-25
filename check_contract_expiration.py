import pandas as pd
from datetime import datetime
import time
import schedule
from smtp import send_reminder_email
from app_utilities import save_file_df, FILE_MAP, FIELD_ID_MAP
from app_utilities import get_file_df
from email.mime.text import MIMEText

def check_contract_expiry():

    df = get_file_df('contracts_log')
    today = datetime.today()
    print('ttttttttttttt',today)
    for index, row in df.iterrows():
        print('in contracttttttttttttttttt')
        expiration_date = pd.to_datetime(row['Expiration date'])
        print('eeeeeeeeeeeee',expiration_date)
        days_to_expire = (expiration_date - today).days
        print('dYSSSSSSSSSSSSSSSSS',days_to_expire)
        contract = row["Contract Number"]
        desc = row["Description"]
        receiver = row['Approver'].split()
        receiver_email ='.'.join(receiver)+'@brookfield.com'
        #receiver_email = receiver_email.lower()
        print(receiver_email)
        #receiver_email ='neelam.gautam@brookfield.com'
        if days_to_expire in [60, 30, 7]:
            print('TRUEEEEEEEEEEEEEEEEE')
            subject = f' Gentle Reminder : {contract} - {desc} expires in {days_to_expire} days'
            body = f'{contract} - {desc} expires in {days_to_expire} days. Please approve it ASAP'
            print('sendingggggggggggggggggggggggggggggggggggg')
            send_reminder_email(receiver_email,body,subject)

schedule.every().day.at("14:56").do(check_contract_expiry)

def run_schedular():
    while True:
        print('in schedular-------------------------------------')
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    check_contract_expiry()