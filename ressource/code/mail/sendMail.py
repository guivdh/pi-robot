import smtplib
import imaplib
import email
import sys
import configparser

EMAIL_ADDRESS = "noreply.simbot@gmail.com"
EMAIL_PASSWORD = "79nXLir62M"

cfg = configparser.ConfigParser()
cfg.read('config/config.cfg')

body = sys.argv[2]
dest = sys.argv[1]


if dest == 'Signaler un problème':
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        subject='Signalement de problème'
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = 'Subject : ' + subject + ' \n\n' + body

        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.encode("utf8"))
        print("Email envoyé !")
else:
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:

        nom = cfg.get('user', 'nom')
        subject = 'Mail de ' + nom
        EMAIL_DEST = cfg.get('mail', dest)

        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = 'Subject : ' + subject + ' \n\n' + body

        smtp.sendmail(EMAIL_ADDRESS, EMAIL_DEST, msg.encode("utf-8"))
        print(EMAIL_DEST)
        print(msg)
        print("Email envoyé !")
