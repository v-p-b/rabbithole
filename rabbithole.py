# Mark functions with their cumulative cyclomatic complexity
#@author buherator
#@category CultOfDragon
#@keybinding 
#@menupath 
#@toolbar 
#@runtime PyGhidra

from ghidra.program.util import CyclomaticComplexity
from ghidra.util.task import TaskMonitor
from ghidra.program.model.symbol import SourceType
from docking.widgets import OptionDialog
from ghidra.app.tablechooser import TableChooserExecutor, AddressableRowObject, ColumnDisplay
from jpype import JImplements, JOverride
from java.lang import String, Integer

CYCLO_MAP = {}
CCs = []
cyclomaticComplexity = CyclomaticComplexity();

@JImplements(TableChooserExecutor)
class RabbitHoleExecutor:
    @JOverride
    def execute(self, rowObject):
        self.lastRowExecuted = rowObject
        return True

    @JOverride
    def getButtonName(self):
        return "I'm late!"

@JImplements(AddressableRowObject)
class RabbitHoleRow():
    def __init__(self, func, cc):
        self.function = func
        #self.address = self.function.getEntryPoint()
        self.cc = cc

    @JOverride
    def getAddress(self):
        return self.function.getEntryPoint()

    @JOverride
    def getCycloComplexity(self):
        return self.cc

    @JOverride
    def getName(self):
        return self.function.getName()

@JImplements(ColumnDisplay)
class RabbitHoleCCColumn():

    @JOverride
    def getColumnValue(self,rowObj):
        return rowObj.getCycloComplexity()

    @JOverride
    def getColumnName(self):
        return "Cumulative Complexity"  

    @JOverride
    def getColumnClass(self):
        return Integer

    @JOverride
    def compare(self, r1, r2):
        c1 = r1.getCycloComplexity()
        c2 = r2.getCycloComplexity()
        return c1-c2

    @JOverride
    def equals(self, other):
        return self.compare(self, other) == 0


@JImplements(ColumnDisplay)
class RabbitHoleNameColumn():

    @JOverride
    def getColumnValue(self,rowObj):
        return rowObj.getName()

    @JOverride
    def getColumnName(self):
        return "Function name"  

    @JOverride
    def getColumnClass(self):
        return String

    @JOverride
    def compare(self, r1, r2):
        n1 = r1.getName()
        n2 = r2.getName()
        if n1 < n2:
            return -1
        elif n2 > n1: 
            return 1
        else:
            return 0

    @JOverride
    def equals(self, other):
        return self.compare(self, other) == 0

def recurse_cyclo(func, visited):
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

tableDialog=createTableChooserDialog("Rabbit Hole", RabbitHoleExecutor())
tableDialog.addCustomColumn(RabbitHoleNameColumn())
tableDialog.addCustomColumn(RabbitHoleCCColumn())

while func is not None:
    cc = recurse_cyclo(func,set())
    CCs.append(cc)
    print("%s\t%d" % (func.getName(), cc))
    tableDialog.add(RabbitHoleRow(func, cc))
    if userDialog == 1:
        func.setName("%s_cc%d" % (func.getName(), cc), SourceType.USER_DEFINED)
    func=getFunctionAfter(func)

tableDialog.show()

print("Rabbit Hole statistics:")
print("Average CC: %f " % (sum(CCs)/len(CCs)))
print("Median CC: %d" % (CCs[int(len(CCs)/2)]))
