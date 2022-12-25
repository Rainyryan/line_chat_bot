from app import create_machine


machine=create_machine()

with open('fsm.png','bw') as f:
    machine.get_graph().draw(f, prog="dot", format="png")
print("done")