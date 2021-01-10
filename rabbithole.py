# Mark functions with their cumulative cyclomatic complexity
#@author buherator
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.program.util import CyclomaticComplexity
from ghidra.util.task import TaskMonitor
from ghidra.program.model.symbol import SourceType
from docking.widgets import OptionDialog

CYCLO_MAP = {}
CCs = []
cyclomaticComplexity = CyclomaticComplexity();

def recurse_cyclo(func, visited = set()):
    entry=func.getEntryPoint().getOffset()

    # Avoid loops
    if entry in visited:
        return 0
    else:
        visited.add(entry)

    # Use the cache
    if (entry in CYCLO_MAP):
        return CYCLO_MAP[entry]

    cc = cyclomaticComplexity.calculateCyclomaticComplexity(func, TaskMonitor.DUMMY)
    for f in func.getCalledFunctions(TaskMonitor.DUMMY):
        cc += recurse_cyclo(f, visited)
    
    CYCLO_MAP[entry] = cc

    return cc

func = getFirstFunction()

userDialog=OptionDialog.showOptionDialog(None, "Rabbit Hole", "Hello Alice! \nDo you want your functions renamed?", "Yes", "No")

if userDialog == 0:
    exit()

while func is not None:
    cc = recurse_cyclo(func)
    CCs.append(cc)
    if userDialog == 1:
        func.setName("%s_cc%d" % (func.getName(), cc), SourceType.USER_DEFINED)
    func=getFunctionAfter(func)

print("Rabbit Hole statistics:")
print("Average CC: %f " % (sum(CCs)/len(CCs)))
print("Median CC: %d" % (CCs[int(len(CCs)/2)]))