# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 13:33:43 2018

@author: nallen
"""

# -*- coding: utf-8 -*-
#!/usr/bin/python2.7
#
# Test being run to export shelf list to collection managers
# Email Excel Spreadhseet to manager and supervisor 
# Use XlsxWriter to create spreadsheet from SQL Query
# 
#

import psycopg2
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import datetime



excelfile =  'WrongAudienceAdult.xlsx'



#Set variables for email

emailhost = 'mail.greenwichlibrary.org'
emailport = '25'
emailsubject = 'Adult bibs with incorrect Audience Facet'
emailmessage = '''Attached is a list of bibs that have the incorrect audience facet for Adult. The audience facet should be 'e'. Instructions for how to update these items can be found on the wiki or by following this link: http://wiki.greenwichlibrary.org/Using-Global-Update-to-edit-the-Audience-Facet.ashx'''
emailfrom = 'nallen@greenwichlibrary.org'
emailto = ['nallen@greenwichlibrary.org']
#,'cataloging2@greenwichlibrary.org','EMcCarthy@greenwichlibrary.org','mribadeneira@greenwichlibrary.org','JTrivedi@greenwichlibrary.org','mderr@greenwichlibrary.org','rcolford@greenwichlibrary.org','MCurcio@greenwichlibrary.org','mjinno@greenwichlibrary.org','SSchugmann@greenwichlibrary.org','SSchmidt@greenwichlibrary.org','ywang@greenwichlibrary.org']

try:
    conn = psycopg2.connect("dbname= user= host= port= password= sslmode=require")
except psycopg2.Error as e:
    print ("Unable to connect to database: " + str(e))
    
cursor = conn.cursor()
cursor.execute(open("wrongaudienceAdult.sql","r",).read())
rows = cursor.fetchall()
conn.close()


workbook = xlsxwriter.Workbook(excelfile, {'remove_timezone': True})
worksheet = workbook.add_worksheet()


worksheet.set_landscape()
worksheet.hide_gridlines(0)



eformat= workbook.add_format({'text_wrap': True, 'valign': 'top' , 'num_format': 'mm/dd/yy'})
eformatlabel= workbook.add_format({'text_wrap': False, 'valign': 'top', 'bold': True})


worksheet.set_column(0,0,20.89)
worksheet.set_column(1,1,14)
worksheet.set_column(2,2,14)
worksheet.set_column(3,3,11)
worksheet.set_column(4,4,42)




worksheet.set_header('WrongAudienceAdult')

worksheet.write(0,0,'Call number', eformatlabel)
worksheet.write(0,1,'Facet character', eformatlabel)
worksheet.write(0,2,'Material type', eformatlabel)
worksheet.write(0,3,'Record No.', eformatlabel)
worksheet.write(0,4,'Title', eformatlabel)




for rownum, row in enumerate(rows):
    worksheet.write(rownum+1,0,row[0])
    worksheet.write(rownum+1,1,row[1])
    worksheet.write(rownum+1,2,row[2], eformat)
    worksheet.write(rownum+1,3,row[3])
    worksheet.write(rownum+1,4,row[4], eformat)



    
    

workbook.close()


#Creating the email message
msg = MIMEMultipart()
msg['From'] = emailfrom
if type(emailto) is list:
    msg['To'] = ','.join(emailto)
else:
    msg['To'] = emailto
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = emailsubject
msg.attach (MIMEText(emailmessage))
part = MIMEBase('application', "octet-stream")
part.set_payload(open(excelfile,"rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition','attachment; filename=%s' % excelfile)
msg.attach(part)

#Sending the email message
smtp = smtplib.SMTP(emailhost, emailport)
smtp.sendmail(emailfrom, emailto, msg.as_string())
smtp.quit()








