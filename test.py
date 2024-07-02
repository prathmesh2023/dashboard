  File "/home/ubuntu/dlib-19.2/setup.py", line 603, in <module>
    setup(
  File "/usr/lib/python3/dist-packages/setuptools/__init__.py", line 153, in setup
    return distutils.core.setup(**attrs)
  File "/usr/lib/python3.10/distutils/core.py", line 148, in setup
    dist.run_commands()
  File "/usr/lib/python3.10/distutils/dist.py", line 966, in run_commands
    self.run_command(cmd)
  File "/usr/lib/python3.10/distutils/dist.py", line 985, in run_command
    cmd_obj.run()
  File "/usr/lib/python3/dist-packages/setuptools/command/install.py", line 74, in run
    self.do_egg_install()
  File "/usr/lib/python3/dist-packages/setuptools/command/install.py", line 116, in do_egg_install
    self.run_command('bdist_egg')
  File "/usr/lib/python3.10/distutils/cmd.py", line 313, in run_command
    self.distribution.run_command(command)
  File "/usr/lib/python3.10/distutils/dist.py", line 985, in run_command
    cmd_obj.run()
  File "/home/ubuntu/dlib-19.2/setup.py", line 590, in run
    self.run_command("build")
  File "/usr/lib/python3.10/distutils/cmd.py", line 313, in run_command
    self.distribution.run_command(command)
  File "/usr/lib/python3.10/distutils/dist.py", line 985, in run_command
    cmd_obj.run()
  File "/home/ubuntu/dlib-19.2/setup.py", line 405, in run
    self.build_dlib()
  File "/home/ubuntu/dlib-19.2/setup.py", line 554, in build_dlib
    if run_process(cmake_cmd):
  File "/home/ubuntu/dlib-19.2/setup.py", line 298, in run_process
    # while t.isAlive():
    while t.is_alive():

AttributeError: 'Thread' object has no attribute 'isAlive'. Did you mean: 'is_alive'?