from itertools import chain, combinations

def getAttributeClosure(X, FDS):
  '''
  Computes the attribute closure given a set of attribute and functional dependencies.
  X  : key attributes
  FDS: list of functional dependencies
  '''
  retval = set(X)
  
  breaks = False

  while not breaks:
    breaks = True
    for fd in FDS:
      lhs = fd[0]
      rhs = fd[1]

      if lhs.issubset(retval) and not rhs.issubset(retval):
        breaks = False
        retval.update(rhs)

  return retval


# Getting super keys

def getSuperKeys(R, FDS):
  
  s = list(R)
  subsets = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

  supers = []

  for subset in subsets:
    closure = getAttributeClosure(set(subset), FDS)
    if closure == R:
      supers.append( set(subset) )

  return supers


def getCandidateKeys(R, FDS):
  '''
  Computes the candidate keys, given a relation and functional dependencies.
  '''
  # Try every subset of R as the key, and find the shortest one
  s = list(R)
# print(s)

  subsets = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
 
  best_length = len(R)

  # print(best_length)

  candidates = []

  for subset in subsets:
    
    #print(subset)
    
    closure = getAttributeClosure(set(subset), FDS)
    if closure == R and len(subset) < best_length:
      candidates = [set(subset)]
      best_length = len(subset)
    elif closure == R and len(subset) == best_length:
      candidates.append(set(subset))

  # print(closure)
  # print(candidates)


  return candidates



def getPrimeAttributes(R, FDS):
  '''
  Computes the prime attributes, given a relation and functional dependencies
  '''
  retset = set([])

  candidates = getCandidateKeys(R, FDS)

  # print(candidates)

  for key in candidates:
    for a in key:
      retset.add( a )

  # print(retset)

  return retset



def getNonPrimeAttributes(R, FDS):
  '''
  Computes the non prime attributes, given a relation and functional dependencies
  '''
  primes = getPrimeAttributes(R, FDS)

  # print(primes)

  return set(R) - set(primes)


def is2NF(R, FDS):
  '''
  Checks if a relation is in 2NF
  Relation schema R is in 2NF if it is in 1NF and it does not have any 
  non-prime attributes that are functionally dependent on a part of a 
  candidate key
  '''

  candidates = getCandidateKeys(R, FDS)
  primes = getPrimeAttributes(R, FDS)
  non_primes = getNonPrimeAttributes(R, FDS)
  
  
  # print(candidates)
  # print(primes)
  # print(non_primes)


  for FD in FDS:
    rhs = FD[1]
    lhs = FD[0]

    # We're only interesting in parts of candidate keys
    if lhs in candidates or len(lhs & non_primes):
      continue

    for att in non_primes:
      if att in rhs:
        print("\t", lhs, "->", rhs, "breaks 2NF requirements (", att, "is non-prime )")
        return False

  return True

def is3NF(R, FDS):
  '''
  Checks if a relation is in 3NF
  '''
  
  superkeys  = getSuperKeys(R, FDS)
  primes     = getPrimeAttributes(R, FDS)
  non_primes = getNonPrimeAttributes(R, FDS)


  # print(superkeys)
  # print(primes)
  # print(non_primes)
  
  
  for FD in FDS:
    rhs = FD[1]
    lhs = FD[0]

    if lhs in superkeys:
      continue

    for att in non_primes:
      if att in rhs:
        print("\t", lhs, "->", rhs, "breaks 3NF requirements (", att, "is non-prime )")
        return False

  return True


# Checks if a relation is in BCNF

def isBCNF(R, FDS):

  superkeys = getSuperKeys(R, FDS)
  # print(superkeys)
  for FD in FDS:
    rhs = FD[1]
    lhs = FD[0]
    # print(lhs)
    # print(rhs)
    if lhs not in superkeys:
      print("\t", lhs, "->", rhs, "breaks BCNF requirements (", lhs, "is non-superkey )")
      return False

  return True


def doChecks(name, R, FDS):

  print("***********************************")
  print("\t Table Name ",name)
  print("***********************************")

  # Calculate candidate keys
  candidate_keys = getCandidateKeys(R, FDS)
  print("Candidate keys:")
  for key in candidate_keys:
    print("\t", key)
  print("")

  # Calculate prime attributes
  prime_attributes = getPrimeAttributes(R, FDS)
  print("Prime attributes:\n\t", prime_attributes)
  print("")

  non_prime_attributes = getNonPrimeAttributes(R, FDS)
  print("Non-prime attributes:\n\t", non_prime_attributes)
  print("")


  
  # Check if the relation is normalized
  
  print("===================================================")
  print("The Normalization status of our input relation is : ")
  print("===================================================")
  print("")
  print("Here we have already assumed that our relation is already in 1st Normal form, i.e. 1NF.")
  print("")

  print("2NF status :")
  is_2NF = is2NF(R, FDS)
  if is_2NF:
    print("\tThe relation is in 2NF")
  print("")

  print("3NF status :")
  is_3NF = is3NF(R, FDS)
  if is_3NF:
    print("\tThe relation is in 3NF")
  print("") 

  print("BCNF status :")
  is_BCNF = isBCNF(R, FDS)
  if is_BCNF:
    print("\tThe relation is in BCNF")
  print("") 


def main():
  lines = []
  with open("input 4.txt") as f:
      for i in range(3):
          line = f.readline().removesuffix("\n")
          lines.append(line)
 
  print("The input files contain the following information about our relation : ")
  print("")      
  # print(lines)
  
  name = ""
  R = -1  
  FDS = []
  
  for line in lines:
    
    # If we've found a new relation, do the calculations for the old one
    if line.find('(') != -1:

      if R != -1:
        doChecks(name, R, FDS)

 #     print("1. Line Prints: ")
#      print(line,R)  
      # Reset the relation and the FDs
      # print(line)
      name = line[:line.find('(')]
      # print(line)
      line = line[ line.find('(')+1 : line.find(')') ]
      R = set( [ x.strip() for x in line.split(',')] )
      # print(R)
      # print(line)
      # print(name)
      FDS = []
      
  #    print("2. Line Prints: ")
 #     print(line,R) 
      continue

    lhs = line.split('->')[0]
    # print(line)
    # print(lhs)
    rhs = line.split('->')[1]
    # print(rhs)
    lhs = set([ x.strip() for x in lhs.split(',')])
    rhs = set([ x.strip() for x in rhs.split(',')])
  
    FD = (lhs, rhs)
    # print("FD : ")
    # print(FD)
    FDS.append( FD )
    
    
  # Do the calculations for the last relation
#  print("R Prints: ")
 # print(line)
  
  if R != -1:
    print("The attributes of our relation are : ")
    print(R)
    print("")
    print("The list of Functional dependencies are : ")
    print(FDS)
    print("")
    
    
    doChecks(name, R, FDS)
  


if __name__ == "__main__":
  main()
