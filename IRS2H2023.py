taxas = [(0, 0, lambda r: 0), (762, 0, lambda r: 0), (886.57, 0.145, lambda r: 0.145*2.3*(1093.31-r)), (932.14, 0.21, lambda r: 0.21*1.3*(1350.22-r)), (999.14, 0.21, lambda r: 114.14), (1106.93, 0.265,  lambda r: 169.09 ), (1600.36, 0.285,  lambda r: 191.23 ), (1961.93, 0.35,  lambda r: 295.26), (2529.05, 0.37,  lambda r: 334.48 ), (3694.46, 0.3872,  lambda r: 377.86), (5469.9, 0.40052,  lambda r: 427.18 ), (6420.55, 0.42722,  lambda r:573.22 ), (20064.21, 0.44952,  lambda r: 716.08 )]

def calcTaxaEParcela(r):
    current = 0
    for t in range(1, len(taxas)):
        if r > taxas[t-1][0] and r <= taxas[t][0]:
            current = taxas[t][1]
            return (current, taxas[t][2](r))
    return 0


def calcSalarioLiquido(r):
    taxaEParcela = calcTaxaEParcela(r)
    return r - (r * 0.11) - (r*taxaEParcela[0]- taxaEParcela[1])

f = open("out.csv", "w")
f.write("bruto,liquido\n")
for i in range(760, 20000):
    f.write(str(i) + "," + str(calcSalarioLiquido(i)) + "\n")
