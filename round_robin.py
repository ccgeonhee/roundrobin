#간트차트 시간 표현, 터틀 함수화.
import sys
import turtle

def move_turtle(angle, length):
    turtle.fd(length)
    turtle.rt(angle)

def write_time(cor1, cor2, string):
    turtle.goto(cor1, cor2)
    turtle.write(string, False, "right", ("", 10))

def write_job_name(cor1, cor2, string, angle):
    turtle.rt(angle)
    turtle.goto(cor1, cor2)
    turtle.write(string, False, "left", ("", 25))

turtle.shape("arrow")
turtle.hideturtle()
turtle.speed(2)
f = open("round.txt", 'r')

line = []
while True:
    tmp = f.readline()
    if not tmp: break
    line.append(tmp)

for i in range(len(line)): #문자열에 들어가는 \n 를 제거하는 과정.
    if line[i].find("\n") != -1:
        line[i] = line[i].replace("\n","")

for i in range(len(line)):
    line[i] = line[i].split()

Average_turn_around = 0
Arrival_time = []
Job_name = []
CPU_cycle = []


for i in range(len(line)):
    Arrival_time.append(int(line[i][0]))
    Job_name.append(line[i][1])
    CPU_cycle.append(int(line[i][2]))

print("도착시간 작업이름 남은작업량")
for i in range(len(line) - 1):#정렬
    for j in range(len(line) - i - 1):
        if Arrival_time[j] > Arrival_time[j+1]:
            Arrival_time[j], Arrival_time[j+1] = Arrival_time[j+1], Arrival_time[j]
            Job_name[j], Job_name[j+1] = Job_name[j+1], Job_name[j]
            CPU_cycle[j], CPU_cycle[j+1] = CPU_cycle[j+1], CPU_cycle[j]
print('---------------------------')


for i in range(len(line)):
    print("%4s %7s %9s" % (Arrival_time[i], Job_name[i], CPU_cycle[i]))
    if i>0 and Arrival_time[i] == Arrival_time[i-1]:
        print("두 작업의 도착시간이 같습니다. 두 작업의 도착시간을 다르게 설정해주세요.")
        sys.exit()

print("\n\n")
Time_quantum = int(input("Time Quantum을 입력하시오: "))

turn_around = [0 for i in range(len(line))]
count = Arrival_time[0]

print("\n\n")
while(CPU_cycle.count(0) != len(line)): #모든 남은 작업량이 0일때까지
    print("작업이름 남은작업량")
    for j in range(len(line)):
        if turn_around[j] == 0 and CPU_cycle[j] < Time_quantum: #if)남은작업량이 2인데 time_quantum이 3일때.
            move_turtle(90, CPU_cycle[j]*15 + 10)
            move_turtle(90, Time_quantum * 20)
            turtle.fd(CPU_cycle[j]  * 15 + 10)

            xcor = turtle.xcor()
            ycor = turtle.ycor()

            write_time(xcor, ycor-20, count)
            write_job_name(xcor, ycor, Job_name[j], 90)
            move_turtle(90, Time_quantum * 20)
            turtle.fd(CPU_cycle[j]  * 15 + 10)
            count += CPU_cycle[j]
            turn_around[j] = count# - Arrival_time[j]  # 종료시간-도착시간
            CPU_cycle[j] = 0 #0으로 만들어줘서 더 돌지 않도록 함.
            print("%4s %7s"%(Job_name[j],  CPU_cycle[j]))
            print('-----------------')
        elif CPU_cycle[j] != 0: #남은 작업량이 0이 아니면
            if j != 0 and count < Arrival_time[j]: #작업의 도착시간이 타임퀀텀+현재진행시간보다 클때.
                while 1: #다음작업 도착시간까지
                    if count > Arrival_time[j] or count == Arrival_time[j]:
                        break
                    elif CPU_cycle.count(0) == j and count < Arrival_time[j]:
                        move_turtle(90, Time_quantum * 70)
                        move_turtle(90, Time_quantum * 20)
                        turtle.fd(Time_quantum * 70)

                        xcor = turtle.xcor()
                        ycor = turtle.ycor()

                        write_time(xcor, ycor - 20, count)
                        write_job_name(xcor, ycor, "대기시간", 90)
                        move_turtle(90, Time_quantum * 20)
                        turtle.fd(Time_quantum * 70)
                        count = Arrival_time[j]
                    else:
                        for i in range(0,j):
                            if turn_around[i] == 0 and CPU_cycle[i] < Time_quantum:
                                move_turtle(90, CPU_cycle[i] * 15 + 10)
                                move_turtle(90, Time_quantum * 20)
                                turtle.fd(CPU_cycle[i] * 15 + 10)

                                xcor = turtle.xcor()
                                ycor = turtle.ycor()

                                write_time(xcor, ycor - 20, count)
                                write_job_name(xcor, ycor, Job_name[i], 90)
                                move_turtle(90, Time_quantum * 20)
                                turtle.fd(CPU_cycle[i] * 15 + 10)
                                count += CPU_cycle[i]
                                turn_around[i] = count  # - Arrival_time[j]  # 종료시간-도착시간
                                CPU_cycle[i] = 0  # 0으로 만들어줘서 더 돌지 않도록 함.
                                print("%4s %7s" % (Job_name[i], CPU_cycle[i]))
                                print('-----------------')
                            elif count > Arrival_time[j]:
                                break
                            else:
                                CPU_cycle[i] = CPU_cycle[i] - Time_quantum
                                print("%4s %7s" %(Job_name[i], CPU_cycle[i]))
                                print('-----------------')

                                move_turtle(90, (Time_quantum * 20))
                                move_turtle(90, (Time_quantum * 20))
                                turtle.fd(Time_quantum * 20)

                                xcor = turtle.xcor()
                                ycor = turtle.ycor()

                                write_time(xcor, ycor-20, count)
                                write_job_name(xcor, ycor, Job_name[i], 90)
                                move_turtle(90, (Time_quantum * 20))
                                turtle.fd(Time_quantum * 20)
                                count += Time_quantum

                                if CPU_cycle[i] == 0:  # 만약 남은 작업량이 0이면
                                    turn_around[i] = count# - Arrival_time[i]  # 반환시간을 저장.
                CPU_cycle[j] = CPU_cycle[j] - Time_quantum
                print("%4s %7s" % (Job_name[j], CPU_cycle[j]))
                print('-----------------')

                move_turtle(90, Time_quantum * 20)
                move_turtle(90, Time_quantum * 20)
                turtle.fd(Time_quantum * 20)

                xcor = turtle.xcor()
                ycor = turtle.ycor()

                write_time(xcor, ycor - 20, count)
                write_job_name(xcor, ycor, Job_name[j], 90)
                move_turtle(90, Time_quantum * 20)
                turtle.fd(Time_quantum * 20)
                count += Time_quantum
                if CPU_cycle[j] == 0:  # 만약 남은 작업량이 0이면
                    turn_around[j] = count# - Arrival_time[j]  # 반환시간을 저장.
            else:
                CPU_cycle[j] = CPU_cycle[j] - Time_quantum
                print("%4s %7s" % (Job_name[j], CPU_cycle[j]))
                print('-----------------')

                move_turtle(90, Time_quantum * 20)
                move_turtle(90, Time_quantum * 20)
                turtle.fd(Time_quantum * 20)

                xcor = turtle.xcor()
                ycor = turtle.ycor()

                write_time(xcor, ycor-20, count)
                write_job_name(xcor, ycor, Job_name[j],90)
                move_turtle(90, Time_quantum * 20)
                turtle.fd(Time_quantum * 20)
                count += Time_quantum

                if CPU_cycle[j] == 0:#만약 남은 작업량이 0이면
                    turn_around[j] = count# - Arrival_time[j] #반환시간을 저장.
                    print(turn_around[j])

    print("\n\n")

turtle.rt(90)
turtle.fd(Time_quantum * 20 + 20)
turtle.write(count,False,"right",("",10))

for i in range(len(turn_around)):#평균 반환시간 구하기
    Average_turn_around += turn_around[i]
    Average_turn_around -= Arrival_time[i]
Average_turn_around = float(Average_turn_around / len(line))


for i in range(len(turn_around)):
    xcor = turtle.xcor()
    ycor = turtle.ycor()
    turtle.color('blue')
    if i==0:
        turtle.penup()
        write_time(xcor, ycor - 80, "작업의 반환시간 = 종료시간 - 시작시간")
        write_time(xcor, ycor-100, "작업 [1]의 반환시간 = " + str(turn_around[0]) + " - " + str(Arrival_time[0] ) + " = " +
                   str(turn_around[0] - Arrival_time[0]))
    elif i==len(turn_around) - 1:
        turtle.penup()
        write_time(xcor, ycor - 30, "작업" + str([i + 1]) + "의 반환시간 = " + str(turn_around[i]) + " - " + str(Arrival_time[i]) +
                   " = " + str(turn_around[i] - Arrival_time[i]))
        turtle.color('red')
        write_time(xcor, ycor - 50, "---------------------------")
        write_time(xcor, ycor - 70, "평균 반환시간 = " + str(Average_turn_around))
    else:
        turtle.penup()
        write_time(xcor, ycor - 30, "작업" + str([i + 1]) + "의 반환시간 = " + str(turn_around[i]) + " - " + str(Arrival_time[i]) +
                   " = " + str(turn_around[i] - Arrival_time[i]))


f.close()
turtle.mainloop()

