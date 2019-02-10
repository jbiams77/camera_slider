from menu import MenuSystem
import time
import signal

x = MenuSystem()
x.daemon = True
x.start()


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

# Register the signal handlers
signal.signal(signal.SIGTERM, service_shutdown)
signal.signal(signal.SIGINT, service_shutdown)

try:
    while True:
        time.sleep(5)
except ServiceExit:
    x.shutdown_flag.set()
    x.join()

print('Exiting main program')