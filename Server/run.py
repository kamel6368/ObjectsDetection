from MyApp import MyApp

main = MyApp()
try:
    main.run()
except Exception as e:
    print e.message
