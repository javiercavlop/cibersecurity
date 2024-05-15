#!/usr/bin/env python

import paillier
import shutil

def encrypt_local():
    priv, pub = paillier.generate_keypair(1536)
    new_file = []
    with open('local/gastos.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            id = line.split(';')[0]
            gasto = int(line.split(';')[1])
            gastos_confiden = paillier.encrypt(pub, gasto)
            new_file.append(f'{id};{gastos_confiden};')
    
    with open('local/gastos_confiden.csv', 'w') as f:
        f.write('\n'.join(new_file))
        
    print('Encrypted!')
    return priv, pub
    
def upload_to_cloud():
    shutil.copyfile('local/gastos_confiden.csv', 'cloud/gastos_confiden.csv')
    print('Uploaded!')
    
def operate_in_cloud(pub):
    result = {}
    with open('cloud/gastos_confiden.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            id = line.split(';')[0]
            gasto = int(line.split(';')[1])
            if id not in result:
                result[id] = gasto
            else:
                result[id] = paillier.e_add(pub, result[id], gasto)
    
    with open('cloud/gastos_acum_confiden.csv', 'w') as f:
        for id, gasto in result.items():
            f.write(f'{id};{gasto};\n')
    
    print('Operated!')
    
def download_from_cloud():
    shutil.copyfile('cloud/gastos_acum_confiden.csv', 'local/gastos_acum_confiden.csv')
    print('Downloaded!')

def decrypt_local(priv, pub):
    gasto_acum = []
    with open('local/gastos_acum_confiden.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            if ";" not in line: continue
            id = line.split(';')[0]
            gasto = int(line.split(';')[1])
            gasto_dec = paillier.decrypt(priv, pub, gasto)
            gasto_acum.append(f'{id};{gasto_dec};')
    
    with open('local/gastos_acum.csv', 'w') as f:
        f.write('\n'.join(gasto_acum))
        
    print('Decrypted!')

if __name__ == '__main__':

    priv, pub = encrypt_local()
    
    upload_to_cloud()
    
    operate_in_cloud(pub)
    
    download_from_cloud()
    
    decrypt_local(priv, pub)
            
        
    