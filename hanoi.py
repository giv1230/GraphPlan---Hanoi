def createDomainFile(domainFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  domainFile = open(domainFileName, 'w') #use domainFile.write(str) to write to domainFile
  buff = ''

  # propositions
  buff += 'Propositions:\n'
  for p in pegs:
    buff += 'clear_{} '.format(p)
    for disk in range(n):
      buff += "disk_{}_on_peg_{} ".format(disk, p)
      buff += "disk_{}_on_top_{} ".format(disk, p)
      buff += "disk_{}_on_bottom_{} ".format(disk, p)

  for disk1 in range(n):
    for disk2 in range(n):
      if disk1 < disk2:
        buff += "disk_{}_on_disk_{} ".format(disk1, disk2)
  buff += "\n"

  # actions
  buff += 'Actions:\n'
  
  for peg_src in pegs:
    for peg_dst in pegs:
      for disk1 in range(n):
        for disk2 in range(n):
          if peg_src != peg_dst:
            # move last disk from peg to a empty peg
            buff += "Name: move_last_disk_{}_on_peg_{}_to_empty_peg_{} \n".format(disk1, peg_src, peg_dst)

            buff += "pre: "
            buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
            buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
            buff += "disk_{}_on_bottom_{} ".format(disk1, peg_src)
            buff += "clear_{} ".format(peg_dst)
            buff += "\n"

            buff += "add: "
            buff += "disk_{}_on_peg_{} ".format(disk1, peg_dst)
            buff += "disk_{}_on_top_{} ".format(disk1, peg_dst)
            buff += "disk_{}_on_bottom_{} ".format(disk1, peg_dst)
            buff += "clear_{} ".format(peg_src)
            buff += "\n"

            buff += "delete: "
            buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
            buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
            buff += "disk_{}_on_bottom_{} ".format(disk1, peg_src)
            buff += "clear_{} ".format(peg_dst)
            buff += "\n"

            if disk1 < disk2:
              #  move disk to empty peg
              buff += "Name: move_disk_{}_from_disk_{}_on_peg_{}_to_empty_peg_{}\n".format(disk1, disk2, peg_src, peg_dst)

              buff += "pre: "
              buff += "disk_{}_on_disk_{} ".format(disk1, disk2)
              buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_peg_{} ".format(disk2, peg_src)
              buff += "clear_{} ".format(peg_dst)
              buff += "\n"

              buff += "add: "
              buff += "disk_{}_on_peg_{} ".format(disk1, peg_dst)
              buff += "disk_{}_on_top_{} ".format(disk1, peg_dst)
              buff += "disk_{}_on_bottom_{} ".format(disk1, peg_dst)
              buff += "disk_{}_on_top_{} ".format(disk2, peg_src)
              buff += "\n"

              buff += "delete: "
              buff += "disk_{}_on_disk_{} ".format(disk1, disk2)
              buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
              buff += "clear_{} ".format(peg_dst)
              buff += "\n"

              # move last disk from peg to a non-empty peg
              buff += "Name: move_last_disk_{}_on_peg_{}_to_disk_{}_on_peg_{} \n".format(disk1, peg_src, disk2, peg_dst)

              buff += "pre: "
              buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_bottom_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_peg_{} ".format(disk2, peg_dst)
              buff += "disk_{}_on_top_{} ".format(disk2, peg_dst)
              buff += "\n"

              buff += "add: "
              buff += "disk_{}_on_peg_{} ".format(disk1, peg_dst)
              buff += "disk_{}_on_top_{} ".format(disk1, peg_dst)
              buff += "disk_{}_on_disk_{} ".format(disk1, disk2)
              buff += "clear_{} ".format(peg_src)
              buff += "\n"

              buff += "delete: "
              buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_bottom_{} ".format(disk1, peg_src)
              buff += "disk_{}_on_top_{} ".format(disk2, peg_dst)
              buff += "\n"

              # move disk from non-empty peg to a non-empty peg
              for disk3 in range(n):
                if disk1 < disk3:
                  buff += "Name: move_disk_{}_from_disk_{}_on_peg_{}_to_disk_{}_on_peg_{}\n".format(disk1, disk2, peg_src, disk3, peg_dst)

                  buff += "pre: "
                  buff += "disk_{}_on_disk_{} ".format(disk1, disk2)
                  buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
                  buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
                  buff += "disk_{}_on_peg_{} ".format(disk2, peg_src)
                  buff += "disk_{}_on_top_{} ".format(disk3, peg_dst)
                  buff += "disk_{}_on_peg_{} ".format(disk3, peg_dst)
                  buff += "\n"

                  buff += "add: "
                  buff += "disk_{}_on_disk_{} ".format(disk1, disk3)
                  buff += "disk_{}_on_top_{} ".format(disk1, peg_dst)
                  buff += "disk_{}_on_peg_{} ".format(disk1, peg_dst)
                  buff += "disk_{}_on_top_{} ".format(disk2, peg_src)
                  buff += "\n"

                  buff += "delete: "
                  buff += "disk_{}_on_disk_{} ".format(disk1, disk2)
                  buff += "disk_{}_on_top_{} ".format(disk1, peg_src)
                  buff += "disk_{}_on_peg_{} ".format(disk1, peg_src)
                  buff += "disk_{}_on_top_{} ".format(disk3, peg_dst)
                  buff += "\n"
  
  domainFile.write(buff)
  domainFile.close()  
        
  
def createProblemFile(problemFileName, n):
  numbers = list(range(n)) # [0,...,n-1]
  pegs = ['a','b', 'c']
  problemFile = open(problemFileName, 'w') #use problemFile.write(str) to write to problemFile
  buff = ''
  
  ### Initial State ###
  buff += 'Initial state: '
  buff += 'clear_b '
  buff += 'clear_c '

  # disk 0 on top a
  buff += 'disk_0_on_top_a '

  # disks 0 to n-2
  for i in range(n-1):
    buff += 'disk_{}_on_peg_a '.format(i)
    buff += 'disk_{}_on_disk_{} '.format(i, i+1)

  # disk n-1
  buff += 'disk_{}_on_peg_a '.format(n-1)
  buff += 'disk_{}_on_bottom_a '.format(n-1)
  buff += "\n"


  ### Goal State ###
  buff += 'Goal state: '
  buff += 'clear_a '
  buff += 'clear_b '

  # disk 0 on top c
  buff += 'disk_0_on_top_c '

  # disks 0 to n-2
  for i in range(n-1):
    buff += "disk_{}_on_peg_c ".format(i)
    buff += "disk_{}_on_disk_{} ".format(i, i+1)

  # disk n-1
  buff += 'disk_{}_on_peg_c '.format(n-1)
  buff += 'disk_{}_on_bottom_c '.format(n-1)
  buff += "\n"
  
  problemFile.write(buff)
  problemFile.close()

import sys
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: hanoi.py n')
    sys.exit(2)
  
  n = int(float(sys.argv[1])) #number of disks
  domainFileName = 'hanoi' + str(n) + 'Domain.txt'
  problemFileName = 'hanoi' + str(n) + 'Problem.txt'
  
  createDomainFile(domainFileName, n)
  createProblemFile(problemFileName, n)