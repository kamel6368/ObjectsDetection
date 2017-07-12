import tasks
from main import Main

main = Main()
try:
    main.run()
except KeyboardInterrupt:
    tasks.shutdown(main, main.tcp_server, main.tcp_client)
    main.logger.print_msg('Stopped by user')
