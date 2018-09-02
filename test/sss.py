s = ['5v1x6bsople3  sys01_web  replicated  1/1       nginx:latest',
     'frxuruvxzg5j  sys01_api  replicated  2/2       nginx:latest',
     'fxdrnvwn5c3g  portainer  replicated  1/1       portainer/portainer:latest']

for i in s:
    print(i.split()[1])
    print(i.split()[3])
