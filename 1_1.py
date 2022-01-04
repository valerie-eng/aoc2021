fin = open('input.txt', 'r')

# Number of times it increased.
count = 0
prev = -1

while True:
  line = fin.readline().strip()
  if line == '':
    break
  N = int(line)
  if prev != -1 and N > prev:
    count += 1
  prev = N

print(count)
