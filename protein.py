import os
class Protein():
  def __init__(self, path):
    self.path = path
    folder = self.path.split('.pdb')[0]
    if not os.path.isdir(folder):
      os.mkdir(folder)
    self.lines = self.get_lines()
    self.sequence = self.get_sequence()
    self.seq_path = self.make_fasta()
    
  def get_lines(self):
    with open(self.path, 'r') as f:
      all_lines = f.readlines()
    return [f.split() for f in all_lines if f.startswith("ATOM")]
  
  def get_sequence(self):
    sequence_dict = {}
    for line in self.lines:
      sequence_dict.setdefault(line[5], self.three_to_one(line[3]))
    return sequence_dict

  def three_to_one(self, three_letter_code):
    '''converts any three letter code to a one letter code'''
    mapping = {'Ala':'A',
              'Arg':'R',
              'Asn':'N',
              'Asp':'D',
              'Cys':'C',
              'Gln':'Q',
              'Glu':'E',
              'Gly':'G',
              'His':'H',
              'Ile':'I',
              'Leu':'L',
              'Lys':'K',
              'Met':'M',
              'Phe':'F',
              'Pro':'P',
              'Ser':'S',
              'Thr':'T',
              'Trp':'W',
              'Tyr':'Y',
              'Val':'V',}
    
    if len(three_letter_code) != 3: # What does this mean? Why are these residues denoted as AARG instead of ARG?
      if three_letter_code[1:].lower() in [i.lower() for i in mapping.keys()]:
        print(f"    WARNING: truncating {three_letter_code} to {three_letter_code[1:]}")
        three_letter_code = three_letter_code[1:]
      else:
        print(f"    WARNING: {three_letter_code} was not found in function three_to_one map")
    return mapping[three_letter_code[0].upper() + three_letter_code[1:].lower()]

  def make_fasta(self):
    fasta_dest = os.path.join(self.path.split('.pdb')[0], os.path.basename(self.path).split('.pdb')[0]+'.fasta')
    fasta =  '>' + os.path.basename(self.path).split('.pdb')[0] + '\n' + ''.join(self.sequence.values())
    with open(fasta_dest, 'w') as f:
      f.write(fasta)
    print('wrote fasta')
    self.sequence
    return fasta_dest
