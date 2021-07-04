from base64 import b64encode, b64decode
def base64_encode_str(s: str) -> str:
    s_byte = s.encode("utf-8")
    by = b64encode(s_byte)
    return by.decode("utf-8")

# こちらは使わないが、convert のチェックのみ
def base64_decode_str(s:str) -> str:
    byte_decoded = b64decode(s)
    return byte_decoded.decode("utf-8")
