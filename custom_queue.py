
class Queue:
    def __init__(self, max=5):
        self.values = []
        self.max = max

    def enqueue(self, value):
        if len(self.values) is self.max:
            self.dequeue()
        return self.values.append(value)

    def dequeue(self):
        if self.is_empty():
            return "Nothing in Queue!"
        return self.values.pop(0)
    
    def max_value(self):
        if self.is_empty():
            return "Queue is empty!"
        return max(self.values)
    
    def is_empty(self):
        return len(self.values) == 0

