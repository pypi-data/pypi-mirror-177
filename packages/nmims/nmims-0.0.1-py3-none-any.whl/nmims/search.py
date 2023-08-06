def search():
    print('''

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('darkgrid')
plt.rcParams['font.size']=18
plt.rcParams['figure.figsize']=(20,8)

x=[1,3,5,1,6,11]
y=[2,6,4,10,10,7]
plt.scatter(x,y,s=100)

plt.annotate('A',(x[0],y[0]))
plt.annotate('B',(x[1],y[1]))
plt.annotate('C',(x[2],y[2]))
plt.annotate('D',(x[3],y[3]))
plt.annotate('E',(x[4],y[4]))
plt.annotate('F',(x[5],y[5]))

plt.plot([1,3],[2,6])
plt.plot([1,5],[2,4])
plt.plot([3,1],[6,10])
plt.plot([5,6],[4,10])
plt.plot([6,11],[10,7])
plt.plot([1,11],[10,7])
plt.plot([3,6],[6,10])


''')

search()