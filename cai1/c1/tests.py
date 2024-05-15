from main import get_signature
import time

NONCE = 1
SECRET_KEY = 'secretkey'

def test_check_it_works():
    start = time.time()
    file1 = 'tests/file1.txt'
    file2 = 'tests/file2.txt'
    with open(file1, 'w') as f:
        c1 = f.write('content')
    with open(file2, 'w') as f:
        c2 = f.write('content')
    assert get_signature(c1) == get_signature(c2)
    print('File has not changed!')
    end = time.time()
    print('Execution time:', end - start)
    
def test_detect_change():
    start = time.time()
    file1 = 'tests/file1.txt'
    file2 = 'tests/file2.txt'
    with open(file1, 'w') as f:
        c1 = f.write('content')
    with open(file2, 'w') as f:
        c2 = f.write('content2')
    assert get_signature(c1) != get_signature(c2)
    print('File has changed!')
    end = time.time()
    print('Execution time:', end - start)

def test_different_secrets():
    start = time.time()
    file1 = 'tests/file1.txt'
    file2 = 'tests/file2.txt'
    with open(file1, 'w') as f:
        c1 = f.write('content')
    with open(file2, 'w') as f:
        c2 = f.write('content')
    signature1 = get_signature(c1)
    secret_key = 'secretkey2'
    signature2 = get_signature(c2, secret_key=secret_key)
    assert signature1 != signature2
    print('Different secrets!')
    end = time.time()
    print('Execution time:', end - start)

def test_different_nonces():
    start = time.time()
    file1 = 'tests/file1.txt'
    file2 = 'tests/file2.txt'
    with open(file1, 'w') as f:
        c1 = f.write('content')
    with open(file2, 'w') as f:
        c2 = f.write('content')
    signature1 = get_signature(c1)
    nonce = 2
    signature2 = get_signature(c2, nonce=nonce)
    assert signature1 != signature2
    print('Different nonces!')
    end = time.time()
    print('Execution time:', end - start)

if __name__ == '__main__':
    test_check_it_works()
    test_detect_change()
    test_different_secrets()
    test_different_nonces()
    