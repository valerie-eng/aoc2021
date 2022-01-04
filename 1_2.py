fin = open('input.txt', 'r')

# Number of times it increased.
count = 0
currSum = 0
prevSum = -1
prev1 = -1
prev2 = -1

i = 0
while True:
  line = fin.readline().strip()
  if line == '':
    break
  n = int(line)
  currSum = n + prev1 + prev2

  # Start checking after 4 numbers.
  if i > 2:
    if currSum > prevSum:
      count += 1

  prev2 = prev1
  prev1 = n
  prevSum = currSum

  i += 1

print(count)
