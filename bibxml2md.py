import xml.etree.ElementTree as ET 
import yaml # pyyaml package
import sys

def removeNewline(str):
    return str.replace('\n', ' ').replace('\r', '')

def parseXML(infile):

    tree = ET.parse(infile)

    root = tree.getroot()
    # Validate root is a "references" tag
    if root.tag != 'references':
        sys.exit("Root tag should be 'references'")

    # Good to go, initialize output map
    references = {}

    for item in root.findall('./reference'):
        anchor = item.get("anchor")
        if anchor == None:
            print("Reference has no anchor, skipping")
            continue

        # initialize output reference
        reference = {}

        target = item.get("target")
        if target:
            reference["target"] = target

        title = removeNewline(item.find("front/title").text)
        if title == "":
            print("Warning: anchor '"+anchor+"' has no title")
        else:
            reference["title"] = title

        # Collect authors
        authors = []
        for author in item.findall('front/author'):
            yauthor = {}

            fullname = author.get("fullname")
            if fullname:
                yauthor["name"] = fullname

            initials = author.get("initials")
            surname = author.get("surname")
            if initials and surname:
                ins = initials + " " + surname
            elif initials:
                ins = initials
            elif surname:
                ins = surname
            else:
                ins = None

            if ins:
                yauthor["ins"] = ins

            org = author.find("organization")
            if org is not None and org.text is not None:
                yauthor["org"] = org.text

            authors.append(yauthor)
            
        reference["author"] = authors

        # The date
        date = item.find("front/date")
        if date is not None:
            month = date.get("month")
            year = date.get("year")
            if month:
                ydate = month + " " + year
            elif year:
                ydate = year
            if month or year:
                reference["date"] = ydate
            else:
                reference["date"] = False # An empty "date" element, this keeps xml2rfc happy
    
        seriesinfoList = item.findall("seriesInfo")
        if seriesinfoList != []:
            yseriesinfo = {}
            for si in seriesinfoList:
                name = si.get("name")
                value = si.get("value")
                yseriesinfo[name] = value
            reference["seriesinfo"] = yseriesinfo

        references[anchor] = reference

    # print(yaml.dump(references))
    return references

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: " + sys.argv[0] + " infile outfile")
    infile = sys.argv[1]
    outfile = sys.argv[2]

    refs = parseXML(infile)
    references = {"references": refs} # Add a top level (this makes it easier to cut and paste)
    out = open(outfile, "w")
    out.write(yaml.dump(references, width = float("inf"))) # work around pyyaml line break behavior

if __name__ == "__main__":
    main()
