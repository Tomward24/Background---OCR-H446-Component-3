import csv

def getQuestion(qIndex):
    questionArray = []
    questions = open("csv/questions.csv")
    check_questions = csv.reader(questions)
    for x in check_questions:
        questionArray.append(x[qIndex])

    return questionArray

def getAnswer(randNum,aIndex):
    answerArray = []
    answers = open("csv/answers.csv")
    check_answers = csv.reader(answers)
    for x in check_answers:
        answerArray.append(x[aIndex])

    return answerArray


