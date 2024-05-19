import hashlib, time

def encrypt_local(filename, i):
    with open(filename) as f:
        lines = f.read().split('\n')
        code_list = [get_signature(line, i) for line in lines]
    
    with open(filename.split('.csv')[0]+'_encrypted.csv', 'w') as f:
        f.write('\n'.join(code_list))
        
    print('Encrypted!')
    
def operate_in_cloud():
    with open('data/dummy_passengers_encrypted.csv') as f:
        lines = f.read().split('\n')
        passengers = set(lines)
    
    with open('data/dummy_noflight_encrypted.csv') as f:
        lines = f.read().split('\n')
        no_flight = set(lines)
    
    intersection = passengers.intersection(no_flight)
    
    with open('data/intersection_encrypted.csv', 'w') as f:
        f.write('\n'.join(intersection))
    
    print('Operated!')

def decrypt_local(i):
    with open('data/intersection_encrypted.csv') as f:
        lines = f.read().split('\n')
        local_intersection = set(lines)
    print("LOCAL INTERSECTION")
    local_count = 0
    with open('data/dummy_passengers.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            encrypted_line = get_signature(line, i)
            if encrypted_line in local_intersection:
                print("LOCAL: "+line)
                local_count += 1
                if local_count == len(local_intersection):
                    break
           
    with open('data/intersection_encrypted.csv') as f:   
        lines = f.read().split('\n')
        gov_intersection = set(lines)    
    gov_count = 0
    print("GOV INTERSECTION")
    with open('data/dummy_noflight.csv') as f:
        lines = f.read().split('\n')
        for line in lines:
            encrypted_line = get_signature(line, i)
            if encrypted_line in gov_intersection:
                print("GOV: "+line)
                gov_count += 1
                if gov_count == len(gov_intersection):
                    break

def get_signature(message, i):
    if i == 256:
        signature = hashlib.sha256(bytes(message, 'utf-8')).hexdigest()
    elif i == 1:
        signature = hashlib.sha1(bytes(message, 'utf-8')).hexdigest()
    elif i == 224:
        signature = hashlib.sha224(bytes(message, 'utf-8')).hexdigest()
    elif i == 384:
        signature = hashlib.sha384(bytes(message, 'utf-8')).hexdigest()
    elif i == 512:
        signature = hashlib.sha512(bytes(message, 'utf-8')).hexdigest()
    else:
        signature = hashlib.sha256(bytes(message, 'utf-8')).hexdigest()
    return signature

if __name__ == '__main__':
    for i in [224, 256, 384, 512]:
        print("Execution time for sha", i)
        start = time.time()
        encrypt_local('data/dummy_passengers.csv', i)
        encrypt_local('data/dummy_noflight.csv', i)
        operate_in_cloud()
        decrypt_local(i)
        end = time.time()
        print('Execution time:', end - start)
    