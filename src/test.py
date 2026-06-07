from operator import itemgetter
from typing import Optional


def find_delivery_pair( weights:list[int], target: int) -> list[int]:
    pointer1 = 0
    pointer2= len(weights) -1


    while( pointer1 < pointer2):
        total = weights[pointer1]+weights[pointer2]
        if(total ==target):
            return [pointer1, pointer2]
        elif(total>target):
            pointer2 -=1
        elif(total<target):
            pointer1 +=1
    return []

bookings = [(1,3),(4, 9),(2, 6), (10,15)]

def merge_bookings(bookings : list[tuple[int,int]]):
    bookings.sort(key=itemgetter(0))
    merged = []
    start = bookings[0]
    end = bookings[0]
    for i in range(1, len(bookings)):
        
        if(bookings[i][0]>= bookings[i-1][0] and bookings[i][0] <= bookings [i-1][1]):
            end = bookings[i]
        else :
            merged.append((start[0],end[1]))
            start = bookings[i]
            end = bookings[i]

    merged.append((start[0],end[1]))
    return merged

print(merge_bookings(bookings))
    