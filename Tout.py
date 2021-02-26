from math import cos, pi

# Μέση θερμοκρασία
TM = 22
# Διακύμανση
DR = 11
# Η ώρα που η θερμοκρασία είναι μέγιστη
T_MAX = 16


tout_temp = []
t_index = []

# Ξεκινάμε από 00:00 με το να είναι η ώρα.
for i in range(24):
    temp = TM + (DR / 2) * cos(2 * pi * (i - T_MAX) / 24)
    tout_temp.append(temp)
    t_index.append(i)

# Θερμοκρασία εξωτερική ανά ώρα
t_out = list(zip(t_index, tout_temp))