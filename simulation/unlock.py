import hashlib, sys, binascii

BANNER = "=== XAVARIA ARCHIVE UNLOCK ==="
# encrypted message; unlocked by passphrase AEONKERNELGATE
ENC_HEX = "4c700d751d9417f266a806ee8d73dd1b00eb2dc184f4ef16523936007a2e5d7db7fa5f3c92d235301790515bcfb33abc90e22d7a521eb400fda0b9c6629d0a4a9a5ace64d61d3db60b6ff32dfcfafe1f1a9792a1a7a6dbe2797ab13b2a89e87af8030f13f80bfd5c3e20b69fdfb2b0a7219d9a2b71a64b4ad2b7a1"

def derive_key(passphrase: str) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()

def xor_stream(data: bytes, key: bytes) -> bytes:
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return bytes(out)

def main():
    print(BANNER)
    if len(sys.argv) != 2:
        print("usage: python3 unlock.py <PASSphrase>")
        sys.exit(1)
    key = derive_key(sys.argv[1])
    enc = binascii.unhexlify(ENC_HEX)
    plain = xor_stream(enc, key)
    try:
        text = plain.decode()
    except UnicodeDecodeError:
        print("❌ wrong passphrase.")
        sys.exit(2)
    if "FLAG{" in text:
        print("✅ unlocked!\n")
        print(text)
    else:
        print("❌ wrong passphrase.")

if __name__ == "__main__":
    main()
