class Protein():
  def __init__(self, path):
    self.path = path
    self.lines = self.get_lines()
    self.sequence = self.get_sequence()
    
  def get_lines(self):
    with open(self.path, 'r') as f:
      all_lines = f.readlines()
    return [f.split() for f in all_lines if f.startswith("ATOM")]
  
  def get_sequence(self):
    sequence_dict = {}
    for line in self.lines:
      sequence_dict.setdefault(line[5], line[3])
      return sequence_dict
