# Mark functions with their cumulative cyclomatic complexity
#@author buherator
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 

from ghidra.program.util import CyclomaticComplexity
from ghidra.util.task import TaskMonitor
from ghidra.program.model.symbol import SourceType
# from docking.widgets import OptionDialog

CYCLO_MAP={}
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

#userDialog=OptionDialog.showOptionDialog(None, "Rabbit Hole", "Hello Alice! \nHow do you want your numbers served?", "Part of function name", "Comment")

#if userDialog == 0:
#    exit()

while func is not None:
    cc = recurse_cyclo(func)
    func.setName("%s_cc%d" % (func.getName(), cc), SourceType.USER_DEFINED)
    func=getFunctionAfter(func)