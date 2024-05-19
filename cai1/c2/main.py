#!/usr/bin/env python
import shutil
import phe

def encrypt_local():
    pub, priv = phe.generate_paillier_keypair(n_length=3072)
    new_file = []
    gastos = []
    with open('local/gastos.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            id = line.split(';')[0]
            gasto = float(line.split(';')[1])
            gastos.append(pub.encrypt(gasto))
            gastos_confiden = pub.encrypt(gasto)
            new_file.append(f'{id};{gastos_confiden.ciphertext()};{gastos_confiden.exponent};')
    
    with open('local/gastos_confiden.csv', 'w') as f:
        f.write('\n'.join(new_file))
    
    print('Encrypted!')
    return pub, priv
    
def upload_to_cloud():
    shutil.copyfile('local/gastos_confiden.csv', 'cloud/gastos_confiden.csv')
    print('Uploaded!')
    
def operate_in_cloud(pub):
    result = {}
    with open('cloud/gastos_confiden.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            id = line.split(';')[0]
            g = line.split(';')[1]
            exp = line.split(';')[2]
            gasto = phe.EncryptedNumber(pub, int(g), int(exp))
            if id not in result:
                result[id] = gasto
            else:
                result[id] += gasto
    
    with open('cloud/gastos_acum_confiden.csv', 'w') as f:
        for id, gasto in result.items():
            f.write(f'{id};{gasto.ciphertext()};{gasto.exponent};\n')
    
    print('Operated!')
    
def download_from_cloud():
    shutil.copyfile('cloud/gastos_acum_confiden.csv', 'local/gastos_acum_confiden.csv')
    print('Downloaded!')

def decrypt_local(pub, priv):
    gasto_acum = []
    with open('local/gastos_acum_confiden.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            if ";" not in line: continue
            id = line.split(';')[0]
            g = int(line.split(';')[1])
            exp = int(line.split(';')[2])
            gasto = phe.EncryptedNumber(pub, g, exp)
            gasto_dec = priv.decrypt(gasto)
            gasto_acum.append(f'{id};{gasto_dec};')
    
    with open('local/gastos_acum.csv', 'w') as f:
        f.write('\n'.join(gasto_acum))
        
    print('Decrypted!')

if __name__ == '__main__':

    pub, priv = encrypt_local()
    
    upload_to_cloud()
    
    operate_in_cloud(pub)
    
    download_from_cloud()
    
    decrypt_local(pub, priv)
            
        
    