from tqdm import tqdm
import psutil

ncpu = psutil.cpu_count()
u = psutil.cpu_percent(0.1, True)

t = [
    tqdm(desc=f"CPU {i} usage",
         total=100,
         leave=False,
         position=i,
         bar_format='{l_bar}{bar}|{n_fmt:4.4}% ',
         initial=u[i]) for i in range(ncpu)
]

try:
    while True:
        n = psutil.cpu_percent(0.1, True)
        for i in range(ncpu):
            t[i].update(n[i] - u[i])
        u = n
except KeyboardInterrupt:
    map(lambda x: x.close(), t)
