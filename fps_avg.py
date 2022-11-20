f = open('fps.txt')
#r = f.read().split('\n')
f.seek(0)
r = f.readlines()
f.close()
for i in range(len(r)):
    if i != '0':
        r[i] = int(r[i])
print('Average FPS:',sum(r)//len(r))
time = {'hours':0,'minutes':0,'seconds':0}
time['seconds'] = len(r)//60
if time['seconds'] >= 60:
    time['seconds'] = len(r)%60
    time['minutes'] = (len(r)//3600)

if time['minutes'] >= 60:
    time['minutes'] = (len(r)%3600)//60
    time['hours'] = len(r)//(60**3)

print('Time played:')
print(time)
