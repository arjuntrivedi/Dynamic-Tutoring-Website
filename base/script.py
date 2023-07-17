import json
import requests
from .models import Course

# flagList is a list of tuples with flag name and search value

def url(flagList):
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula." \
          "IScript_ClassSearch?institution=UVA01&term=1228"
    for item in flagList:
        url += "&" + item[0] + "=" + str(item[1])
    r = requests.get(url)
    classList = []
    for c in r.json():
        department = c['subject']
        number = c['catalog_nbr']
        name = c['descr']
        courseName = department + " " + number + ": " + name
        if courseName not in classList:

            c = Course(department = department, number = number, name = name)
            c.save()
            classList.append(courseName)
    return classList

def main():

    for i in range(90):
        print("saving page", i)
        flagList = [("term", 1228), ("page", str(i))]
        list = url(flagList)
#main()
