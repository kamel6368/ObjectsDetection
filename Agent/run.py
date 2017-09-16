import tasks
from Main import Main

main = Main()
try:
    main.run()
except KeyboardInterrupt:
    tasks.shutdown(main, main.tcp_server, main.tcp_client, main.video_capture)
    main.logger.print_msg('Stopped by user')
