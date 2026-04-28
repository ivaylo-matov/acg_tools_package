# Dynamo Python node inputs:
# IN[0] = list of family instances
# IN[1] = list of room instances
#
# Output:
# Dictionary where each key is a room number and each value is the list of
# input family instances whose LocationPoint is inside that room.

import clr

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import LocationPoint

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_location_point(element):
    if element is None or element.Location is None:
        return None

    location = element.Location
    if isinstance(location, LocationPoint):
        return location.Point

    return None


family_instances = as_list(IN[0])
rooms = as_list(IN[1])

# Keep the original Dynamo-wrapped family instances in the result values.
instances = []
for wrapped_instance in family_instances:
    revit_instance = UnwrapElement(wrapped_instance)
    if revit_instance is not None:
        instances.append((wrapped_instance, revit_instance))

revit_rooms = []
for room in rooms:
    revit_room = UnwrapElement(room)
    if revit_room is not None:
        revit_rooms.append(revit_room)

result = {}

for wrapped_instance, revit_instance in instances:
    point = get_location_point(revit_instance)
    if point is None:
        continue

    for room in revit_rooms:
        if room.IsPointInRoom(point):
            room_number = room.Number
            if room_number not in result:
                result[room_number] = []

            result[room_number].append(wrapped_instance)
            break

OUT = result
