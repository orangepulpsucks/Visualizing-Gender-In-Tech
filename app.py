import csv
from flask import Flask, request, render_template
import psycopg2, random

from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    "host=db dbname=postgres user=postgres password=postgres",
    cursor_factory=RealDictCursor)
app = Flask(__name__)

# HOME -> 1
@app.route('/')
def render_sets1():
    edlevel = request.args.get("edlevel", "%")
    gender = request.args.get("gender", "%")
    mainbranch = request.args.get("mainbranch", "%")
    yearscode = request.args.get("yearscode", "")
    country = request.args.get("country", "")
    haveworkedwith = request.args.get("haveworkedwith", "")
    computerskills = request.args.get("computerskills", "")
    sort_by = request.args.get("sort_by", "yearscode")
    sort_dir = request.args.get("sort_dir", "asc")
    limit = request.args.get("limit", 500, type=int)

#note to self: ilike is case insensitive!
    from_where_clause1 = """
        from theme
        where %(gender)s is null or gender like %(gender)s
        and (  %(edlevel)s is null or edlevel like %(edlevel)s )
        and ( %(mainbranch)s is null or mainbranch like %(mainbranch)s)
        and ( %(yearscode)s is null or yearscode = %(yearscode)s )
        and ( %(computerskills)s is null or computerskills = %(computerskills)s )
        and ( %(haveworkedwith)s is null or haveworkedwith ilike %(haveworkedwith)s )
        and ( %(country)s is null or country ilike %(country)s )
    """

    params1 = {
        "gender": f"{gender}",
        "edlevel": f"{edlevel}",
        # "mainbranch": f"{mainbranch}" if mainbranch != '' else '%',
        "mainbranch": f"{mainbranch}",
        "yearscode": int(yearscode) if yearscode and yearscode.isdigit() else 0
        if yearscode and not yearscode.isdigit() else None,
        "computerskills": int(computerskills) if computerskills and computerskills.isdigit() else 0
        if computerskills and not computerskills.isdigit() else None,
        "haveworkedwith": f"%{haveworkedwith}",
        "country": f"%{country}",

        "sort_by": sort_by,
        "sort_dir" : sort_dir,
        "limit" : limit
}

    def get_sort_dir(col):
        if col== sort_by:
            return "desc" if sort_dir == "asc" else "asc"
        else:
            return "asc"
             
    with conn.cursor() as cur:
        cur.execute(f"""select gender, edlevel, mainbranch, yearscode, computerskills, haveworkedwith, country
                        {from_where_clause1} 
                        order by {sort_by} {sort_dir} 
                        limit %(limit)s 
                    """,
                    params1)
        results1 = list(cur.fetchall())  
        
        cur.execute(f"select count(*) as count {from_where_clause1}", params1)
        count = cur.fetchone()["count"]

    print(results1)
    
    return render_template("home.html",
                           theme=results1,
                           params1=request.args,
                           result_count=count,
                           get_sort_dir = get_sort_dir
                           ) 
    
# VISUALIZATIONS-BY-GENDER 
@app.route('/Visualizations-by-Gender')
def visualizations_by_gender():
    return render_template("visualizations-by-gender.html"
                           ) 
    
# VISUALIZATIONS-BY-EDUCATION 
@app.route('/Visualizations-by-Education')
def visualizations_by_education():
    return render_template("visualizations-by-education.html")

# VISUALIZATIONS-BY-BRANCH 
@app.route('/Visualizations-by-Branch')
def visualizations_by_branch():
    return render_template("visualizations-by-branch.html")

# ABOUT
@app.route('/About')
def about():
    return render_template("about.html")

