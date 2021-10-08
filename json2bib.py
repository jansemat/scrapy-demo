import os
import sys
import json
from string import Template

# requirement: convert from JSON to bibtex
def req_3(json_obj):
	bib_obj = "@article{\n"
	bib_obj += Template("  Title={$val}").substitute(val=json_obj["content"]["Title"])
	for author in json_obj["content"]["Authors"]:
		bib_obj += Template("  Author={$val}\n").substitute(val=author)

	bib_obj += Template("  URL={$val}\n").substitute(val=json_obj["content"]["DOI"])

	keywords = ";".join(json_obj["content"]["Keywords"]) + ";" + str(json_obj["count"])
	bib_obj += Template("  Keywords={$val}\n").substitute(val=keywords)

	bib_obj += "}\n"

	return bib_obj

# requirement: add search terms + number of occurances as keywords to each article
def req_2(global_list, article):
	doi_key = article['DOI']
	if doi_key in global_list:
		global_list[doi_key]['count'] += 1
		global_list[doi_key]['content']['Keywords'] += article['Keywords']
	else:
		global_list[doi_key] = {'content': article, 'count': 1}


# requirement: deduplicate results from all files
def req_1(files_dir):
	global_list = {}
	current_file = ""

	try:
		files_list = [files_dir + "/" + file_str for file_str in os.listdir(files_dir)]

		for file in files_list:
			current_file = file
			with open(file, "r") as fd:
				file_content = json.load(fd)

			for article in file_content:
				req_2(global_list, article)

	except:
		sys.exit("[Error] Error opening input directory, '" + current_file + "'")

	return global_list


def main():
	if len(sys.argv) != 2:
		sys.exit("[Error] Not enough args\n")
	files_dir = sys.argv[1]

	if files_dir[-1] == "/":
		files_dir = files_dir[:-1]

	global_list = req_1(files_dir)
	filename = "all.bib"
	with open(filename, "w") as fd:
		for doi_key in global_list:
			json_obj = global_list[doi_key]
			bib_obj = req_3(json_obj)
			_ = fd.write(bib_obj + "\n")

	return

if __name__ == "__main__":
	main()
