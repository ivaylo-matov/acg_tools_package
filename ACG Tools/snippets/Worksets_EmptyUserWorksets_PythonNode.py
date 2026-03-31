import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ElementWorksetFilter
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import FilteredWorksetCollector
from Autodesk.Revit.DB import WorksetKind

clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager


doc = DocumentManager.Instance.CurrentDBDocument

# Collect only user-created worksets.
user_worksets = list(
    FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
)

empty_worksets = []

for ws in user_worksets:
    # Count only placed element instances (exclude element types).
    instance_count = (
        FilteredElementCollector(doc)
        .WherePasses(ElementWorksetFilter(ws.Id, False))
        .WhereElementIsNotElementType()
        .GetElementCount()
    )

    if instance_count == 0:
        empty_worksets.append(ws)

# OUT returns Revit Workset objects that contain no element instances.
OUT = empty_worksets
