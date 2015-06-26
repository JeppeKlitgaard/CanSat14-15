import re
import os

pattern = re.compile(r"(FFD8.+?FFD9)", re.DOTALL | re.MULTILINE)


def read_file(filepath):
    """
    Returns a sequence of byte objects.
    """
    f = open(filepath, "r")

    data_content = f.read()

    image_matches = pattern.findall(data_content)

    byte_objs = []

    for image in image_matches:
        image = image.replace("\n", "")  # remove newlines
        byte_objs.append(bytes.fromhex(image))

    return byte_objs


def read_dir(filepath):
    files = os.listdir(filepath)

    byte_objs = []

    for f in files:
        try:
            f = os.path.join(filepath, f)
            byte_objs.append(read_file(f))
        except (UnicodeDecodeError, ValueError):
            pass

    for byte_obj_m, i in zip(byte_objs, range(len(byte_objs))):
        for byte_obj_i, ii in zip(byte_obj_m, range(len(byte_obj_m))):
            with open("img_batch{}_image{}.jpg".format(str(i), str(ii)), "wb") as f_out:
                f_out.write(byte_obj_i)
