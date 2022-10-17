from email.message import EmailMessage
import smtplib
import os
import ssl


SENDER_MAIL = "berichtsheftautomated@gmail.com"


def create_mail(content, bytes, mails):
    msg = EmailMessage()
    msg['Subject'] = f'Berichtsheft KW {content["date"]} Nr {content["berichtNummer"]}'
    msg['From'] = SENDER_MAIL
    msg["To"] = ", ".join(mails)

    message_body = [
        "Hi mein Liebster,"
        " ",
        "Hier dein Berichtsheft",
        "Falls mit der Word Datei etwas fucked ist, hier nochmal der Content:"
        " ",
        "Betriebliche Todo's:",
        content["todos"],
        " ",
        "Wochenbericht:",
        content["weekly_theme"],
        " ",
        "Schulschmutz",
        content["school"],
        " ",
        "Have an wonderful Day",
        "And Kuss auf die Nuss"
    ]

    msg.set_content("\n".join(message_body))

    file_name = "Berichtsheft_{}_KW_{}.docx".format(
        content["berichtNummer"], content["date"])

    msg.add_attachment(bytes, maintype="application",
                       subtype="vnd.openxmlformats-officedocument.wordprocessingml.document", filename=file_name)

    return msg


def send_mail(content, bytes):
    mails = [mail.strip() for mail in content["mails"]]

    mail = create_mail(content, bytes, mails)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls(context=context)
            smtpObj.login(SENDER_MAIL, os.getenv("EMAIL_PW", ""))
            smtpObj.sendmail(SENDER_MAIL, mails,
                             mail.as_string())  # type: ignore
    except Exception as e:
        print(e)
