#Implement Union, Intersection, Complement and Difference operations on fuzzy sets. Also create fuzzy relations by Cartesian product of any two fuzzy sets and perform max-min composition on any two fuzzy relations.


# Define Fuzzy Set Operations

def fuzzy_union(set_a, set_b):
    """Perform the union of two fuzzy sets"""
    return {key: max(set_a.get(key, 0), set_b.get(key, 0)) for key in set_a.keys() | set_b.keys()}

def fuzzy_intersection(set_a, set_b):
    """Perform the intersection of two fuzzy sets"""
    return {key: min(set_a.get(key, 0), set_b.get(key, 0)) for key in set_a.keys() & set_b.keys()}

def fuzzy_complement(set_a):
    """Compute the complement of a fuzzy set"""
    return {key: 1 - value for key, value in set_a.items()}

def fuzzy_difference(set_a, set_b):
    """Compute the difference of two fuzzy sets"""
    return {key: max(set_a.get(key, 0) - set_b.get(key, 0), 0) for key in set_a.keys()}

def fuzzy_cartesian_product(set_a, set_b):
    """Compute the Cartesian product of two fuzzy sets"""
    return {(a, b): min(set_a.get(a, 0), set_b.get(b, 0)) for a in set_a for b in set_b}

def fuzzy_max_min_composition(relation_r, relation_s):
    """Perform max-min composition of two fuzzy relations"""
    result = {}
    # Iterate over each pair (a, c)
    for (a, b1), val1 in relation_r.items():
        for (b2, c), val2 in relation_s.items():
            if b1 == b2:  # b1 from relation_r should match b2 from relation_s
                result[(a, c)] = max(result.get((a, c), 0), min(val1, val2))
    return result

# Example fuzzy sets
set_a = {'a': 0.5, 'b': 0.8, 'c': 0.2}
set_b = {'b': 0.6, 'c': 0.7, 'd': 0.3}
set_c = {'c': 0.9, 'd': 0.4}

# Perform set operations
print("Union:", fuzzy_union(set_a, set_b))
print("Intersection:", fuzzy_intersection(set_a, set_b))
print("Complement of set_a:", fuzzy_complement(set_a))
print("Difference of set_a and set_b:", fuzzy_difference(set_a, set_b))

# Create fuzzy relations by Cartesian product
relation_ab = fuzzy_cartesian_product(set_a, set_b)
print("Fuzzy Relation (A x B):", relation_ab)

relation_bc = fuzzy_cartesian_product(set_b, set_c)
print("Fuzzy Relation (B x C):", relation_bc)

# Perform max-min composition on fuzzy relations
composition_result = fuzzy_max_min_composition(relation_ab, relation_bc)
print("Max-Min Composition (R ∘ S):", composition_result)
