import turtle as t
import requests
import time
import random

screen = t.Screen()

def create_turtle(x,y,shape = 'square'):
    new_seg = t.Turtle()
    new_seg.penup()
    new_seg.shape(shape)
    new_seg.goto(x,y)
def draw_board(x1,y1,car = 0):
    data_x = [x for x in range(-460, 480, 20)]
    data_y = [y for y in range(-380, 390, 20)]
    stable_y = [-380, 380]
    stable_x = [-460, 460]

    parking_s_x = [-460, -276, -92, 92, 276, -460]
    parking_s_y = [-360, 100]

    for x in stable_x:
        for y in data_y:
            create_turtle(x, y)
    for y in stable_y:
        for x in data_x:
            create_turtle(x, y)
    for x in parking_s_x:
        for y in parking_s_y:
            for i in range(14):
                create_turtle(x, y + i * 20)
    if(car):
        print(x1," ",y1)
        create_turtle(x1, y1, 'car_2.gif')
def setup_s():
    global screen
    screen.screensize(400, 400)
    screen.tracer(0)
    screen.register_shape('car_2.gif')
    screen.bgcolor("white")

def return_start(data,string):
    return data.find(string) + len(string) + 2
def return_end(data,start):
    return data.find('"',start,len(data))
def return_start_dec(data,string):
    return data.find(string) + len(string) + 2
def return_end_dec(data,start):
    return data.find('}',start,len(data))

token_id = "cfb28aad-1182-4be5-870d-262f4092858f"
headers = {"api-key": "NNSXS.U4H3ZFFCMSR42BUAZPW2UWGFBV4WCNI5EXDJXDY.SHIF3PP5PBMJNZESN5XLR5TZJTJUIGKVUTM2I22IVBUV"}
last_received = '2023-02-20T23:47:27.289519170Z'
#
status = {'eui-70b3d57ed005a712' : 0}
positions = {'eui-70b3d57ed005a712':[-368, -220]}
setup_s()
screen.update()
screen.exitonclick()

while True: 
    data = []
    r = requests.get('https://webhook.site/token/'+ token_id +'/requests?sorting=newest', headers=headers)
    for request in r.json()['data']:
        data.append(request)
    last = data[0]['content']
    print(last)
    #for i in range(0,len(data)):
    device_id = last[return_start(last,'"device_id"'):return_end(last,return_start(last,'"device_id"'))]
    print(device_id)
    actual_received = last[return_start(last,'"received_at"'):return_end(last,return_start(last,'"received_at"'))]
    if actual_received != last_received:
        last_received = actual_received
        if return_start_dec(last,"packet_number") - len("packet_number") - 2 > 0:
            payload = last[return_start_dec(last,"packet_number"):return_end_dec(last,return_start_dec(last,"packet_number"))]
            status[device_id] = payload
            print(positions[device_id][1])
            print(positions[device_id][0])
            #draw_board(positions[device_id][0],positions[device_id][1],payload)
            screen.update()
            screen.exitonclick()
            time.sleep(10)
            last_received = actual_received



# screen.listen()
# screen.onkey(move_forward,"w")
# screen.onkey(move_backward,"s")
# screen.onkey(turn_left,"a")
# screen.onkey(turn_right,"d")








