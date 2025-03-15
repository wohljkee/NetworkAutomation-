print(ord('a'))
print(chr(97))

print(120 ^ 140)  # 1010 ^ 1111  = 0101; 0101 ^ 1111 = 1010

enc = chr(ord('a') ^ 240)
print(enc)

dec = chr(ord(enc) ^ 240)
print(dec)