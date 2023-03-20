import time

while True:

    # logging into email id using imap library

    import imaplib
    import email

    imap_server = "imap.gmail.com"
    email00 = 'sg6239@srmist.edu.in'
    passward = "qsuosnaujrftwhsv"

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email00, passward)

    # getting the unseen mail with subject Weather00

    imap.select("Inbox")

    Client_details = []  # if multiple mails exist

    waste, msgnums = imap.search(None, 'Subject "Weather00"', "UNSEEN")

    for msgnum in msgnums[0].split():
        waste, data = imap.fetch(msgnum, "(RFC822)")

        message = email.message_from_bytes(data[0][1])
        print(f"Message Number: {msgnum}")
        print(f"From: {message.get('From')}")
        print(f"Date: {message.get('Date')}")
        print(f"Subject: {message.get('Subject')}")
        print("\n")

        temp1 = message.get("From")
        m_id = None

        for i in range(len(temp1)):
            if temp1[i] == "<":
                m_id = temp1[i + 1: -1]
                break

        if m_id == None:
            m_id = temp1

        Client_mail = m_id
        temp = message.get("Subject")
        sub, location = temp.split()

        Client_details.append([Client_mail, location])

    print(Client_details)

    # SCRAPING THE WEATHER DATA

    from requests_html import HTMLSession

    weather = []
    for nums in Client_details:
        # taking input from user
        city = nums[1]

        # creating url
        url = f"https://www.google.com/search?q={city}+weather"

        # user agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

        s = HTMLSession()
        r = s.get(url, headers=headers)

        # fiding temperature
        temp = r.html.find('span#wob_ttm', first=True).text + "°C"

        # finding sky description
        sky_Description = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text

        # finding date and time
        Date_tim = r.html.find('div.wob_dts', first=True).find('#wob_dts', first=True).text

        # Scraping rain, humidity and wind
        rain = r.html.find('div.wtsRwe', first=True).find('span#wob_pp', first=True).text
        humidity = r.html.find('div.wtsRwe', first=True).find('span#wob_hm', first=True).text
        wind = r.html.find('div.wtsRwe', first=True).find('span#wob_ws', first=True).text

        wet = f'''
      Hi there!
      This is your city's weather

      Time                   :-   {Date_tim}
      Temperature       :-   {temp}
      Sky Description  :-   {sky_Description} 
      Precipitation       :-   {rain}
      Humidity             :-   {humidity}
      Wind Speed       :-   {wind}

      Have a nice day ahead   :-)'''

        weather.append(wet)

    # SENDING MAILS AS WEATHER REPORT

    import smtplib
    from email.message import EmailMessage
    import ssl  # to add layer of security

    email_sender = 'sg6239@srmist.edu.in'
    email_passward = "qsuosnaujrftwhsv"

    for i in range(len(Client_details)):
        email_receiver = Client_details[i][0]

        subject = f"{Client_details[i][1]}'s Weather Deails"
        body = f"{weather[i]}"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_passward)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        print(email_receiver, subject)

    time.sleep(5)