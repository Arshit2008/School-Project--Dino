'''def isEmpty(stk):
    if stk == []:
        return True
    else:
        return False
    
def push(stk,item):
    stk.append(item)
    top = len(stk)-1
    
def pop(stk):
    if isEmpty(stk):
        return("Underflow")
    
    else:
        item = stk.pop()
        if len(stk) == 0:
            top = None
        else:
            top = len(stk)-1
        return item

def peek(stk):
    if isEmpty(stk):
        return("underflow")
    else:
        top = len(stk)-1
        return (stk[top])
    
def Display(stk):
    if isEmpty(stk):
        print("Stack Empty")
        
    else:
        top = len(stk)-1
        print(stk[top])
        
        for a in range(top-1,-1,-1):
            print(stk[a])
            
            
stack = []
top = None
while True:
    print("1.push,2.pop,3.peek,4.display stack,5.exit")
    
    ch = int(input ("what operation: "))
    if ch == 1:
        item = input("Enter item : ")
        push(stack,item)
        
    elif ch == 2:
        item = pop (stack)
        if item == "Underflow":
            print("Underflow ! Stack is Empty")
        else:
            print("item poped",item)
            
    elif ch == 3:
        item = peek(stack)
        if item =="Underflow":
            print("item is underflow")
        else:
            print("topmost item i s: ",item)
            
    elif ch == 4:
        Display (stack)
        
    if ch == 5: break
    
    else:print("Invalid input")       ''' 
    
'''
    
L = [("laptop",90000),("mobile",30000),("pen",50),("headphones",1500)]

Product =[]
#push
def Push_element(L):
    for item in L:
        if item[1] > 50:
            Product.append(item)
    print(Product)
    
Push_element (L)


def Pop_item():
    while len(Product) > 0:
        popped_item = Product.pop()
        print(popped_item)
    else:
        print("Stack Empty")
        
Pop_item()'''




Nums = [213,10025,167,254923,14,1297653,31498,286,92765]
BIGNUMS = []
def PushBig (Num):
    for item in Num:
        if len(str(item)) >= 5:
            BIGNUMS.append(item)
            
PushBig (Nums)
print(BIGNUMS)

def PopBig():
    while len(BIGNUMS) > 0:
        print(BIGNUMS.pop())
    else:
        print("Stack Empty")
        
        
PopBig()