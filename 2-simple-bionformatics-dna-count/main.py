import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

image = Image.open("2-simple-bionformatics-dna-count/dna.jpg")

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA

***
""")

st.header("Enter DNA sequence")

sequence_input = """>DNA Query\n
GGTATGTTCCCTGCTTGGCGCGTTCCTTCTAGGCTTTGCGGGCACGAGACCTTATTGAGT\n
GCCCACCCCGTGCTCTGTCACCAAGAGGGGTTTCTGGTTACCCTAGAAGGCCTAGTGTTT\n
ACAGGCGCTAGGAGGGGCACGCTTTCGTCTTTGATTTGGAGATACCTTCGTGATACCACC\n
CCACGGAATCCGCAAGTCGGGATACTTCTGGTAGCATTACAAATAAGTTTCAGGGTGGCA\n
CCTAGTTGCGTGCAACTGAAGGCGAATCCTCTGTAAGCGCCCACCAACGGGTATCCTAGT\n
CGGCCACTAATTCGGCATGGTATAAGATAACACGGCCTGATGCTCAAAGCATCACGCCAT\n
TTAAGATGCTTATAATTGTACCCCTAAAATGAGTCCACGGATGTAATGAACGGGCGGCCT\n
AAGCCAGCCCCCATCTCGCATTAATAGTTTCCCGAAGTCCCTAAACGTTTTGATTCTTGC\n
CATAAGTCCGTTGTACTTGGCACAGAAACGCAAGTATGGACGGTAATGCCTCCCACACTA\n
GGCGGAAACTTTTACGCCTCACGCCAAACTAGCTGTTGTTTGTTTTTACTCTTGCAGCAT\n
CTGGCTCGGCACGAGTTTCTAAGGCTTTCGTGACGTAGTCCTAACTACCTTGAGGTGAAT\n
CCGTAACTCCGCGAGCGTCAAGCGATACGCAGTCTCGGGAGTGTCTCTAGAAAAGATCCT\n
CCAAACCCTTTACCGCACAAGATTAAGCTCGTTATTCAAACCCAATGTGGAGTTTATGCC\n
GCACAAGATGGGGCACGCTCGCGTTGCAAGTATAAATATGATGATATCCCAGTGTCAGGG\n
TTTCAACTGCCAGTCTGTACGCGCCGTAAGACCGGCCATACTACCATTAGGTTTACCGTG\n
AACACTGAAGAATGGGGGATTCGGTTTCTTGCGTGTCCATCTTCTAGTGCCCGGTACGAG\n
TGGCGCGTGTCATGACGTGGACTCGCTACTGGTTTAGGGT
"""
sequence = st.text_area("Sequence input", sequence_input, height=25)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = "".join(sequence)

st.write("***")

st.header("Input (DNA Query)")
sequence

st.header("Output (DNA Nucleotide Counts)")

st.subheader("1. Print dictionary")
def DNA_nucleotide_count(sequence):
    d = dict([
        ("A", sequence.count("A")),
        ("T", sequence.count("T")),
        ("G", sequence.count("G")),
        ("C", sequence.count("C"))
    ])
    
    return d

X = DNA_nucleotide_count(sequence)
X_label = list(X)
X_values = list(X.values())

X

st.subheader("2. Print text")
st.write(f"There are {X['A']} adeninde (A)")
st.write(f"There are {X['T']} thymine (T)")
st.write(f"There are {X['G']} guanine (G)")
st.write(f"There are {X['C']} cytosine (C)")

st.subheader("3. Print dataframe")
df = pd.DataFrame.from_dict(X, orient="index")
df = df.rename({0: "Count"}, axis="columns")
df.reset_index(inplace=True)
df = df.rename(columns={"index": "Nucleotide"})
st.write(df)

st.subheader("4. Display bar chart")
chart = alt.Chart(df).mark_bar().encode(
    x="Nucleotide",
    y="Count"
).properties(
    width=alt.Step(80)
)
st.write(chart)