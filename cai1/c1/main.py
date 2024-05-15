import hmac
import hashlib
import shutil, os

NONCE = 1
SECRET_KEY = 'secretkey'

def get_signature(content, secret_key=SECRET_KEY, nonce=NONCE):
    message = '{} {}'.format(nonce, content)
    signature = hmac.new(
        bytes(secret_key, 'utf-8'), 
        msg=bytes(message, 'utf-8'), 
        digestmod=hashlib.sha256).hexdigest().upper()
    return signature

def store_hashes():
    files_list = os.listdir('local/files')
    signatures = []
    for file_path in files_list:
        with open(f'local/files/{file_path}', 'rb') as file:
            data = file.read()
            signature = get_signature(data)
            signatures.append((file_path, signature))
            
    with open('local/hashes.csv', 'w') as f:
        for file_path, signature in signatures:
            f.write(f'{file_path};{signature};\n')
        print('Stored!')
        
def upload_to_cloud():
    files_list = os.listdir('local/files')
    for file_path in files_list:
        shutil.copyfile(f'local/files/{file_path}', f'cloud/files/{file_path}')
    print('Uploaded!')
    
def cloud_provider_calculate_hashes():
    files_list = os.listdir('cloud/files')
    signatures = []
    for file_path in files_list:
        with open(f'cloud/files/{file_path}', 'rb') as file:
            data = file.read()
            signature = get_signature(data)
            signatures.append((file_path, signature))
            
    with open('cloud/hashes.csv', 'w') as f:
        for file_path, signature in signatures:
            f.write(f'{file_path};{signature};\n')
        print('Stored!')
        
def download_hashes():
    shutil.copyfile('cloud/hashes.csv', 'local/hashesCloud.csv')
    print('Downloaded!')
    
def check_hashes():
    local_hashes = {}
    with open('local/hashes.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            if ";" not in line: continue
            file_path = line.split(';')[0]
            signature = line.split(';')[1]
            local_hashes[file_path] = signature
    
    cloud_hashes = {}
    with open('local/hashesCloud.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            if ";" not in line: continue
            file_path = line.split(';')[0]
            signature = line.split(';')[1]
            cloud_hashes[file_path] = signature
        
    for file_path, signature in local_hashes.items():
        if cloud_hashes[file_path] != signature:
            print(f'File {file_path} has been tampered!')
        else:
            print(f'File {file_path} is safe!')

if __name__ == '__main__':
    store_hashes()
    upload_to_cloud()
    cloud_provider_calculate_hashes()
    download_hashes()
    check_hashes()