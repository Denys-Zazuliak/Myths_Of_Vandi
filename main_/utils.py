import json

def rect_collision(rect1, rect2):
    if rect1.right >= rect2.left and rect1.left <= rect2.right and rect1.bottom >= rect2.top and rect1.top <= rect2.bottom:
        colliding = True
    else:
        colliding = False

    return colliding


def point_collision(point_pos, rect):
    if point_pos[0] >= rect.left and point_pos[0] <= rect.right and point_pos[1] >= rect.top and point_pos[
        1] <= rect.bottom:
        colliding = True
    else:
        colliding = False
    return colliding


def read_json(file):
    file = file + ".json"
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def write_json(data, file):
    file = file + '.json'
    with open(file, 'w') as json_file:
        json.dump(data, json_file, indent=2, separators=(", ", " : "), sort_keys=True)
    return file

