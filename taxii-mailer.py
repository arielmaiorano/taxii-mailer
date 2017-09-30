###############################################################################
# taxii-mailer.py
#
# úsese: python taxii-mailer.py
#
# ver. 0.1 - 02/06/2019
#
###############################################################################

###############################################################################

# configuraciones para el server TAXII
TAXII_SERVER_HOST = 'open.taxiistand.com'
TAXII_SERVER_SSL = True
TAXII_DISCOVERY_PATH = '/services/discovery'
TAXII_COLLECTION_NAME = 'hailataxii.guest.Abuse_ch'
#TAXII_COLLECTION_NAME = 'hailataxii.guest.MalwareDomainList_Hostlist'

# mails de destino
EMAIL_DESTINATARIOS = ['xxx@gmail.com']

# configuración SMTP
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
SMTP_USER = 'yyy@gmail.com'
SMTP_PASSWORD = 'yyy123'

###############################################################################

from cabby import create_client
from stix.core import STIXPackage
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from io import StringIO
from datetime import datetime, timedelta
import pytz
from pprint import pprint


# conexión al server taxii
client = create_client(TAXII_SERVER_HOST, use_https=TAXII_SERVER_SSL, discovery_path=TAXII_DISCOVERY_PATH)

# fecha para poll (bloques registrados con fecha >= X)
fechahora_desde = datetime.now(pytz.utc) - timedelta(hours=4)
#print("fecha/hora desde: " + str(fechahora_desde))

# resumen de indicadores para mail...
mail_indicadores = 'INDICADORES DESDE ' + str(fechahora_desde) + ' [' + TAXII_SERVER_HOST + ']\n\n'

# poll de bloques...
content_blocks = client.poll(collection_name=TAXII_COLLECTION_NAME, begin_date=fechahora_desde)
for block in content_blocks:
    #print(type(block.content))
    #print('==============================================')
    #print(block.content)
    #print('==============================================')

    sio = StringIO(block.content.decode('utf-8'))
    package = STIXPackage.from_xml(sio)

    #package_intent = package.stix_header.package_intents[0]
    #print(type(package_intent), package_intent.xsi_type, package_intent)
    #print('==============================================')

    stix_dict = package.to_dict()
    #pprint(stix_dict)
    #print('==============================================')

    print('procesando bloque id: ' + stix_dict['id'])
    
    '''
    if 'observables' not in stix_dict:
        print('sin observables.')
        pprint(stix_dict)
        continue
    for observable in stix_dict['observables']['observables']:
        print("-> " + observable['description'])
        print("-> " + observable['title'])
    '''


    if 'indicators' in stix_dict:
        for indicator in stix_dict['indicators']:
            mail_indicadores += 'Fecha/hora: ' + indicator['timestamp'] + '\n'
            mail_indicadores += 'Título: ' + indicator['title'] + '\n'
            mail_indicadores += 'Descripción: ' + indicator['description'] + '\n'
            mail_indicadores += '\n'
        print('.', end='')
    else:
        print('x', end='')


#print(mail_indicadores)

try:
    mensaje = MIMEText(mail_indicadores, _charset="UTF-8")
    mensaje['Subject'] = Header('Reporte TAXII', "utf-8")
    smtp = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER, EMAIL_DESTINATARIOS, mensaje.as_string())
    smtp.quit()
except Exception as ex:
    print('ERROR AL ENVIAR MAIL.')
    print(ex)

