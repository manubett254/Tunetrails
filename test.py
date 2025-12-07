import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'ghtzojczwuuhjgcu')
    print("SMTP connection successful!")
    server.quit()
except Exception as e:
    print("Failed:", e)
