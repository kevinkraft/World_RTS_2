#script to test if a change to a list affects the same list that is an atribute of a class

class Hi(object):
    def __init__(self, l):
        self.l = l

def main():

    list = [1,2,3]
    print 'list: ', list

    hi1 = Hi(list)

    print 'hi1.l: ', hi1.l
    
    list.remove(2)
    #list = [1, 3]
    print 'list: ', list
    print 'hi1.l: ', hi1.l

main()
