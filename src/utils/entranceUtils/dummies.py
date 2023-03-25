def type_of_meal_plan(data):
    a=[0,0,0,0]
    if data=='Meal Plan 1':
        a[0]=1
    if data=='Meal Plan 2':
        a[1]=1
    if data=='Meal Plan 3':
        a[2]=1
    if data=='Not Selected':
        a[3]=1
    return a
    

def room_type_reserved(data):
    a=[0,0,0,0,0,0,0]
    if data=='Room_Type 1':
        a[0]=1
    if data=='Room_Type 2':
        a[1]=1
    if data=='Room_Type 3':
        a[2]=1
    if data=='Room_Type 4':
        a[3]=1
    if data=='Room_Type 5':
        a[4]=1
    if data=='Room_Type 6':
        a[5]=1
    if data=='Room_Type 7':
        a[6]=1
    return a

def market(data):
    a=[0,0,0,0,0]
    if data=='Aviation':
        a[0]=1
    if data=='Complementary':
        a[1]=1
    if data=='Corporate':
        a[2]=1
    if data=='Offline':
        a[3]=1
    if data=='Online':
        a[4]=1
    return a



def booking(data):
    a=[0,0]
    if data=='Canceled':
        a[0]=1
    if data=='Not_Canceled':
        a[1]=1
    return a



def arrival_year(data):
    a=[0,0]
    if data==2017:
        a[0]=1
    if data==2018:
        a[1]=1
    return a



def arrival_month(data):
    a=[0]*12
    a[data-1]=1
    return a


def arrival_date(data):
    a=[0]*31
    a[data-1]=1
    return a

