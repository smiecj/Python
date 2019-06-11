#-*- coding: UTF-8 -*- 
import requests
import OpenSSL
import json
import sys
import importlib

sys.getdefaultencoding()
importlib.reload(sys)

def p12_to_pem(certname, pwd):
    # pem_name = certname + ".pem"
    # f_pem = open(pem_name, 'wb')
    # p12file = certname + ".p12"
    # p12 = OpenSSL.crypto.load_pkcs12(open(p12file, 'rb').read(), pwd)
    # f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
    # f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
    # ca = p12.get_ca_certificates()
    # if ca is not None:
        # for cert in ca:
            # f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
    # f_pem.close()
    pem_name = certname + ".pem"
    return pem_name
    
def get_request(url,header):
    print("Get request url: " + url + "; header: " + str(header))
    time = 0
    while True:
        time = time + 1
        try:
            r = requests.get(url, headers=header, verify=False, timeout=100)
        except (BaseException, e):
            print("request failed!", e)
        else:
            # judge whether return code is ok
            if r.status_code != 404:
                print("request success!")
                return r.text
            else:
                print("return code is ", r.status_code)
        if time > 3:
            print("Connect " + str(time) + " time failed! Please check.")
            return False
        print("Connect " + str(time) + " time failed! Will connect again.")