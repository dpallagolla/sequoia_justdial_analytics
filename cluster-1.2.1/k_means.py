#! /usr/bin/env python
from cluster import KMeansClustering
import json 

f_categories = open("cat_less.txt", "r").read()
f_json = open("data_less.txt", "r").read()

json_data = json.loads(f_json)

categories = f_categories.split("\n")
k_means_list = []


# category = "Advertising Agencies"
for category in categories:
	try:
		if(json_data[category]):	
			for cat in json_data[category]:
				v = cat["latlon"]
				k_means_list.append((float(v.split(",")[0]), float(v.split(",")[1])))

			cl = KMeansClustering(k_means_list)
			clusters = cl.getclusters(12)
			# print category
			# print clusters
			cluster_file = open("./Output/" + category, "w")
			for cluster in clusters:
				for tup in cluster:
					# print tup[0]
					cluster_file.write(str(tup[0]) + "," + str(tup[1]) + " ")
				cluster_file.write("\n")
			print category + " Done"
			cluster_file.close()
	except Exception as e:
		pass