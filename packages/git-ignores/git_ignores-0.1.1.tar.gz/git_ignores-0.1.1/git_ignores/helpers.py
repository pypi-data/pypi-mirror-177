def write_to_file(filename, data):
    """Helper method that writes data to the given file"""
    filet = open(filename, 'w')
    filet.write(data)
    filet.close()

def append_to_file(filename, data):
  """Helper method that appends data to a file"""
  filet = open(filename, 'a')
  filet.write(data)
  filet.close() 