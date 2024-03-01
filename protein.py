import os
class Protein():
  def __init__(self, original_location):
    self.folder = original_location.split('.pdb')[0]
    if not os.path.isdir(self.folder):
      os.mkdir(self.folder)
    new_location = os.path.join(self.folder, os.path.basename(original_location))
    os.rename(original_location, new_location)
    self.path = new_location
    self.sequence = self.get_sequence()
    
  def get_lines(self):
    with open(self.path, 'r') as f:
      all_lines = f.readlines()
    return [f.split() for f in all_lines if f.startswith("ATOM")]
  
  def get_sequence(self):
    with open(self.path, 'r') as f:
      all_lines = f.readlines()
    lines = [f.split() for f in all_lines if f.startswith("ATOM")]
    sequence_dict = {}
    for line in lines:
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
