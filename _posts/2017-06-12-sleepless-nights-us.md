---
layout: post
title:  Sleepless nights in the US
date:   2017-12-06
image:  images/blog4/cover.jpg
tags:   work autonomous vehicle car robotics self-driving igvc usa
---
It was a fantasy for almost everyone in the team to visit the States at least once in their life. I was all curious to see for myself as to what makes it so desirable: the free enterprise? the liberties that people enjoy? Well whatever it is.. we were on our journey to the US, half way across the globe from India! We didn't have to face the difficulties of Columbus for we had huge steel crafts carrying us by air this time. By team here, I mean Team Abhiyaan, the robotics team from IIT Madras who are self-driven to make self-drives. I was lucky to be a part of such a wonderful and fun team.

For the context here, Team Abhiyaan was set to participate in the Intelligent Ground Vehicle Competition, the largest Unmanned Ground Vehicle Competition for University Students happening in Oakland University, Detroit city, Michigan. To be honest, we were unsure whether we'll be participating this year, given we had the Computer Vision (CV) module of the robot incomplete. The frustrated head Ramana goes, "I wanted the flight tickets to be reserved only after I saw the first costmap from lane detection and now somehow we have them booked already. It's all gonna go in vain..". Everyone in the room could sense the disappointment in his tone. But magic happened the night before we left to the airport. 

One last night-out we thought, toiling through the night with the will of finishing the lane detection part. It was 3:40 AM when that happened! The first look of static map built with the point-cloud data from CV and costmap inflation around it in RViz. I screamed in joy as co-team head was committing the changes in cv branch in gitlab. I was hasty in sharing screenshots of the brief moment of triumph in the team's whatsapp group. Alas, we had a chance at the competition. 

The trip to US seemed like an another episode of Breaking Bad to be honest. From smuggling (in our terms) the explosive Lithium Polymer batteries to getting drunk in the plane, we had it all. To our surprise, the luggage check at New Delhi and Chennai was stringent than the US customs. Now zoom out from an ever more South Indian place like Chennai and zoom into an American dream city like Detroit. Well coincidence is that Chennai is called the Detroit of Asia due to the boom of Auto Industry. States was much better than I imagined: wide welcoming streets, lush green grass near the sidewalk, the cold sun, uniform house designs and like cherry on top of all this, no traffic congestion. Warmth of people in US was much better than the warmth of Chennai (which should actually be described as unforgiving heat). The spell of Pizza and McD every corner made me forget the delicious Dosa and sambar for a week. 

"Where is Alan key number 4?", this was all the screaming I heard through the first two days of stay at Comfort Suites. Who knew that the assembly of the robot would take two full days even after holding facetime with the mechanical team back in India! We were frustrated that two days went by and that we were just working on screwing and bolting and turning and juggling with the aluminium extrusion channels. It was a miracle that we put on those gears on place. This is how we made it look after two and half days of slaving away.

Once the bot was assembled, the worst cases scenarios started sprouting one by one. There was no Differential GPS satellites in our arena. We reset the entire configuration to somehow get 19cm accuracy in latitude. We qualified the simple course on day 3! That was simple we thought, while the bigger problems were swallowing us whole. The transform between UTM[^1]  (Universal Transverse Mercator) and the bot specific map frame was now trembling like a blistered lightning in the sky. This problem kept us awake dawn and dusk, we couldn't tell the difference. The theme of night-out was just set for us in those dim-lit yellow striped tents in the campus (cover of the blog). We slaved away for three full days trying to figure out a solution. The cold nights were just too cruel. The hot solder rod now had dew drops on it. We used the heat gun to keep our hands from freezing and becoming numb. My overheating laptop running Ubuntu, finally had relief in those cold crazy nights. 

The solution finally dawned upon us on the fourth night when we everyone was sitting on the grass grounds, having lost all the hope. The team lead came up with a code that takes the IMU[^2]  (Inertial Measurement Unit) generated Quaternions and origin with respect to UTM frame and transformed the GPS waypoints into the simple bot specific map co-ordinates. Our code for localization and mapping was more robust than the default package which did the job! (navsat_mapping).

You'd think we'd had it enough right? But no, that's where you're wrong my sweet summer child! The Computer Vision code for lane detection was.. well, computationally expensive. Because of that, our costmap update was at snail's pace. We had a 7th Gen Intel NUC[^3]  (Next Unit of Computing) burning its transistors for processing the camera feed. We had to tune a lot of parameters to decrease the computational load including compromising on the costmap dimensions, adopting the less expensive path planning algorithms and decreasing the speed of the robot. With all that jugaad work, we did enter into the heat but that was the last day for AutoNav challenge, we either run this heat or we lose it.

![team](/images/blog4/3.jpeg)
*Kernel 1.0 running the heats*

There it was, our bot ready in the arena, gloriously with the backdrop of all the effort, making it stand where it is right now. The judges took the remote from us. At the press of the start button we ran the code, out spit the error info by the bot on the terminal: 
```
[INFO]: LIDAR failed
[INFO]: Sparton IMU died
[INFO]: Camera feed not found
```
\
We all had our eyes welled up. We retrieved the bot immediately from the arena. We found the loose connection in the internal circuitry and fixed it instantly. Damn! That was one good show you freaking robot, we thought. We ran it again and this time the bot had a blind spot on the field and it started turning right since it detected no lane to its immediate right. That's it. We didn't qualify the minimum speed requirement. But we figured the problem just by looking at the costmap. It was the camera; it's position was aligned at a higher angle which paved way for the blind spot.

Alas we didn't get another chance to run, since it was the end of heats. If only we had been given one more chance!  We ran the bot by turning the camera down and pushing it one meter initially, after the heats and it ran perfectly. However, it was too late by then; the competition had ended. But the relief that, we did actually solve one of the most challenging problems of the century prevailed with us till we left the States. This is us with the bot, standing proud next to the tricolor.

![team](/images/blog4/2.jpg)
*The team with the robot in front of the tricolor*


[^1]: UTM - The Universal Transverse Mercator (UTM) conformal projection uses a 2-dimensional Cartesian coordinate system to give locations on the surface of the Earth. 
[^2]: IMU - The Inertial Measurement Unit is nothing but a gyroscope/accelerometer that gives the yaw, pitch and roll information of the bot when attached to it.
[^3]: NUC - Next Unit of Computing (NUC) is a small-form-factor personal computer designed by Intel.