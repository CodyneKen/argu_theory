#gunicorn.conf.py

# Après chaque push, recréer venv, pip install flask, networkx, matplotlib, gunicorn
# puis lancer gunicorn -c gunicorn.conf.py app:app

# The socket to bind to. This can be an IP address and port number or a Unix socket.
# In this case, we're binding to a Unix socket.
bind = "unix:/root/argu_theory/app.sock"

# The number of worker processes. This should generally be 2-4 x $(NUM_CORES), depending
# on your application's workload.
workers = 4

# The maximum number of simultaneous clients that a single worker process can handle.
# The default is 1000.
worker_connections = 1000

# The type of worker processes to use. The default is "sync", but other options include
# "eventlet", "gevent", and "tornado".
worker_class = "sync"

# The maximum number of requests a worker will process before restarting. This can help
# manage memory leaks in your application. The default is 0, which means "no limit".
max_requests = 1000

# The amount of time (in seconds) that a worker can spend handling a single request. If a
# worker takes longer than this, it will be killed and a new worker will be spawned.
timeout = 30