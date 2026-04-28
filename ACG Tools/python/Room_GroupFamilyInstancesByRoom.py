# Dynamo Python node inputs:
# IN[0] = list of family instances
# IN[1] = list of room instances
#
# Output:
# OUT[0] = list of rooms that contain one or more furniture instances
# OUT[1] = 2D list of furniture instances, aligned with OUT[0]
# OUT[2] = list of rooms that do not contain any input furniture instances,
#          excluding room numbers already present in OUT[0]

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


furniture_instances = as_list(IN[0])
rooms = as_list(IN[1])

# Keep the original Dynamo-wrapped elements in the output values.
instances = []
for wrapped_instance in furniture_instances:
    revit_instance = UnwrapElement(wrapped_instance)
    if revit_instance is not None:
        instances.append((wrapped_instance, revit_instance))

room_pairs = []
for wrapped_room in rooms:
    revit_room = UnwrapElement(wrapped_room)
    if revit_room is not None:
        room_pairs.append((wrapped_room, revit_room))

furniture_by_room = [[] for room_pair in room_pairs]

for wrapped_instance, revit_instance in instances:
    point = get_location_point(revit_instance)
    if point is None:
        continue

    for index, room_pair in enumerate(room_pairs):
        room = room_pair[1]
        if room.IsPointInRoom(point):
            furniture_by_room[index].append(wrapped_instance)
            break

rooms_with_furniture = []
furniture_in_rooms = []
rooms_without_furniture = []
room_numbers_with_furniture = set()

for index, room_pair in enumerate(room_pairs):
    wrapped_room = room_pair[0]
    revit_room = room_pair[1]
    room_furniture = furniture_by_room[index]

    if room_furniture:
        rooms_with_furniture.append(wrapped_room)
        furniture_in_rooms.append(room_furniture)
        room_numbers_with_furniture.add(revit_room.Number)

for index, room_pair in enumerate(room_pairs):
    wrapped_room = room_pair[0]
    revit_room = room_pair[1]
    room_furniture = furniture_by_room[index]

    if not room_furniture and revit_room.Number not in room_numbers_with_furniture:
        rooms_without_furniture.append(wrapped_room)

OUT = rooms_with_furniture, furniture_in_rooms, rooms_without_furniture
