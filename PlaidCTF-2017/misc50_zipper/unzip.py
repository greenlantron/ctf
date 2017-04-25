import zlib

with open('zipper_50d3dc76dcdfa047178f5a1c19a52118.zip') as f:
    for i in range(0x1E, 0x88):
        try:
            f.seek(i)
            decoded_data = f.read(0x88 - i)
            print zlib.decompress(decoded_data , -15)
        except Exception as e:
            pass
