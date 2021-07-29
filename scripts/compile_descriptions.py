# Compiles all descriptions into a single .txt file for training language models
import json
import re

if __name__ == "__main__":
    file = open("../get_waifu/data/waifu_details.json", "r")
    buffer = ""
    details = json.loads(file.read())
    file.close()
    for obj in details:
        desc = obj['description']
        fullname = re.sub(r'".+"|\(.+\)|-.+', '', obj['name'])
        names = fullname.split(' ')
        # This is to ensure that our model does not learn the meaning of specific names.
        desc = desc.replace(fullname, '[FULLNAME]')
        firstname = names[0]
        print(firstname)
        desc = re.sub(firstname, '[FIRSTNAME]', desc)
        buffer += desc + "\n"
    descFile = open("../data/waifu_descriptions_normalized.txt", 'w')
    descFile.write(buffer)
    descFile.close()
