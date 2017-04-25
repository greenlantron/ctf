## Zipper (Misc, 50 points, 335 solves)

    Something doesn't seem quite right with this zip file.
    
    Can you fix it and get the flag?

We are given a challenge with a [zip file](zipper_50d3dc76dcdfa047178f5a1c19a52118.zip) and a request to fix it. Attempting to unzip it returns an error as expected.
```
$ unzip zipper_50d3dc76dcdfa047178f5a1c19a52118.zip
Archive:  zipper_50d3dc76dcdfa047178f5a1c19a52118.zip
warning:  filename too long--truncating.
[  ]
:  bad extra field length (central)
```

Our next step is to inspect the zip and get more information about what is wrong. Opening it inside of [010 Editor](https://www.sweetscape.com/010editor/) we can use the zip template to better understand what is wrong. From this point I attempted to fix the fields manually. While fixing the primary issues I could still not perform an unzip. Having identified the section containing the data, and not trusting the fields inside of the zip, I decided to bruteforce the decryption.

The algorithm used is COMP_DEFLATE accoridng the zip file and the default. A quick google search of `python deflate` gives us this [stack overflow post](http://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations) which is exactly what we want. Inflate without the header and of only the data. Since the zip file would normally contain that information of length and crc. _At least according to what I understand._ One bruteforce script later starting at the offset of data and we have the flag.

```python
import zlib

with open('zipper_50d3dc76dcdfa047178f5a1c19a52118.zip') as f:
    for i in range(0x1E, 0x88):
        try:
            f.seek(i)
            decoded_data = f.read(0x88 - i)
            print zlib.decompress(decoded_data , -15)
        except Exception as e:
            pass
```

**PCTF{f0rens1cs_yay}**
