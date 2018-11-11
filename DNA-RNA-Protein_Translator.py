""" DNA-RNA-AAs Translation | 2018-11-11 Hwx """

# Input Your Target DNA Sequnce Here
Sequence = """GCTTATCTCTCTTGGCCCACCATTACGCAAATGGTGGTAGGTAGGTGAAGAACGGTGAGA"""


DNA = ["A", "T", "G", "C"]
RNA = ["A", "U", "G", "C"]

Codon_Table = {

    "GCU" : "Ala", "GCC" : "Ala", "GCA" : "Ala", "GCG" : "Ala",
    "CGU" : "Arg", "CGC" : "Arg", "CGA" : "Arg", "CGG" : "Arg", "AGA" : "Arg", "AGG" : "Arg",
    "AAU" : "Asn", "AAC" : "Asn",
    "GAU" : "Asp", "GAC" : "Asp",
    "UGU" : "Cys", "UGC" : "Cys",
    "CAA" : "Gln", "CAG" : "Gln", "GAA" : "Glu", "GAG" : "Glu", "GGU" : "Gly", "GGC" : "Gly", "GGA" : "Gly", "GGG" : "Gly",
    "CAU" : "His", "CAC" : "His",
    "AUU" : "Ile", "AUC" : "Ile", "AUA" : "Ile",
    "UUA" : "Leu", "UUG" : "Leu", "CUU" : "Leu", "CUC" : "Leu", "CUA" : "Leu", "CUG" : "Leu",
    "AAA" : "Lys", "AAG" : "Lys", "AUG" : "Met",
    "UUU" : "Phe", "UUC" : "Phe",
    "CCU" : "Pro", "CCC" : "Pro", "CCA" : "Pro", "CCG" : "Pro",
    "UCU" : "Ser", "UCC" : "Ser", "UCA" : "Ser", "UCG" : "Ser", "AGU" : "Ser", "AGC" : "Ser",
    "ACU" : "Thr", "ACC" : "Thr", "ACA" : "Thr","ACG" : "Thr",
    "UGG" : "Trp",
    "UAU" : "Tyr", "UAC" : "Tyr",
    "GUU" : "Val", "GUC" : "Val", "GUA" : "Val", "GUG" : "Val",

    "AUG" : "START=>",
    "UAA" : "<=STOP", "UGA" : "<=STOP", "UAG" : "<=STOP"

}

Notation_Table = {

    "Ala": "A",
    "Arg": "R",
    "Asn": "N",
    "Asp": "D",
    "Cys": "C",
    "Gln": "Q",
    "Glu": "E",
    "Gly": "G",
    "His": "H",
    "Ile": "I",

    "Leu": "L",
    "Lys": "K",
    "Met": "M",
    "Phe": "F",
    "Pro": "P",
    "Ser": "S",
    "Thr": "T",
    "Trp": "W",
    "Tyr": "Y",
    "Val": "V",

    "START=>" : "[S=>]",
    "<=STOP"  : "[<=S]",

}


# Convert DNA -> RNA
DNA_Sequence = ""
for Nucleotide in Sequence:
    if Nucleotide in DNA:
        DNA_Sequence += Nucleotide
    else:
        print("\nThis Is Not A Standard DNA Sequence.\n")
        exit()
print("DNA Sequence:", DNA_Sequence)

RNA_Sequence = ""
for Nucleotide in DNA_Sequence:
    if Nucleotide in RNA:
        pass
    elif Nucleotide == "T":
        Nucleotide = "U"
    RNA_Sequence += Nucleotide
print("RNA Sequence:", RNA_Sequence)


# Length of Nucleotide Sequence
RNA_Length = len(RNA_Sequence)
# codon_number = RNA_Length // 3

if RNA_Length % 3 == 0:
    print("Numbers of Codon in RNA Sequence:", RNA_Length // 3)
else:
    print("Numbers of Codon in RNA Sequence:", RNA_Length)


# Convert RNA -> Amino Acid (AA)
AA_Sequence = ""

for position in range(0, RNA_Length, 3):
    short_seq = RNA_Sequence[position : position + 3]
    if short_seq in Codon_Table:
        AA_Sequence += Codon_Table[short_seq] + " "
    else:
        AA_Sequence += "X" + " "
        print("There Is A Codon In RNA Sequnce Can Not Be Recognised:", short_seq, position, position + len(short_seq))
print("Amino Acid Sequence: ", AA_Sequence)


# Convert AA -> Notation AAS
AA_Notation_Sequnce = ""
for position in range(0, RNA_Length, 3):
    short_seq = RNA_Sequence[position : position + 3]
    if short_seq in Codon_Table:
        AA = Codon_Table[short_seq]
        Notation = Notation_Table[AA]
        AA_Notation_Sequnce += Notation
    else:
        AA_Sequence += "X" + " "
        print("There Is A Codon In RNA Sequnce Can Not Be Recognised:", short_seq, position, position + len(short_seq))
print("Notation Of Amino Acid Sequence: ", AA_Notation_Sequnce)




# Another Form Of Codon Table
codon_table = {

    "Ala" : ["GCU", "GCC", "GCA", "GCG"],
    "Arg" : ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "Asn" : ["AAU", "AAC"],
    "Asp" : ["GAU", "GAC"],
    "Cys" : ["UGU", "UGC"],
    "Gln" : ["CAA", "CAG"],
    "Glu" : ["GAA", "GAG"],
    "Gly" : ["GGU", "GGC", "GGA", "GGG"],
    "His" : ["CAU", "CAC"],
    "Ile" : ["AUU", "AUC", "AUA"],

    "Leu" : ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
    "Lys" : ["AAA", "AAG"],
    "Met" : ["AUG"],
    "Phe" : ["UUU", "UUC"],
    "Pro" : ["CCU", "CCC", "CCA", "CCG"],
    "Ser" : ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
    "Thr" : ["ACU", "ACC", "ACA", "ACG"],
    "Trp" : ["UGG"],
    "Tyr" : ["UAU", "UAC"],
    "Val" : ["GUU", "GUC", "GUA", "GUG"],

    "Start" : ["AUG"],
    "Stop"  : ["UAA", "UGA", "UAG"]

}
