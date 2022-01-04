fin = open('input.txt', 'r')

readings = []
scannerReadings = []

while True:
  line = fin.readline()
  if line == '' or line == '\n':
    if len(scannerReadings) > 0:
      readings.append(scannerReadings)
    scannerReadings = []
    if line == '':
      # End of file.
      break
  elif line.startswith('---'):
    continue
  else:
    coords = tuple(map(lambda x: int(x), line.strip().split(',')))
    scannerReadings.append(coords)

S = len(readings)
# Whether a scanner successfully overlaps a known scanner.
known = [False] * S
# Set of beacons in scanner 0's frame of reference.
beaconSet = set()
# Set of known scanners to be used as a reference.
tempRefScannerSet = set()
# Coordinates of the scanners.
scannerCoords = [(0, 0, 0)] * S

# Mark scanner 0 as known and add to tempRefSet.
known[0] = True
tempRefScannerSet.add(0)
numKnown = 1
# Add beacons from scanner 0 into beaconSet.
for beacon in readings[0]:
  beaconSet.add(beacon)

# Returns point after 2D rotation.
def rotate(point, rotation):
  if rotation == 0:
    return point
  elif rotation == 1:
    return (-point[2], point[1], point[0])
  elif rotation == 2:
    return (-point[0], point[1], -point[2])
  else:
    return (point[2], point[1], -point[0])

# Returns point after orientation (6 faces and 4 rotations).
def orient(point, orientation):
  face = orientation // 4
  rotation = orientation % 4
  px = point[0]
  py = point[1]
  pz = point[2]
  if face == 0:
    (ox, oy, oz) = rotate((px, py, pz), rotation)
  elif face == 1:
    (ox, oy, oz) = rotate((-py, px, pz), rotation)
  elif face == 2:
    (ox, oy, oz) = rotate((-px, -py, pz), rotation)
  elif face == 3:
    (ox, oy, oz) = rotate((py, -px, pz), rotation)
  elif face == 4:
    (ox, oy, oz) = rotate((px, pz, -py), rotation)
  elif face == 5:
    (ox, oy, oz) = rotate((px, -pz, py), rotation)
  return (ox, oy, oz)

# Returns (overlap, dx, dy, dz, orientation).
def checkOverlap(refScanner, otherScanner):
  for i in range(len(refScanner)):
    for j in range(len(otherScanner)):
      for o in range(24):

        newCoords = orient(otherScanner[j], o)

        # Calculate offset.
        dx = newCoords[0] - refScanner[i][0]
        dy = newCoords[1] - refScanner[i][1]
        dz = newCoords[2] - refScanner[i][2]

        # Apply offset and count matching beacons.
        matchCount = 0
        for c in range(len(otherScanner)):
          n = orient(otherScanner[c], o)
          nx = n[0] - dx
          ny = n[1] - dy
          nz = n[2] - dz
        
          if (nx, ny, nz) in refScanner:
            # We got a match.
            matchCount += 1
            if matchCount == 12:
              return (True, dx, dy, dz, o)

  # We didn't find enough matches.
  return (False, 0, 0, 0, 0)

# Adds beacons after orientation and offset.
# Returns converted beacons.
def addBeacons(scanner, dx, dy, dz, orientation):
  global beaconSet
  converted = []
  for b in scanner:
    n = orient(b, orientation)
    nx = n[0] - dx
    ny = n[1] - dy
    nz = n[2] - dz
    beaconSet.add((nx, ny, nz))
    converted.append((nx, ny, nz))
  return converted

# Check unknown scanners for overlap with known scanners.
while True:
  # Select a scanner to be used as a reference.
  refScanner = tempRefScannerSet.pop()
  for i in range(S):
    # Don't compare the same scanner.
    if i == refScanner:
      continue
    # Skip if the scanner is already known.
    if known[i]:
      continue
    
    print('Comparing', i, 'to', refScanner)
    r = checkOverlap(readings[refScanner], readings[i])
    if not r[0]:
      continue

    # Found overlap.
    print('Found overlap')
    # Add converted beacons.
    convertedReadings = addBeacons(readings[i], r[1], r[2], r[3], r[4])
    # Replace scanner's readings with converted readings.
    readings[i] = convertedReadings
    # Scanner is known.
    known[i] = True
    numKnown += 1
    # Add so it can be used as a reference later.
    tempRefScannerSet.add(i)

    # Scanner position is opposite of offset.
    scannerCoords[i] = (-r[1], -r[2], -r[3])

    # Check if all scanners are known.
    if numKnown == S:
      break
  if numKnown == S:
    break

# Find max distance between all scanners.
maxD = 0
for i in range(S):
  for j in range(i+1, S):
    distance = abs(scannerCoords[i][0] - scannerCoords[j][0]) + abs(scannerCoords[i][1] - scannerCoords[j][1]) + abs(scannerCoords[i][2] - scannerCoords[j][2])
    if distance > maxD:
      maxD = distance

print('Number of beacons:', len(beaconSet))
print('Max distance:', maxD)
