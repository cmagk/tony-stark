from math import cos, pi

# Μέση θερμοκρασία
TM = 22
# Διακύμανση
DR = 11
# Η ώρα που η θερμοκρασία είναι μέγιστη
TMAX = 16


ToutTemp = []
Tindex = []

# Ξεκινάμε από 00:00 με το να είναι η ώρα.
for i in range(24):
    temp = TM + (DR / 2) * cos(2 * pi * (i - TMAX) / 24)
    ToutTemp.append(temp)
    Tindex.append(i)  # TODO remove

# Θερμοκρασία εξωτερική ανά ώρα
Tout = list(zip(Tindex, ToutTemp))