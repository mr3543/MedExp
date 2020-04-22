import os 

with open('secret_key.txt','wb') as f:
    sk = os.urandom(16)
    f.write(sk)

