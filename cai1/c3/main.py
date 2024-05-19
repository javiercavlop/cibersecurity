import hashlib, shutil

def encrypt_local(filename):
    with open(filename) as f:
        lines = f.read().split('\n')
        code_list = [hashlib.sha256(bytes(line, 'utf-8')).hexdigest() for line in lines]
    
    with open(filename.split('.csv')[0]+'_encrypted.csv', 'w') as f:
        f.write('\n'.join(code_list))
        
    print('Encrypted!')

def upload_to_cloud():
    shutil.copyfile('local/passengers_encrypted.csv', 'cloud/passengers_encrypted.csv')
    shutil.copyfile('gov/noflight_encrypted.csv', 'cloud/noflight_encrypted.csv')
    print('Uploaded!')
    
def operate_in_cloud():
    with open('cloud/passengers_encrypted.csv') as f:
        lines = f.read().split('\n')
        passengers = set(lines)
    
    with open('cloud/noflight_encrypted.csv') as f:
        lines = f.read().split('\n')
        no_flight = set(lines)
    
    intersection = passengers.intersection(no_flight)
    
    with open('cloud/intersection_encrypted.csv', 'w') as f:
        f.write('\n'.join(intersection))
    
    print('Operated!')
            
def download_from_cloud():
    shutil.copyfile('cloud/intersection_encrypted.csv', 'local/intersection_encrypted.csv')
    shutil.copyfile('cloud/intersection_encrypted.csv', 'gov/intersection_encrypted.csv')
    print('Downloaded!')

def decrypt_local():
    with open('local/intersection_encrypted.csv') as f:
        lines = f.read().split('\n')
        local_intersection = set(lines)
    print("LOCAL INTERSECTION")
    local_count = 0
    with open('local/passengers.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            encrypted_line = hashlib.sha256(bytes(line, 'utf-8')).hexdigest()
            if encrypted_line in local_intersection:
                print("LOCAL: "+line)
                local_count += 1
                if local_count == len(local_intersection):
                    break
           
    with open('gov/intersection_encrypted.csv') as f:   
        lines = f.read().split('\n')
        gov_intersection = set(lines)    
    gov_count = 0
    print("GOV INTERSECTION")
    with open('gov/noflight.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            encrypted_line = hashlib.sha256(bytes(line, 'utf-8')).hexdigest()
            if encrypted_line in gov_intersection:
                print("GOV: "+line)
                gov_count += 1
                if gov_count == len(gov_intersection):
                    break

if __name__ == '__main__':
    # Encrypting the files in the local directory of the client
    encrypt_local('local/passengers.csv')
    # Encrypting the files in the local directory of the government
    encrypt_local('gov/noflight.csv')
    # Uploads the encrypted files to the cloud
    upload_to_cloud()
    # Operates in the cloud
    operate_in_cloud()
    # Downloads the result from the cloud
    download_from_cloud()
    # Decrypts the result in the local directories of the client and the government
    decrypt_local()
    