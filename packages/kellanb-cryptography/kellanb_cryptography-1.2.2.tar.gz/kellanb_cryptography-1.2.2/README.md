# kellanb-cryptography 

### installation
`pip install kellanb-cryptography`

### use 
### kellanb-cryptography easy 

a tool for quick and simple encryption

`from kellanb-cryptography import easy`


`encrypted = easy.encrypt(data,key)   `<br>
data: string<br>
key: string

`decrypted = easy.decrypt(encrypted,key) `<br>
encrypted: string<br>
key: string

### kellanb-cryptography key
generate a key from password

`from kellanb_cryptography import key`

`key = key.gen_key_from_password(password, length=256)`<br>

password: string<br>
length in bits: int

### kellanb-cryptography aes
encrypt in aes
`from kellanb_cryptography import aes`

`encrypted = aes.encrypt_aes(data, key,mode='GCM')`<br>
data: string<br>
key: string, length 16,24,or 32
mode: 'GCM','EAX',or 'CCM', shows mode of operation

`decrypted = aes.decrypt_aes(encrypted, key)`<br>
encrypted: string<br>
key: string, length 16,24,or 32


### kellanb-cryptography chacha20
encrypt in chacha20
`from kellanb_cryptography import chacha20`

`encrypted = chacha20.encrypt_chacha_20(data, key)`<br>
data: string<br>
key: string, 32 <br>

`decrypted = aes.decrypt_chacha20(encrypted, key)`<br>
encrypted: string<br>
key: string, length 32


### kellanb-cryptography hash
generate a key from password

`from kellanb_cryptography import hash`


`hash.sha256(data)`
data: string, data to be hashed 

`hash.sha256(data)`  
data: string, data to be hashed 

`hash.512(data)`  
data: string, data to be hashed 

`hash.sha3_256(data)`  
data: string, data to be hashed 

`hash.sha3_512(data)`  
data: string, data to be hashed 


### kellanb-cryptography hmac
tamper-proof your messages

`from kellanb_cryptography import hmac`

`mac = hmac.create_hmac(data,password)`

data: string,
password: password to verify with

### NOTE: THIS WILL NOT ENCRYPT YOUR DATA

`hmac.verify_hmac(data,mac,password)`
returns 1 for not tampered, a zero for check fail (data tampered)

data: data to verify
mac: HMAC code
password: password to verify with

