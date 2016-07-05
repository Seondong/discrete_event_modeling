import random, string, simpy

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

class Doolgi(object):
    def __init__(self, env):
        self.env = env
        self.id = randomword(5)
        self.level = random.randint(1, 10)
        self.action = env.process(self.collect())
        self.collect_amount = random.randint(0, 20)
    def collect(self):
        while True:
            print('Doolgi %s collects %d won at time %.1f' % (self.id, self.collect_amount, self.env.now))
            yield self.env.timeout(self.level)


env = simpy.Environment()
dictDoolgi = dict()
listDoolgi = list()
for i in range(10):
    doolgi = Doolgi(env)
    listDoolgi.append(doolgi)

print listDoolgi
    # listDoolgi.append(Doolgi(env, id, rint))
print len(listDoolgi)
print listDoolgi[0].id
del listDoolgi[0]
print len(listDoolgi)

env.run(until=100)








