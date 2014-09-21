#! /usr/bin/env python

f_categories = open("cat_less.txt", "r").read()

categories = f_categories.split("\n")

var = "L.circle([%f, %f], 50, { color: %s, fillcolor: %s, fillOpacity: 0.3 }).addTo(map);"

color_code = ["00FF00", "2EFF00", "5CFF00", "8BFF00", "B9FF00", "E7FF00", "FFE700", "FFB900", "FF8B00", "FF5C00", "FF2E00", "FF0000"]

for category in categories:
	w = open("./Output/" + category + ".send", "w")
	rank = []
	rank_index = []
	rank_sort = []
	rank_loop = []
	# print category
	f = open("./Output/" + category, "r")
	least = []
	least_centroids = []
	for cluster in f:
		# print len(cluster.split())
		if(len(cluster) > 1):
			rank.append(len(cluster.split()))
	# 		rank_sort.append(len(cluster.split()))
	
	# # print rank
	# if(len(rank_sort) > 1):
	# 	rank_sort.sort()
	# # print rank_sort
	# # print rank
	# # print rank
	# # if(len(rank) > 1):
	# # 	rank_sort = rank
	# # 	print rank_sort.sort()
	# for i in range(2):
	# 	least.append(rank_sort[i])
	# # print rank_sort
	# # print least

	# for vrank in rank_sort:
	# 	rank_index.append(rank.index(vrank))
	# 	rank_loop.append(rank.index(vrank))
	# rank_loop.sort()
	# # print rank_index
	# # if(len(rank) > 1):
	# # 	print rank 
	# # 	print rank_index	
	f.close()
	for i in range(2):
		least.append(rank[i])
	
	f = open("./Output/" + category, "r")
	m = 0 
	
	for cluster in f:
		if(not cluster):
			break
		sum_x = 0.0
		sum_y = 0.0
		flag = 0
		if(len(cluster.split()) in least):
			flag = 1
		for latlong in cluster.split():
			# print latlong
			co = latlong.split(',')
			# print co
			# print latlong
			if(m < 12):
				# var_w = var % (float(co[0].strip()), float(co[1].strip()), "'#" + color_code[rank_index.index(rank_loop[m])] + "'", "'#" + color_code[rank_index.index(rank_loop[m])] + "'")
				var_w = var % (float(co[0].strip()), float(co[1].strip()), "'#" + color_code[m] + "'", "'#" + color_code[m] + "'")
				w.write(var_w + "\n")
			if(flag):
				sum_x += float(co[0].strip())
				sum_y += float(co[1].strip())
		if(flag):
			least_centroids.append(float(sum_x/len(cluster.split()))) 
			least_centroids.append(float(sum_y/len(cluster.split())))
		m += 1

	var_n = "L.circle([%f, %f], 1000, { color: '#CCCCCC', fillcolor: '#CCCCCC', fillOpacity: 0.3 }).addTo(map);"
	f_least = open("./Output/" + category + ".centroid", "w")
	lat = 0
	for text in least_centroids:
		if(lat):
			f_least.write(var_n % (lat, text) + "\n")
			lat = 0
		else:
			lat = text
	f_least.close()

	f.close()
	w.close()






