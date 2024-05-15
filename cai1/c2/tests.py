import paillier
import time

def test_if_works():
    print("Testing if it works")
    start = time.time()
    priv, pub = paillier.generate_keypair(1536)
    mean_time_iter = []
    for i in range (0, 100):
        print("Testing", i)
        time_iter = time.time()
        x = paillier.encrypt(pub, i)
        y = paillier.encrypt(pub, i+1)
        z = paillier.e_add(pub, x, y)
        assert paillier.decrypt(priv, pub, z) == i + i + 1
        end_iter = time.time()
        print("Time iter:", end_iter - time_iter)
        mean_time_iter.append(end_iter - time_iter)
        
    end = time.time()
    print("Time:", end - start)
    mean_time_iter = sum(mean_time_iter) / len(mean_time_iter)
    print("Mean time iter:", mean_time_iter)
    

        
def test_big_numbers():
    print("Testing big numbers")
    start = time.time()
    priv, pub = paillier.generate_keypair(1536)
    n = 100000000000000000000
    x = paillier.encrypt(pub, n)
    y = paillier.encrypt(pub, n*2)
    z = paillier.e_add(pub, x, y)
    assert paillier.decrypt(priv, pub, z) == n*3
    end = time.time()
    print("Time:", end - start)

if __name__ == '__main__':
    test_if_works()
    test_big_numbers()
    print('All tests passed!')