symbol="NIFTY17DEC2218510CE"
symbol_1=symbol[:-7]

if "PE"==symbol[-2:]:
    symbol_1+="P"
elif "CE"==symbol[-2:]:
    symbol_1+="C"

symbol_1+=symbol[-7:-2]
print(symbol_1)