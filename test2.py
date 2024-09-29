class UserLevel:
    def __init__(self, points):
        self.points = points

    def currentLevel(self):
        if self.points < 0:
            return 0
        elif self.points <= 99:
            return 1
        else:
            level = 1
            self.max=100
            self.min=0
            diff = self.max
            while self.points >= self.max :
                level += 1
                diff += diff
                self.min=self.max
                self.max=diff+self.max
            self.level=level
            return level
    def getMinOfRange(self):
        return self.min
    def getMaxOfRange(self):
        return self.max

# Example usage
# level = UserLevel(points=220)
# print(level.currentLevel())  # Output: 2
# print(level.pointsNeededToCompleteLevel())  # Output: 80

level = UserLevel(points=700)
print(level.currentLevel())  # Output: 2
# print(level.pointsNeededToCompleteLevel())  # Output: 180
