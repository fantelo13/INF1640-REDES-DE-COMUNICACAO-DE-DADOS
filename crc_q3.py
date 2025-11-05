#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Tabela completa do LFSR para GEN = "1011011"

GEN = "1011011"   # x^6 + x^4 + x^3 + x + 1  (indiscutível)
MSG = "10001100011111010001110000111110"

def step(R, I):
    R5,R4,R3,R2,R1,R0 = R
    f = R5 ^ I                  # feedback
    # atualiza (taps em R4, R3, R1 e R0)
    R5p = R4
    R4p = R3 ^ f
    R3p = R2 ^ f
    R2p = R1
    R1p = R0 ^ f
    R0p = f
    return (R5p,R4p,R3p,R2p,R1p,R0p), f

def bits_to_str(R): return ''.join(str(b) for b in R)

def run_table(msg_bits):
    R = (0,0,0,0,0,0)
    print("t  I  f |  R5 R4 R3 R2 R1 R0   (estado após o clock)")
    print("-- -- --+----------------------")
    # fase A: 32 bits da mensagem (MSB->LSB)
    for t,ch in enumerate(msg_bits):
        I = int(ch)
        R, f = step(R, I)
        print(f"{t:02d} {I}  {f} |  {R[0]}  {R[1]}  {R[2]}  {R[3]}  {R[4]}  {R[5]}")
    # estado após a entrada de todos os bits
    print("\nEstado após t=31 (deve ser o CRC):", bits_to_str(R))
    # fase B (flush): 6 clocks com I=0
    for k in range(6):
        t = 32 + k
        R, f = step(R, 0)
        print(f"{t:02d} 0  {f} |  {R[0]}  {R[1]}  {R[2]}  {R[3]}  {R[4]}  {R[5]}")
    print("\nEstado final após flush:", bits_to_str(R))

if __name__ == "__main__":
    run_table(MSG)
