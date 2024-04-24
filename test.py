class Student:
    def __init__(self,name,number,score):
        self.name = name
        self.number = number
        self.score = [0] * number

    def getName(self):
        return self.name

    def getScore(self,i):
       if 0 <= i < self.number:
           return self.score[i]
       else:
           return "Invalid index"

    def inputScore(self):
        print("Enter score for:",self.name)
        for i in range(self.number):
            score = float(input("Enter score for subject: {}: ",format(i+1)))
            self.score[i] = score

    def getAverage(self):
        total_score = sum(self.score)
        return total_score / self.number

    def getHighscore(self):
        return max(self.score)

    def 

