from math import cos, pi

# Μέση θερμοκρασία
Tm = 22
# Διακύμανση
DR = 11
# Η ώρα που η θερμοκρασία είναι μέγιστη
tmax = 16


ToutTemp = []
Tindex = []

# Ξεκινάμε από 00:00 με το να είναι η ώρα.
for i in range(24):
    temp = Tm + (DR / 2) * cos(2 * pi * (i - tmax) / 24)
    ToutTemp.append(temp)
    Tindex.append(i)  # TODO remove

# Θερμοκρασία εξωτερική ανά ώρα
Tout = list(zip(Tindex, ToutTemp))