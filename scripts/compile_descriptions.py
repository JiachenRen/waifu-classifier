# Compiles all descriptions into a single .txt file for training language models
import json

if __name__ == "__main__":
    file = open("../get_waifu/data/waifu_details.json", "r")
    buffer = ""
    details = json.loads(file.read())
    file.close()
    for obj in details:
        desc = obj['description']
        buffer += desc + "\n"
    descFile = open("../data/waifu_descriptions.txt", 'w')
    descFile.write(buffer)
    descFile.close()
