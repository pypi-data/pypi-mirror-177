
Mail library that abstract away complexity of setting up mail server

"""
      NOTE:
          in all `BaseMail` mathod there is a keyword argument called `port`, that port is the port of your SMTP server which will listen, make sure to put the port that is convenient to your SMTP server e.g for gmail is 465
          
          
      To tests your mail locally, boot up the python mail server on a different terminal by:
      $:/~    `python3 -m smtpd -c DebuggingServer -n localhost:7000`
          
      and then open another terminal and run your python script including the below code in it:
      >>>    from kyaah import BaseMail

      >>>    subj = f"Hellow world!"
      >>>    body = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum voluptate ipsum voluptatum doloribus, incidunt totam doloremque."


      >>>    base = BaseMail(
      ...      from_usr = "myself@mail.com",
      ...      mail_passwd = "myP@$$w)rD",
      ...      to_usr = ["userOne@mail.com", "userTwo@mail.com"],
      ...      subject = subj,
      ...      body = body,
      ...      server = "<your_mail_server>",
      ...      )
      >>>    base.local_mail()
      ------------------------------------------------------------------------------------------------------
      To send a text mail to someone:
          
      >>>    from kyaah import BaseMail

      >>>    subj = f"Hellow world!"
      >>>    body = "Lorem ipsum dolor sit amet consectetur adipisicing elit, rerum voluptate ipsum volupt."


      >>>    base = BaseMail(
      ...      from_usr = "myself@mail.com",
      ...      mail_passwd = "myP@$$w)rD",
      ...      to_usr = ["userOne@mail.com", "userTwo@mail.com"],
      ...      subject = subj,
      ...      body = body,
      ...      server = "<your_mail_server>",
      ...      )
      >>>    base.send_mail(port=465)
      ------------------------------------------------------------------------------------------------------
      To send a text mail together with an image:
      >>>    from kyaah import BaseMail

      >>>    subj = f"Hellow world!"
      >>>    body = "Lorem ipsum dolor sit amet consectetur adipisicing elit, rerum voluptate ipsum volupt."


      >>>    base = BaseMail(
      ...      from_usr = "myself@mail.com",
      ...      mail_passwd = "myP@$$w)rD",
      ...      to_usr = ["userOne@mail.com", "userTwo@mail.com"],
      ...      subject = subj,
      ...      body = body,
      ...      server = "<your_mail_server>",
      ...      )
      >>>    base.mail_with_image('image_1.jpg', port=465)
          
      If you want to send more than one image, pass a list of the images as argument into the `mail_with_image` method like:
      >>>    base.mail_with_image(['image_1.png', 'image_2.jpg'], port=465)
      ------------------------------------------------------------------------------------------------------
      To send mail together with files, pass a list of the files you want to send as an argument in the `mail_with_file` method like:
      >>>    from kyaah import BaseMail

      >>>    subj = f"Hellow world!"
      >>>    body = "Lorem ipsum dolor sit amet consectetur adipisicing elit, rerum voluptate ipsum volupt."


      >>>    base = BaseMail(
      ...      from_usr = "myself@mail.com",
      ...      mail_passwd = "myP@$$w)rD",
      ...      to_usr = ["userOne@mail.com", "userTwo@mail.com"],
      ...      subject = subj,
      ...      body = body,
      ...      server = "<your_mail_server>",
      ...      )

      >>>    base.mail_with_file(['file_1.pdf', 'file_2.docx'], port=465)
      ------------------------------------------------------------------------------------------------------
      To send mail together with html page call the `mail_with_page` method and pass a keyword args `file` with a value of the absolute location of your html file in the `mail_with_page` method, like:
      
      >>>    from kyaah import BaseMail

      >>>    subj = f"Hellow world!"
      >>>    body = "Lorem ipsum dolor sit amet consectetur adipisicing elit, rerum voluptate ipsum volupt."


      >>>    base = BaseMail(
      ...      from_usr = "myself@mail.com",
      ...      mail_passwd = "myP@$$w)rD",
      ...      to_usr = ["userOne@mail.com", "userTwo@mail.com"],
      ...      subject = subj,
      ...      body = body,
      ...      server = "<your_mail_server>",
      ...      )

      >>>    base.mail_with_page(file='index.html', port=465)
      
      If you want to test we provide you with a test feature which in short is to the keyword args of `file='default'` like:
      
      >>>    base.mail_with_page(file='default', port=465)
      ------------------------------------------------------------------------------------------------------
      
      # SECURITY
      
      FOR SECURITY REASON
      we provide you a class called `Vault`. This class will look your email address and password/app_password in your sysytem environment variable. And you don't need to change anything in your code, all the mothods is thesame. Look more for this class in your interpreter by calling the  '''help(Vault)'''  Use this class in production instead of the  '''BaseMail'''  class. example:
      
      >>>    from kyaah import Vault

      >>>    subj = f"Hellow world!"
      >>>    body = "Lorem ipsum dolor sit amet consectetur adipisicing elit, rerum voluptate ipsum volupt."


      >>>    base = Vault(
      ...      from_usr = "myself@mail.com",
      ...      mail_passwd = "myP@$$w)rD",
      ...      to_usr = ["userOne@mail.com", "userTwo@mail.com"],
      ...      subject = subj,
      ...      body = body,
      ...      server = "<your_mail_server>",
      ...      )

      >>>    base.send_mail(port=465)
      ------------------------------------------------------------------------------------------------------
      
      # TOKENS
      
      There is a OTP code feature if you want to send an OTP code for verification by:
      >>>  from kyaah import Tokens
      
      >>>  otp_code = Tokens.mail_otp()
      636937
      
      You can also specify the length of numbers you want by passing a key argument of `_range` in the method like:
      >>>  otp_code = Tokens.mail_otp(_range = 10)
      5373593635
      ------------------------------------------------------------------------------------------------------
      Use `Faker` class for giving you random email address
      
      >>>  import logging
      >>>  from kyaah import Faker
      
      >>>  formatter = "[+] [%(asctime)s] [%(levelname)s] %(message)s"
      >>>  logging.basicConfig(format = formatter)

      >>>  logger = logging.getLogger()
      >>>  logger.setLevel(logging.DEBUG)
      
      >>>  logger.info(Faker().faker())
      ------------------------------------------------------------------------------------------------------
"""
