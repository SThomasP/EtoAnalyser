import sys


class ProgressBar:
    def __init__(self, verb, noun, count, length=15):
        self.verb = verb
        self.noun = noun
        self.count = count
        self.length = length
        self.trailing = ""
        self.progress = 0

    def start(self):
        self.trailing = trailing = '> ({:.0%})'.format(self.percentage)
        leading = '{}ing {}:'.format(self.verb.capitalize(), self.noun.capitalize())
        t_count = (20 - len(leading)) // 4 + 1
        description = leading + '{}<{}'.format('\t' * t_count, ' ' * self.length) + trailing
        sys.stdout.write(description)

    def update(self, amount=1):
        if not self.done:
            sys.stdout.flush()
            sys.stdout.write('\b' * (self.length + len(self.trailing)))
            self.progress += amount
            self.trailing = '> ({:.0%})'.format(self.percentage)
            dashes = int(self.percentage * self.length)
            spaces = self.length - dashes
            description = '{}{}'.format('-' * dashes, ' ' * spaces) + self.trailing
            sys.stdout.write(description)
            if self.done:
                sys.stdout.write(' {}ed \r\n'.format(self.verb.capitalize()))
                sys.stdout.flush()

    @property
    def done(self):
        return self.progress == self.count

    @property
    def percentage(self):
        return self.progress / self.count