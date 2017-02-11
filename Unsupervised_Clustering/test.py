import k_means as km

def difference(v1, v2):
    """Basic geometric difference."""
    sum = 0
    for i in range(len(v1)):
        sum += (v1[i] - v2[i]) ** 2
    return sum ** (1.0/2)

test = """3	4	5	6
8	9	6	-1"""

print(km.k_means(2, km.tsv_to_features(test), difference))
