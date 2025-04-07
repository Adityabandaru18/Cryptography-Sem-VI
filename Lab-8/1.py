from py_ecc.bls.ciphersuites import G2ProofOfPossession as bls
import random

NUM_CLIENTS = 3

clients = []
for i in range(NUM_CLIENTS):
    sk = bls.KeyGen(i.to_bytes(2, 'big')) 
    pk = bls.SkToPk(sk) 
    clients.append({'id': i, 'sk': sk, 'pk': pk})

messages = [f"Client-{c['id']}-message".encode() for c in clients]
signatures = []

print("=== Client Signatures ===")
for i, client in enumerate(clients):
    msg = messages[i]
    sig = bls.Sign(client['sk'], msg)
    signatures.append(sig)
    print(f"Client {client['id']} signed: {msg.decode()}")
    print(f"Signature: {sig.hex()[:60]}...")

print("\n=== Server Verification ===")
for i, client in enumerate(clients):
    msg = messages[i]
    valid = bls.Verify(client['pk'], msg, signatures[i])
    status = "VALID" if valid else "INVALID"
    print(f"Verification for Client {client['id']} message: {status}")

print("\n=== Aggregated Signature (Optional) ===")
common_message = b"shared-message"
individual_sigs = [bls.Sign(c['sk'], common_message) for c in clients]
aggregated_sig = bls.Aggregate(individual_sigs)
pubkeys = [c['pk'] for c in clients]

is_valid_agg = bls.FastAggregateVerify(pubkeys, common_message, aggregated_sig)
print(f"Aggregated Signature Verification: {'VALID' if is_valid_agg else 'INVALID'}")
