import smtplib
import random
import datetime as dt

my_email = "piotrek.szewczul19@gmail.com"
quote_for_the_day = ""
with open("quotes.txt") as file:
    data = file.readlines()
    quote_for_the_day = random.choice(data)

if dt.datetime.now().weekday() == 4:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        message = "Subject:Hello\n\n"+quote_for_the_day
        connection.starttls()
        connection.login(user=my_email, password = "ongacdjnydeqznxe")
        connection.sendmail(from_addr=my_email,to_addrs="mateusz.szuflicki@ttas.pl",msg = "Subject:Hello\n\n"+quote_for_the_day)
        connection.close()
