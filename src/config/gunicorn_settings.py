import os

bind = '127.0.0.1:' + str(os.getenv('PORT', 8080))
proc_name = 'Infrastructure-Practice-Flask'
workers = 3