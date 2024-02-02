from flask import *
import sqlite3

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT issueno,articleid FROM article GROUP BY issueno ORDER BY issueno DESC ")
    issueNOs = c.fetchall()
    conn.close()
    return render_template("home.html", issueNOs=issueNOs)

@app.route("/issue/<issueno>")
def issue(issueno):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT articleid FROM article WHERE issueno=?",(issueno, ))
    records = c.fetchall()
    articleIDs = []
    for id in records:
        articleIDs.append(id[0])

    allData = []
    nameData = []
    for id in articleIDs:
        c.execute("SELECT art.articletitle,aut.authorname FROM article art, author aut, authorarticle autart WHERE "
                  "art.articleid=autart.articleid AND aut.authorid=autart.authorid AND art.articleid=?", (id, ))
        secondrecord = c.fetchall()

        for names in secondrecord:
           nameData.append(names[1])

        mytuple = ((secondrecord[0][0],) + (nameData, ))
        allData.append(mytuple)
        nameData =  []

    conn.close()
    return render_template("issue.html", allrecords=allData)



@app.route("/author/<authorname>")
def author(authorname):
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT authorid FROM author WHERE authorname=?",(authorname, ))
    records = c.fetchall()
    idlist = []
    for id in records:
        c.execute("SELECT art.articletitle FROM article art, author aut, authorarticle autart WHERE "
                  "art.articleid=autart.articleid AND aut.authorid=autart.authorid AND aut.authorid=?", (id[0],))
        records = c.fetchall()

    return render_template("author.html", data=records)


@app.get("/getissue")
def getissue():

    articleTitle = request.args.get("q", None)
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT issueno FROM article WHERE articletitle=?",(articleTitle, ))
    records = c.fetchall()[0][0]
    conn.close()
    return records

@app.get("/getauthors")
def getauthors():

    articleTitle = request.args.get("q", None)
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()
    c.execute("SELECT articleid FROM article WHERE articletitle=?",(articleTitle, ))
    records = c.fetchall()
    namelist = ""
    for record in records:
        c.execute("SELECT aut.authorname FROM article art, author aut, authorarticle autart WHERE "
                  "art.articleid=autart.articleid AND aut.authorid=autart.authorid AND art.articleid=?", (record[0],))
        allrecords = c.fetchall()

    conn.close()
    #ı am notsure for this part so I commented hocam, ifit works, please consideras not commented
    # for name in allrecords:
    #     namelist += name[0]
    #
    # return namelist
    return ""


if __name__ == "__main__":
    app.run()