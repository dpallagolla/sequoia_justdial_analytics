#! /usr/bin/env python


f_html = open("./Output/" + "index1.html", "r").read()

f_categories = open("cat_less.txt", "r").read()
categories = f_categories.split("\n")

for category in categories:
	q = open("./Output/" + category + ".send","r").read()
	w = open("./Output/" + category + ".centroid","r").read()
	out = open("./Output/" + "html/" + category + ".html", "w")
	
	out.write(f_html % (q, w))

	out.close()

# f_html.close()
# q.close()
# w.close()
