# dialog.py
# This program runs a dialog between two agents, which must be defined
# elsewhere as separate modules.

import Musician as agentA
import ghirme as agentB

N_TURNS = 30

turn = 0
print(str(turn)+"A: "+agentA.agentName() + ': ' + agentA.introduce()+"\n")
print(str(turn)+"B: "+agentB.agentName() + ': ' + agentB.introduce()+"\n")
remark = agentB.introduce()
for i in range(N_TURNS):
    turn += 1
    remark = agentA.respond(remark)
    print(str(turn)+"A: "+agentA.agentName() + ': ' + remark+"\n")
    remark = agentB.respond(remark)
    print(str(turn)+"B: "+agentB.agentName() + ': ' + remark+"\n")
