from pwn import *
from itertools import chain, combinations

# context.log_level = 'DEBUG'

from random import Random
import copy

visaPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

mastercardPrefixList = [
        ['5', '1'],
        ['5', '2'],
        ['5', '3'],
        ['5', '4'],
        ['5', '5']]

amexPrefixList = [
        ['3', '4'],
        ['3', '7']]

discoverPrefixList = [
        ['6', '0', '1', '1']]


def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:

        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):

            sum += int(reversedCCnumber[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10

    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)


def credit_card_number(rnd, prefixList, length, howMany):

    result = []

    while len(result) < howMany:

        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number(ccnumber, length))

    return result


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0













def main():
    r = remote('misc.chal.csaw.io', 8308)
    
    generator = Random()
    generator.seed()        # Seed from current time
    while True:
        out = r.recvuntil("!")
        if "Visa" in out:
            out = credit_card_number(generator, visaPrefixList, 16, 1)[0]
        elif "American Express" in out:
            out = credit_card_number(generator, amexPrefixList, 15, 1)[0]
        elif "MasterCard" in out:
            out = credit_card_number(generator, mastercardPrefixList, 16, 1)[0]
        elif "Discover" in out:
            out = credit_card_number(generator, discoverPrefixList, 16, 1)[0]
        elif "starts with" in out:
            startswith = out.split()[-1][:-1]
            out = credit_card_number(generator, [list(startswith)], 16, 1)[0]
        elif "ends with" in out:
            endswith = out.split()[-1][:-1]
            while True:
                out = credit_card_number(generator, [['4']], 16, 1)[0]
                if out.endswith(endswith):
                    break
        elif "need to know" in out:
            card = out.split()[5]
            if is_luhn_valid(card):
                out = '1'
            else:
                out = '0'
        else:
            break
        
        r.send(out + "\n")
        out = r.recvuntil("!")
    r.interactive()


if __name__ == '__main__':
    main()
