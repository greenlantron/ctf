## bananaScript (Reversing, 450 points, 24 solves)

    Not too sure how to Interpret this, the lab member who wrote this "forgot" to write any documentation. This shit, and him, is bananas. B, A-N-A-N-A-S.

_This challenge took me the longest and I ended up bruteforcing possible flags at the end._

We're given a binary [monkeyDo](monkeyDo) and an input [banana.script](banana.script). The script contains 125 lines of various number of `BANANAS` with mixed capitalizations. `BANANAS` is 7 letters and with only the capitalization changing per letter each field has 2^7 (128) values. The challenge was updated to include additional scripts but the first one is what we need to reverse in order to get the flag.

Internal the monkeyDo binary reads the script for various opcodes that operate on it's 16 internal buffers/registers. You can read stdin from a buffer, print out a buffer, store a value, compare buffers together, do basic math operations, mix buffers together, and a rolling xor. Possibly even more. I added a breakpoint into the binary so I could see what line of the script was being executed as each point to aid in my dynamic analysis.

```python
b *0x04074E6
commands
silent
printf "Processing line %d\n", (*(int*)($rbp-0xE50) + 1)
c
end
```

With the help of the breakpoint I could quickly go back and see where checks were being performed. After reversing the binary and passing the initial checks I wanted to make a simplified test case version of the script. You can find the heavily annotated version in [simple.banana](simple.banana). I first attempted to read in a raw string as the buffer for the xor with the flag but it seemed I was perhaps needing a character that wouldn't input correctly. So instead I keep the `banaNAs!` magic value and work against that before I xor against the flag. I generate an ugly script to do just that and printed out all the possible flags. I correctly guessed that the last character of the string would be an `s` from the partial flag I could view. After trying a couple which seemed right I got the actual correct flag.

`flag{0r4ng3_3w3_ch1pp3r_1_h47h_n07_s4y_b4n4n4rs}`
