from edda import Edda

edda = Edda()
res = edda.check_in_edda_by_name("oceanai")
if not res == None:
    edda_link = edda.get_edda_link("oceanai")
    print(edda_link)
else:
    print("Not found")
