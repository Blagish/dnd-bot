from parser import d2

print(d2('d%'))
print(d2('sum(3 cock)'))
print(d2('d20+ad20+ed20+kd20'))
print(d2('d20%5 AAA + d20 BBB + d20 AAA'))
print(d2('2ad20%18 BBB'))
print(d2('sum(4 cock, 2 cock, 1 rock)'))
print(d2('min(4 cock, 2 cock, 1 rock)'))
print(d2('max(4 cock, 2 cock, 1 rock)'))
print(d2('sum(map(((it=2)+(it=4)+2*(it=6)):5x(d6)))'))
print(d2('sum(6x(d20 рыба))'))
print(d2('sum(3 аааа, 4 аааа, 5 баа)'))
print(d2('3 аааа + 4 аааа + 5 баа'))

print(d2('(3, 4) + 5'))
print(d2('(3 пог, 4 пег) + (5 пог, д6)'))
print(d2('sum((3 пог, 4 пег) + (5 пог, д6))'))
print(d2('2 * (3, 4)'))
