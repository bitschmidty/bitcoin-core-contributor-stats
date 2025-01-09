import glob, os, json, jinja2
from collections import defaultdict as dd

GH_META_DIR = "../github-metadata-backup-bitcoin-bitcoin"

user = "<GITHUB-HANDLE>"
year = "2024"

prs = []
for file_name in [file for file in glob.glob(os.path.join(GH_META_DIR + "/pulls/", '*.json'))[:]]:
    with open(file_name) as json_file:
        prs.append(json.load(json_file))

own_prs = []
count_prs_opened = 0
count_prs_merged = 0
count_prs_closed = 0
count_commits = 0
labels_opened = dd(int)
prs_others = []
comments_own = 0
comments_others = 0

prs_by_user = [pr for pr in prs if pr["pull"]["user"]["login"] == user] 
for pr in prs_by_user:
    # opened in year
    pull = pr["pull"]
    if pull["created_at"].startswith(year):
        own_prs.append(pull)
        count_prs_opened+=1
        
        for label in pull["labels"]:
            labels_opened[label["name"]] += 1
    # merged in year
    if "merged_at" in pull and pull["merged_at"].startswith(year):
        if pull not in own_prs:
            own_prs.append(pull)
        count_prs_merged+=1
        count_commits += int(pull["commits"])
    #closed in year
    if pull["state"] == "closed" and "merged_at" not in pull and pull["closed_at"].startswith(year):
        if pull not in own_prs:
            own_prs.append(pull)
        count_prs_closed+=1

for commented_pr in prs:
    total_comments_all = 0
    
    for event in commented_pr["events"]:
        # review
        if event["event"] == "reviewed" and "user" in event and event["user"]["login"] == user and event["submitted_at"].startswith(year):
            total_comments_all+=1
        # comment
        elif event["event"] == "commented" and "user" in event and event["user"]["login"] == user and event["created_at"].startswith(year):
            total_comments_all+=1
    # review comment
    for comment in commented_pr["comments"]:
        if "user" in comment and comment["user"] is not None and "login" in comment["user"] and comment["user"]["login"] == user and comment["created_at"].startswith(year):
            total_comments_all+=1
    
    if total_comments_all > 0:
        if commented_pr["pull"]["user"]["login"] == user:
            comments_own += total_comments_all
        else:
            comments_others += total_comments_all
            prs_others.append({'number': commented_pr["pull"]["number"], 'count': total_comments_all, "title" : commented_pr["pull"]["title"]})

stats = {'year': year,
        'contributor': user,
        'prs_opened': count_prs_opened,
        'components': [(l[0], l[1]) for l in sorted([l for l in labels_opened.items()], key=lambda i: i[1], reverse=True)[0:3]],
        'prs_merged': count_prs_merged,
        'prs_closed': count_prs_closed,
        'commits': count_commits,
        'popular_prs': sorted(own_prs, key=lambda i: int(i["comments"])+int(i["review_comments"]), reverse=True)[0:10], #TODO: this is missing a comment data source that github doesnt have in summary fields (review)
        'comments': comments_own+comments_others,
        'comments_others': comments_others,
        'prs_others': sorted(prs_others, key=lambda i: int(i["count"]), reverse=True)[0:10]}

print(jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template('stats.html').render(stats=stats))