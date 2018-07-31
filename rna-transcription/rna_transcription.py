dna_to_rna_grammar = {
    'G': 'C',
    'C': 'G',
    'T': 'A',
    'A': 'U'
}
def to_rna(dna_strand):
    return ''.join([ dna_to_rna_grammar[c] for c in dna_strand ])
