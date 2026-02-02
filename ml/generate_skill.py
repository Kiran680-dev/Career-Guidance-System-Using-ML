import random
import csv

careers = {
#TECHNICAL caree paths 
"Software Engineer": [
["python","dsa","algorithms","debugging","programming","oop","datastructures"],
["java","oop","collections","multithreading","jdbc","spring","backend"],
["c++","optimization","debugging","systems","programming","memory","pointers"],
["git","linux","docker","debugging","systems","versioncontrol"],
["golang","concurrency","backend","systems","api","microservices"]
],

"Frontend Developer": [
["html","css","javascript","react","uiux","responsive"],
["html","css","bootstrap","figma","javascript","design"],
["vue","css","api","axios","javascript","frontend"],
["react","sass","responsive","design","frontend","ui"],
["angular","typescript","uiux","css","html","frontend"]
],

"Backend Developer": [
["python","django","sql","api","backend","authentication"],
["python","flask","postgresql","docker","api","backend"],
["nodejs","express","mongodb","api","server","backend"],
["java","springboot","sql","restapi","backend","microservices"],
["php","laravel","mysql","api","backend","server"]
],

"Full Stack Developer": [
["react","nodejs","mongodb","express","api","fullstack"],
["javascript","react","nodejs","sql","fullstack","frontend"],
["html","css","javascript","flask","sql","backend"],
["mern","react","node","express","mongodb","fullstack"],
["frontend","backend","api","database","fullstack","development"]
],

"Cloud Engineer": [
["aws","cloud","docker","kubernetes","devops","linux","terraform"],
["azure","cloud","linux","networking","deployment","devops"],
["gcp","cloud","terraform","ci/cd","devops","automation"],
["aws","ec2","s3","iam","monitoring","cloud"],
["docker","jenkins","pipeline","automation","cloud","devops"]
],

"Cybersecurity Analyst": [
["cybersecurity","networking","firewall","linux","ethicalhacking","security"],
["penetrationtesting","security","linux","monitoring","analysis"],
["networksecurity","threatanalysis","malware","forensics","siem"],
["security","vulnerability","testing","firewall","incidentresponse"],
["ethicalhacking","kali","linux","cyberlaw","security"]
],

"Data Scientist": [
["python","pandas","numpy","machinelearning","statistics","dataanalysis"],
["python","sklearn","matplotlib","seaborn","analytics","visualization"],
["r","statistics","dataanalysis","visualization","modeling","analytics"],
["python","tensorflow","keras","deeplearning","ai","neuralnetworks"],
["python","sql","tableau","analytics","reporting","datavisualization"]
],

"DevOps Engineer": [
["docker","kubernetes","ci/cd","automation","pipeline","devops"],
["jenkins","docker","cloud","automation","deployment","pipeline"],
["linux","scripting","devops","monitoring","automation","infrastructure"],
["terraform","cloud","ci/cd","devops","pipeline","automation"],
["kubernetes","cloud","automation","docker","devops","container"]
],

"Mobile App Developer": [
["java","android","studio","mobile","development","apps"],
["flutter","dart","mobile","ui","development","apps"],
["swift","ios","mobile","apps","development","apple"],
["reactnative","javascript","mobile","apps","ui"],
["android","kotlin","mobile","apps","development"]
],

"Machine Learning Engineer": [
["python","tensorflow","machinelearning","ai","modeling","neuralnetworks"],
["pytorch","deep","learning","neuralnetworks","ai","training"],
["python","sklearn","ml","algorithms","ai","modeling"],
["pandas","data","preprocessing","ml","python","analytics"],
["ai","modeltraining","tensorflow","python","ml"]
],

"Data Engineer": [
["python","etl","spark","hadoop","datawarehouse","sql"],
["python","airflow","etl","pipeline","dataengineering"],
["spark","hadoop","data","bigdata","etl","processing"],
["sql","datawarehouse","etl","analytics","datamodeling"],
["python","spark","hadoop","pipeline","dataengineering"]
],

"AI Engineer": [
["python","ai","machinelearning","deeplearning","tensorflow"],
["python","nlp","ai","transformers","pytorch"],
["computervision","opencv","ai","deeplearning"],
["ai","modeltraining","tensorflow","python","neuralnetworks"],
["pytorch","ai","deeplearning","modeldeployment"]
],

"Game Developer": [
["unity","c#","game","development","graphics"],
["unreal","c++","game","design","3d"],
["unity","game","physics","animation"],
["c++","game","engine","development","graphics"],
["unity","c#","game","ui","animation"]
],

"Blockchain Developer": [
["blockchain","solidity","ethereum","smartcontracts"],
["web3","solidity","crypto","blockchain","defi"],
["ethereum","smartcontracts","solidity","web3"],
["blockchain","crypto","security","web3"],
["solidity","ethereum","blockchain","development"]
],

"Database Administrator": [
["sql","database","mysql","performance","optimization"],
["postgresql","database","backup","recovery"],
["oracle","database","administration","security"],
["sqlserver","database","maintenance","monitoring"],
["database","indexing","query","optimization"]
],

"Network Engineer": [
["networking","routing","switching","tcpip"],
["cisco","network","routing","firewall"],
["networksecurity","vpn","network","protocols"],
["lan","wan","network","infrastructure"],
["network","monitoring","routing","switching"]
],

# NON TECHNICAL 
"Marketing Manager": [
["marketing","branding","sales","analytics","strategy","campaign"],
["seo","content","socialmedia","advertising","marketing"],
["digitalmarketing","campaign","analytics","strategy","branding"],
["communication","presentation","negotiation","sales","targets"],
["marketresearch","strategy","branding","growth","planning"]
],

"Business Analyst": [
["dataanalysis","business","reporting","excel","analytics"],
["requirements","stakeholder","communication","analysis","documentation"],
["business","strategy","analytics","planning","reporting"],
["process","analysis","documentation","modeling","business"],
["market","analysis","strategy","planning","reporting"]
],

"Financial Analyst": [
["finance","modeling","investment","riskanalysis","excel"],
["financialanalysis","portfolio","investment","banking","finance"],
["financialreporting","accounting","analysis","budgeting","finance"],
["portfolio","management","finance","investment","analysis"],
["financial","valuation","analysis","investment","finance"]
],

"Banking Officer": [
["finance","accounting","tally","taxation","auditing"],
["banking","loan","credit","finance","compliance"],
["investment","banking","riskanalysis","excel","finance"],
["banking","operations","finance","services","compliance"],
["financialanalysis","investment","banking","risk","portfolio"]
],

"Graphic Designer": [
["photoshop","illustrator","creativity","branding","design"],
["figma","uiux","wireframe","prototype","design"],
["canva","poster","typography","layout","creativity"],
["illustrator","logo","branding","design","graphics"],
["adobe","creativity","visual","editing","design"]
],

"UI UX Designer": [
["figma","uiux","wireframe","prototype","design"],
["userresearch","design","prototype","uiux","figma"],
["interaction","design","wireframe","prototype","uiux"],
["designthinking","usability","uiux","research","figma"],
["userexperience","design","figma","prototype","uiux"]
],

"Content Writer": [
["writing","storytelling","blogging","editing","creativity"],
["seo","blogging","contentstrategy","writing","editing"],
["article","writing","storytelling","editing","blogging"],
["copywriting","blogging","content","marketing","writing"],
["content","creation","writing","editing","blogging"]
],

"Sales Manager": [
["sales","negotiation","communication","targets","presentation"],
["customer","relations","sales","strategy","marketing"],
["leadgeneration","negotiation","sales","closing","deals"],
["salesstrategy","communication","targets","marketing"],
["businessdevelopment","sales","negotiation","strategy"]
],

"Product Manager": [
["product","strategy","roadmap","stakeholder","agile"],
["productplanning","roadmap","analytics","management","strategy"],
["marketresearch","product","development","strategy","planning"],
["productlifecycle","planning","strategy","roadmap"],
["agile","scrum","product","planning","roadmap"]
],

"HR Manager": [
["recruitment","hiring","training","hr","management"],
["employee","relations","hr","policies","training"],
["talent","acquisition","hiring","recruitment","hr"],
["hr","management","employee","engagement","training"],
["performance","management","hr","training","recruitment"]
],

"Digital Marketing Specialist": [
["seo","socialmedia","marketing","campaign"],
["googleads","analytics","marketing","advertising"],
["contentmarketing","seo","branding","digitalmarketing"],
["socialmedia","content","marketing","strategy"],
["analytics","seo","marketing","growth"]
],

"Project Manager": [
["projectmanagement","planning","leadership","agile"],
["scrum","planning","stakeholder","management"],
["projectplanning","teammanagement","riskmanagement"],
["leadership","project","planning","communication"],
["agile","scrum","projectmanagement"]
],

"Operations Manager": [
["operations","management","planning","logistics"],
["supplychain","operations","optimization"],
["operations","process","management"],
["logistics","planning","operations","analysis"],
["operations","management","strategy"]
],

"Entrepreneur": [
["business","startup","strategy","innovation"],
["entrepreneurship","management","leadership"],
["startup","marketing","businessdevelopment"],
["innovation","strategy","business"],
["startup","growth","businessdevelopment"]
],

"Teacher": [
["teaching","education","communication","presentation"],
["curriculum","teaching","education","planning"],
["education","classroom","teaching"],
["learning","education","communication"],
["teaching","training","education"]
],

"Psychologist": [
["psychology","counselling","therapy","behavior"],
["mentalhealth","psychology","therapy"],
["counselling","psychology","research"],
["behavior","analysis","psychology"],
["therapy","psychology","mentalhealth"]
],

"Lawyer": [
["law","legalresearch","litigation","contracts"],
["legal","law","court","argument"],
["legalresearch","law","caseanalysis"],
["contracts","law","negotiation"],
["law","legalwriting","litigation"]
],

"Journalist": [
["journalism","writing","reporting","news"],
["investigation","reporting","media"],
["writing","news","media"],
["reporting","communication","journalism"],
["news","analysis","reporting"]
],

"SEO Specialist": [
["seo","keywords","analytics","content"],
["searchengine","optimization","seo","ranking"],
["seo","marketing","googleanalytics","content"],
["seo","backlinks","optimization","marketing"],
["seo","traffic","analytics","growth"]
],

"Public Relations Manager": [
["publicrelations","communication","branding","media"],
["pressrelease","communication","media","branding"],
["publicrelations","marketing","communication"],
["media","communication","reputation"],
["branding","publicrelations","communication"]
],

"Event Manager": [
["eventplanning","management","coordination"],
["event","planning","logistics"],
["event","communication","organization"],
["eventmanagement","planning","budget"],
["event","coordination","management"]
],

"Supply Chain Manager": [
["supplychain","logistics","planning"],
["inventory","supplychain","management"],
["logistics","operations","planning"],
["supplychain","distribution","analysis"],
["procurement","supplychain","logistics"]
],

"Economist": [
["economics","analysis","research"],
["economics","dataanalysis","statistics"],
["economicresearch","policy","analysis"],
["economics","forecasting","analysis"],
["economics","research","reporting"]
],

"Research Analyst": [
["research","analysis","data"],
["marketresearch","analysis","report"],
["research","dataanalysis","report"],
["analysis","research","statistics"],
["research","survey","analysis"]
],

"Interior Designer": [
["interior","design","creativity"],
["design","spaceplanning","decor"],
["interior","architecture","design"],
["design","furniture","layout"],
["interior","planning","design"]
],

"Video Editor": [
["videoediting","premiere","editing"],
["editing","video","storytelling"],
["aftereffects","videoediting","motion"],
["video","editing","production"],
["editing","video","creativity"]
],

"Photographer": [
["photography","editing","camera"],
["photoshoot","lighting","camera"],
["photography","editing","creativity"],
["camera","composition","photography"],
["photography","visual","editing"]
],

"Animator": [
["animation","design","creativity"],
["3d","animation","modeling"],
["animation","storyboard","design"],
["animation","graphics","motion"],
["animation","visual","design"]
],

"Game Designer": [
["gamedesign","story","mechanics"],
["game","design","levels"],
["gamedesign","creativity","concept"],
["game","mechanics","design"],
["game","concept","design"]
],

"Customer Support Specialist": [
["customerservice","communication","support"],
["support","communication","problem"],
["customer","support","service"],
["communication","customerservice"],
["support","service","communication"]
],

"Hotel Manager": [
["hospitality","management","service"],
["hotel","management","operations"],
["hospitality","planning","service"],
["hotel","operations","management"],
["hospitality","customer","management"]
],

"Travel Consultant": [
["travel","planning","tourism"],
["tourism","booking","planning"],
["travel","tourism","communication"],
["travel","management","tourism"],
["travel","planning","customer"]
]
}

rows = []
for career in careers:
    for i in range(60):   # 60 rows per career
        skill_set = random.choice(careers[career])
        random.shuffle(skill_set)
        rows.append([" ".join(skill_set), career])
random.shuffle(rows)

with open("ml/data/skill_data.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["skills","career"])
    writer.writerows(rows)
print("Dataset generated successfully (2881 rows)")