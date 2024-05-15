import syft as sy
import pytorch as torch

# Set up virtual workers
hook = sy.TorchHook()
alice = sy.VirtualWorker(hook, id="alice")
bob = sy.VirtualWorker(hook, id="bob")

# Alice and Bob's private sets
alice_data = [1, 2, 3, 4, 5]
bob_data = [4, 5, 6, 7, 8]

# Encrypt sets
alice_data_encrypted = [torch.tensor([x]).encrypt("alice") for x in alice_data]
bob_data_encrypted = [torch.tensor([x]).encrypt("bob") for x in bob_data]

# Share encrypted sets
alice_data_shared = [x.share(bob, alice) for x in alice_data_encrypted]
bob_data_shared = [x.share(bob, alice) for x in bob_data_encrypted]

# Perform private set intersection
intersection = sy.intersection(alice_data_shared, bob_data_shared)

# Decrypt intersection
intersection_decrypted = [x.get().decode() for x in intersection]

print("Intersection:", intersection_decrypted)
