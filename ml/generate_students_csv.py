import csv
import random
import pandas as pd
df=pd.read_csv("ml/data/students.csv")
print(df["career_domain"].value_counts())

# stream options 
streams = [
"Computer Science",
"Information Technology",
"Data Science",
"Mathematics",
"Statistics",
"Mechanical Engineering",
"Commerce",
"Finance",
"Law",
"Arts",
"Psychology"
]

#ineterst options 
interests = [
"Development",
"Data",
"AI",
"Cloud",
"Security",
"Finance",
"Writing",
"Design",
"Research"
]

# career data 
career_data = {
"Software Developer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Development"],
"skills":[
"python","java","django","flask","api","git","linux",
"backend","programming","oop","dsa","algorithms","debugging"
]
},

"Data Scientist":{
"education":["Undergraduate","Postgraduate","PhD"],
"streams":["Data Science","Computer Science","Mathematics","Statistics"],
"interest":["Data","AI","Research"],
"skills":[
"python","pandas","numpy","statistics","machinelearning",
"analytics","dataanalysis","matplotlib","seaborn",
"scikit","sql","visualization"
]
},

"Machine Learning Engineer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Data Science","Mathematics"],
"interest":["AI","Development"],
"skills":[
"python","tensorflow","pytorch","machinelearning",
"ai","deeplearning","neuralnetworks","modeltraining"
]
},

"Cloud Engineer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Cloud","Development"],
"skills":[
"aws","docker","kubernetes","cloud","devops",
"linux","terraform","jenkins","monitoring"
]
},

"Cybersecurity Analyst":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Security"],
"skills":[
"linux","network","security","ethicalhacking",
"firewall","penetration","cybersecurity",
"threatanalysis","forensics"
]
},

"Content Writer":{
"education":["High School","Undergraduate"],
"streams":["Arts"],
"interest":["Writing","Design"],
"skills":[
"writing","seo","blogging","editing",
"content","copywriting","storytelling",
"articles","creativity"
]
},

"Financial Analyst":{
"education":["Undergraduate","Postgraduate"],
"streams":["Finance","Commerce"],
"interest":["Finance"],
"skills":[
"excel","financialanalysis","accounting",
"budgeting","investment","financialmodeling",
"reporting","valuation","analytics"
]
},

"Finance Manager":{
"education":["Undergraduate","Postgraduate"],
"streams":["Finance","Commerce"],
"interest":["Finance"],
"skills":[
"finance","accounting","budgeting",
"financialplanning","management",
"investment","taxation","audit"
]
},

"Clinical Psychologist":{
"education":["Undergraduate","Postgraduate","PhD"],
"streams":["Psychology"],
"interest":["Research"],
"skills":[
"counselling","therapy","mentalhealth",
"psychology","behavioranalysis","diagnosis",
"patientcare","research","communication"
]
},

"Psychology Researcher":{
"education":["Postgraduate","PhD"],
"streams":["Psychology"],
"interest":["Research"],
"skills":[
"research","statistics","dataanalysis",
"psychology","behaviorstudy","reportwriting",
"analysis","survey","academicwriting"
]
},

"Lawyer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Law"],
"interest":["Research"],
"skills":[
"legalresearch","litigation","courtprocedure",
"legalwriting","argument","contractlaw",
"caseanalysis","negotiation","documentation"
]
},

"Legal Advisor":{
"education":["Undergraduate","Postgraduate"],
"streams":["Law"],
"interest":["Research"],
"skills":[
"legaladvice","corporatelaw","contractreview",
"legalresearch","documentation","compliance",
"regulations","riskanalysis","legalwriting"
]
},

"Judge":{
"education":["Postgraduate","PhD"],
"streams":["Law"],
"interest":["Research"],
"skills":[
"legalanalysis","judgement","courtprocedure",
"lawinterpretation","legalresearch",
"decisionmaking","caseanalysis","ethics","legalwriting"
]
},

"Frontend Developer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Development"],
"skills":[
"html","css","javascript","react","bootstrap",
"frontend","ui","responsive","web"
]
},

"Backend Developer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Development"],
"skills":[
"python","django","flask","nodejs","api",
"backend","database","sql","authentication"
]
},

"Full Stack Developer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Development"],
"skills":[
"javascript","react","nodejs","mongodb",
"fullstack","frontend","backend","api"
]
},

"Data Analyst":{
"education":["Undergraduate","Postgraduate"],
"streams":["Data Science","Statistics","Mathematics"],
"interest":["Data"],
"skills":[
"excel","sql","python","dataanalysis",
"visualization","statistics","analytics"
]
},

"DevOps Engineer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Cloud"],
"skills":[
"docker","kubernetes","ci","cd",
"jenkins","automation","linux","devops"
]
},

"Mobile App Developer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Computer Science","Information Technology"],
"interest":["Development"],
"skills":[
"android","kotlin","flutter","dart",
"mobile","apps","reactnative","ui"
]
},

"Mechanical Design Engineer":{
"education":["Undergraduate","Postgraduate"],
"streams":["Mechanical Engineering"],
"interest":["Research"],
"skills":[
"cad","solidworks","design","mechanics",
"manufacturing","engineering"
]
},

"Investment Banker":{
"education":["Undergraduate","Postgraduate"],
"streams":["Finance","Commerce"],
"interest":["Finance"],
"skills":[
"finance","investment","valuation",
"financialmodeling","banking","analysis"
]
},

"Marketing Specialist":{
"education":["Undergraduate","Postgraduate"],
"streams":["Commerce","Arts"],
"interest":["Design"],
"skills":[
"marketing","branding","campaign",
"seo","socialmedia","analytics"
]
},

"Academic Researcher":{
"education":["Postgraduate","PhD"],
"streams":["Mathematics","Statistics","Psychology"],
"interest":["Research"],
"skills":[
"research","statistics","analysis",
"academicwriting","survey","datacollection"
]
}
}

#Database data of code 
rows=[]
counter=1

for career in career_data:
    for i in range(800):
        name=f"S{counter}"
        if random.random() < 0.7:
            stream=random.choice(career_data[career]["streams"])
        else:
            stream=random.choice(streams)

        if random.random() < 0.7:
            interest=random.choice(career_data[career]["interest"])
        else:
            interest=random.choice(interests)

        education=random.choice(career_data[career]["education"])
        cgpa=round(random.uniform(6.5,9.5),1)

        skill_list=career_data[career]["skills"]
        num_skills=random.randint(3,8)
        skills=" ".join(random.sample(skill_list,min(num_skills,len(skill_list))))

        rows.append([
            name,
            education,
            stream,
            cgpa,
            skills,
            interest,
            career
        ])
        counter+=1

#save database 
with open("ml/data/students.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow([
    "name",
    "education_level",
    "stream",
    "cgpa",
    "skills",
    "interest",
    "career_domain"
    ])
    writer.writerows(rows)
print("Dataset generated successfully (~6500 rows)")