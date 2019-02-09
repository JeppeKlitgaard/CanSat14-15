import re
import os

pattern = re.compile(r"\nEnd of pic\n\n(\d+)\nStart pic\n(FFD8.+?FFD9)",
                     re.DOTALL | re.MULTILINE)


def read_file(filepath):
    """
    Returns a sequence of byte objects.
    """
    f = open(filepath, "r")

    data_content = f.read()

    image_matches = pattern.findall(data_content)

    objs = []

    for (time, image) in image_matches:
        image = image.replace("\n", "")  # remove newlines
        objs.append([time, bytes.fromhex(image)])

    return objs


def read_dir(filepath):
    files = os.listdir(filepath)

    objs = []

    for f in files:
        try:
            f = os.path.join(filepath, f)
            objs.append(read_file(f))
        except (UnicodeDecodeError, ValueError):
            pass

    for (byte_obj_m, i) in zip(objs, range(len(objs))):

        for (byte_obj_i, ii) in zip(byte_obj_m, range(len(byte_obj_m))):

            with open("img_batch{}_image{}___time{}.jpg".format(str(i), str(ii), str(byte_obj_i[0])), "wb") as f_out:
                f_out.write(byte_obj_i[1])
