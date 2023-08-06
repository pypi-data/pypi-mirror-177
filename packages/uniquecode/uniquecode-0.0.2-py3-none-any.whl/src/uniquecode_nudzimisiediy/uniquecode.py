import string, random


class Uniquecode:

    options = {
        'randomize': True,
        'limit_size': 6,
        'shift_increment': True,
    }
    
    def __init__(self, prefix='', pattern='' + string.digits + string.ascii_lowercase, suffix='', **options):
        self.prefix = prefix
        self.suffix = suffix
        self.pattern = pattern
        if options:
            self.options.update(options)
        self._pattern = list(self.pattern)
        if self.options['randomize']:
            random.shuffle(self._pattern)
        self.count_max = self.count_limit

    def count(self, n, shift):
        l = len(self.pattern)
        r = (n % l) + shift
        n = int(n / l)
        return self.get_output_char(r), n

    def get_output_char(self, ind):
        output_index = ind if ind<len(self.pattern) else ind-len(self.pattern)
        return self._pattern[output_index]

    @property
    def count_limit(self):
        if self.options['limit_size']:
            self.size = self.options['limit_size'] - len(self.prefix) - len(self.suffix)
            return len(self.pattern) ** self.size - 1
        return None

    def generate(self, n):
        output = ''
        shift = 0
        while n > 0:
            result, n = self.count(n, shift)
            output = result + output
            if self.options['shift_increment']:
                shift += 1
        return output, shift

    def get(self, n):
        if self.count_max and n > self.count_max:
            return 'out of range'
        output, shift = self.generate(n)
        if self.count_max:
            while len(output) < self.size:
                if self.options['shift_increment']:
                    shift += 1
                output = self.get_output_char(shift) + output
        return self.prefix + output + self.suffix