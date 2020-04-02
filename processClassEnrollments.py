from stanfordclasses import StanfordClass
import pickle
import pandas as pd
import plotly.express as px
pickleFilesToAnalyze = ['stanfordclasslistBEFOREANNOUNCEMENTv2.pkl', 
                        'stanfordclasslistAFTERANNOUNCEMENT3-28.pkl',
                        'stanfordclasslistAFTERANNOUNCEMENT3-30.pkl',
                        'stanfordclasslistAFTERANNOUNCEMENT3-31.pkl',
                        'stanfordclasslistAFTERANNOUNCEMENT04_02_01_12_25.pkl',
                        'stanfordclasslistAFTERANNOUNCEMENT04_02_21_38_36.pkl']
pickleFileDaysSinceAnnouncement = [0, 2, 4, 5, 6, 7]
classEnrollmentsOverTime = {}
totalEntries = 0
TRANSITION_SPEED = 400


for pickleFile in pickleFilesToAnalyze:
    with open(pickleFile, 'rb') as f:
        StanfordClassList = pickle.load(f)
    f.close()
    totalEntries+=1
    for currentClass in StanfordClassList:
        #print("===========================================")
        #print(currentClass.title)
        offeredInSpring = False
        hasLecture = False
        countInLecture = 0
        waitListInLecture = 0
        countInSections = 0
        waitListInSection = 0
        totalEnrolled = 0
        currentClass.sections.sort(key = lambda s: s['sectionNumber'])
        for section in currentClass.sections:
            if section['term'] == '2019-2020 Spring':
                offeredInSpring = True
                if section['component'] == 'LEC':
                    hasLecture = True
                    countInLecture += int(section['numEnrolled'])
                    waitListInLecture += int(section['currentWaitlistSize'])
                else:
                    countInSections += int(section['numEnrolled'])
                    waitListInSection  += int(section['currentWaitlistSize'])
                #print(section)
                #print()
        if offeredInSpring:
            if hasLecture:
                totalEnrolled = countInLecture + waitListInLecture
            else:
                totalEnrolled = countInSections + waitListInSection
            #print("Total Enrolled: ", totalEnrolled)
            if totalEnrolled == 0:
                classEnrollmentsOverTime.pop(currentClass.name, None)
                continue
            if currentClass.name not in classEnrollmentsOverTime:
                classEnrollmentsOverTime[currentClass.name] = [totalEnrolled]
                if len(classEnrollmentsOverTime[currentClass.name]) < totalEntries:
                    classEnrollmentsOverTime.pop(currentClass.name, None)
                    continue
                #if len(classEnrollmentsOverTime[currentClass.name]) < totalEntries-1:
                #    while len(classEnrollmentsOverTime[currentClass.name]) < totalEntries:
                #        classEnrollmentsOverTime[currentClass.name].insert(0,0)
            else:
                #while len(classEnrollmentsOverTime[currentClass.name]) < totalEntries-1:
                #    classEnrollmentsOverTime[currentClass.name].insert(0,0)
                
                if len(classEnrollmentsOverTime[currentClass.name]) < totalEntries:

                    classEnrollmentsOverTime[currentClass.name].append(totalEnrolled)
        #print("===========================================")
        #print()
        #print()

classEnrollmentDataPoints = {}
classEnrollmentDataPoints['className'] = []
classEnrollmentDataPoints['Total Enrolled'] = []
classEnrollmentDataPoints['Change in Enrollment since Announcement'] = []
classEnrollmentDataPoints['Absolute Change in Enrollment since Announcement'] = []
classEnrollmentDataPoints['Days Since Announcement'] = []
classEnrollmentDataPoints['department'] = []
for currentClass in classEnrollmentsOverTime:
    for i in range(1,totalEntries):
        classEnrollmentDataPoints['className'].append(currentClass)
        classSize = classEnrollmentsOverTime[currentClass][i]
        classEnrollmentDataPoints['Total Enrolled'].append(classSize)
        changeInSize = classSize - classEnrollmentsOverTime[currentClass][0]
        spaceIndex = currentClass.find(" ")
        classEnrollmentDataPoints['department'].append(currentClass[0:spaceIndex])
        classEnrollmentDataPoints['Change in Enrollment since Announcement'].append(changeInSize)
        #classEnrollmentDataPoints['changeRelativeToClassSize'].append(abs(changeInSize/classSize)*100)
        classEnrollmentDataPoints['Absolute Change in Enrollment since Announcement'].append(abs(changeInSize))
        classEnrollmentDataPoints['Days Since Announcement'].append(pickleFileDaysSinceAnnouncement[i])




classEnrollments = pd.DataFrame.from_dict(classEnrollmentDataPoints)

fig = px.scatter(classEnrollments, x="Total Enrolled", y="Change in Enrollment since Announcement", animation_frame="Days Since Announcement", 
            animation_group = "className", size="Absolute Change in Enrollment since Announcement", color = "department",
            hover_name = "className")
fig.update_layout(transition = {"duration": TRANSITION_SPEED, "easing": "cubic-in-out"})
sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Days since announcement: ",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": TRANSITION_SPEED, "easing": "quad-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}
fig.update_layout(sliders = [sliders_dict], title = "Changes in Course Enrollment since the announcement of S/NC grading", xaxis_title = "Total Enrollment in Class", yaxis_title = "Change in Enrollment since Announcement")
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = TRANSITION_SPEED
fig.layout.updatemenus[0].buttons[0].args[1]["transition"] = {"duration": TRANSITION_SPEED, "easing": "cubic-in-out"}
fig.layout.updatemenus[0].buttons[1].args[1]["transition"] = {"duration": TRANSITION_SPEED, "easing": "cubic-in-out"}
for step in fig.layout.sliders[0].steps:
    step["args"][1]["frame"]["duration"] = TRANSITION_SPEED
    step["args"][1]["transition"]["duration"] = TRANSITION_SPEED
fig.write_html("/pickles/bubblegraph.html")