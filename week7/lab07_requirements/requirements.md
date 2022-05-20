Part 1 - Requirment Elicitation
C: We would want to have a new system to help students see how many many available seats there are on campus
E: Location? so in lecture hall only or for other classroom as well?
C: We would want this system in pretty much everywhere in campus, hall, classroom, gym, study room, car park etc
E: K, so does the number of seat remining has to be very specific or a approximation is good enough?
C: We would prefer to have a specific number of seat remining for lecture hall, but for the other, a rough estimation is good enough. We also want it to be accessable via different devices and it will all shown in a map format.
E: So in a map format and user could click into a specific part and know how free that area is, right?
C: yeah, and we want it to be update freqently as well, and it need to work on working hour only.
E: K, so how much are u willing to pay
C: can you do it for free
E: Fuck you, i am out

Part 2 - Requirements Analysis
- As a student I would want know if the classroom is full so that i dont have to walk in just to find out there is no space left for me.
- As a student I would want to know if the study room are free and be able to book it at advance so that me and my team could have a place to do our project without having to find a free room
- As a student I would want to know how many people in the gym, i dont want go to the gym if there is too many in there, it feel stress
- As a student I would want the system to be user friendly so that i could use it easily.
- As a student I want the system to update freqently so that the infomation is not outdate and reliable 

Part 3 - Requirements Specification
Goal in conetxt: info of seat avability in lecture hall
Scope: UNSW Streams
level: primary task
Preconditions: The user is a unsw student
Success end condition: number of seat return
Fail end condition: the number of seat fail to return
Primary actor: User
Trigger: user press the lecture hall in the map in the frondend

Scenario - detect how many seat left in a lecture hall
- Set up a student id card reader and a gate in front of the hall.
- Every student has to use the id card to get into it.
- Num of card read = num of current people in the hall
- num of seats left = total seat -  num of card read
- Sent the num of seat left to the system every 15 second
- Update the num of seat left on the system
- When user have click in the relevant area that displace info about that hall, displace the num of seat left.
- If seat left is over 50% of total seat, return a green signal and tell them that it is still really free, if it is between 50 - 90%, a yellow signal tell the user that the hall is getting full. Finally, if it is nearly full, it will displace the number of people have entered the hall and tell the user how many seat left.
- When the user left the building, they will have to scan their id card as well and num of seat left will plus 1.