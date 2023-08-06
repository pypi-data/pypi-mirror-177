# Birman
Multipart formdata decoder

### Install


### Get started

Decode multipart form data
```python
from birman import Decoder
# multipart_data = b'---- ...etc'

decoder = Decoder(multipart_data)
result = decoder.decode()
```
This would return a normalized dict
```python
# example from params - ?email=test@test.com&password=wizard
# result -
# {
#     "email": {
#         "name": "email",
#         "value": "test@test.com",
#     },
#     "password": {
#         "name": "password",
#         "value": "wizard",
#     },
# }
```

Parse URI form params
```python
from birman import Encoder

arg = "?email=test@test.com&password=wizard"
result = Encoder.parse_params(arg)
```
This would return a normalized dict
```python
# result -
#  {
#     "email": {
#         "name": "email",
#         "value": "test@test.com",
#     },
#     "password": {
#         "name": "password",
#         "value": "wizard",
#     },
# }
```