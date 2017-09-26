## Prophecy (Reversing, 200 points, 26 solves)

    The prophecy is more important than either of us! Reveal its secrets, Zeratul! The future rests on it!" -Karass-

_A surprisingly low solve rate for 200 points. I'll admit this took me longer than expected._

We are provided both the challenge binary [prophecy](prophecy) and a server running the same binary. Opening inside IDA we can quickly see it's large state machine structure and redundant paths within the `parser` function.

![prop1.png](prop1.png)

Fresh off the heels of solving [bananaScript](../rev450_banana) the first step I wanted was to gain further introspection into the state machine. This was done by adding a breakpoint to print information for the state.

```python
b *0x4010FD
commands
  silent
  printf "[+] Exec state: %x\n", $eax
  c
end
```

With this added we can see the last states that were executed and quickly jump to them by searching for their immediate values. This is especially helpful as the binary contains duplicate functionality. The first check needed to pass at state 0x110EB79F is `strstr(buf, '.starcraft')`. Looking further into the binary we see this `buf` being used at state _0x844F148F_ to open our file as writable [_"wb"_], write 300 bytes, and close the file before reopening as readonly [_"rb"_]. Let's add a few more breakpoints for the file interactions.

```python
b fopen
commands
  silent
  printf "[-] Opening: %s\n", $rdi
  c
end

b *0x4028A2
commands
  silent
  printf "[+] Read %d num of bytes\n", $rax
  c
end
```

```[+] Exec state: 962e7c4e
[+] Exec state: 7c688d7e
----------------------------------------------
|PROPHECY PROPHECY PROPHECY PROPHECY PROPHECY|
----------------------------------------------
[*]Give me the secret name
>>BANANA_ME_CRAZY.starcraft
[+] Exec state: a0ebe5ab
[+] Exec state: 43ab77fe
[+] Exec state: 34601a9
[+] Exec state: fa333ff8
[+] Exec state: 90434f0f
[+] Exec state: e490a284
[*]Give me the key to unlock the prophecy
>>key
[+] Exec state: c0f1dacd
[+] Exec state: d1d97fd7
[+] Exec state: 18a41283
[+] Exec state: 16bda242
[+] Exec state: b0155555
[+] Exec state: 110eb79f
[+] Exec state: 3a1099d5
[+] Exec state: f17225d6
[+] Exec state: f458003
[*]Interpreting the secret....
[+] Exec state: 83b82311
[+] Exec state: 6faae75a
[+] Exec state: 844f148f
[-] Opening: /tmp/BANANA_ME_CRAZY.starcraft
[-] Opening: /tmp/BANANA_ME_CRAZY.starcraft
[+] Exec state: ced24adb
[+] Exec state: 7204358c
[+] Exec state: 1f460fa8
[-] Reading: 4
```

We find our first read at state `0x1f460fa8` and a compare against a magic value of `0x17202508`. The result of the compare is stored in `[rbp+var_3D]`. We can presume it will be checked in a future state. Continuing through the binary like this we can trivially determine the magic values necessary to reach the goal.

One roadblock I ran into was that two additional magic values contained null values. I found that when inserting a null value into the key the byte before would also be nulled out. I patched out the checks with the null values for now so I could continue finding the full string, eventually reaching this:

```python
pack("<I", 0x17202508)
+ "AAAAAAAA"
+ chr(0x4B)
+ chr(0x2)
+ "\x93\xea\xe4\0"
+ "ZERATUL"
+ "\0SAVED"
+ "AAAA"
```

Each line above is a separate check within the binary. The code that inserts the null byte into the string is at state _0x18a41283_ performing the action `buf[strlen(buf)-1] = 0;`. This means only the first null byte would get it's prefix nulled, a fact I observed during my quick and dirty testing. _With this knowledge in hand it should have been obvious what to do next. Simply inserting a null byte into the 8 bytes that are not checked after the first magic value. Instead I went down various rabbit holes reversing out what the different paths for the outputting strings did. Wondering if you could control how much data was written to our /tmp/ file performing multiple writes to get our data into the correct format. After solving other challenges I had the epiphany at 1:30AM and got the flag._ Working solution inside [prop.py](prop.py).


`flag{N0w_th3_x3l_naga_that_f0rg3d_us_a11_ar3_r3turn1ng_But d0_th3y_c0m3_to_sav3_0r_t0_d3str0y?}`

_"Now, the Xel'Naga that forged us all, are returning. But do they come to save, or to destroy?" - Dark Prelate Zeratul_
