import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    key_orderID = record[1]
    mr.emit_intermediate(key_orderID, record)

def reducer(key, list_of_values):
    orderLine = []
    for val in list_of_values:
        if val[0] == "order" :
            orderLine = val
            break
    
    result = []
    for val in list_of_values:
        if val[0] != "order" :
            result = orderLine + val
            mr.emit(result)           
   

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
