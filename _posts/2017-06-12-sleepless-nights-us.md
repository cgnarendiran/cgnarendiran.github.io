---
layout: post
title:  Sleepless nights in the US
date:   2017-12-06
image:  images/blog4/cover.jpg
tags:   work autonomous vehicle car robotics self-driving igvc usa
---
It was a dream for almost everyone in the team to visit the States. I was all curious to see for myself as to what makes it so desirable: the free enterprise? the liberties that people enjoy? Well whatever it was.. we were en route to America, half way across the world from India! By team here, I mean the team Abhiyaan, the robotics team from IIT Madras who are self-driven to make self-drives. I was fortunate to be part of such a wonderful and fun group.

For the context here, Team Abhiyaan was set to participate in the Intelligent Ground Vehicle Competition (IGVC), the largest Unmanned Ground Vehicle Competition for University Students happening in Oakland University, Detroit city, Michigan US. To be honest, we were unsure whether we'd be participating that year, given we had the Computer Vision (CV) module of the robot incomplete. The frustrated head Ramana goes, "I wanted the flight tickets to be reserved only after I saw the first costmap from lane detection and now somehow we have them booked already. It's all gonna go in vain..". Everyone in the room could sense the disappointment in his tone. But magic happened the night before we left to the airport. 

One last night-out we thought, toiling through the night with the will of finishing the lane detection part. It was 3:40 AM when that happened! The first look of static map built with data from CV module and costmap inflation around it in RViz. I screamed in joy as the co-team head was committing the changes in gitlab. I was hastily sharing screenshots of the brief moment of triumph in the team's whatsapp group. Alas, we had a chance at the competition. 

The trip to US felt like an episode of Breaking Bad. From smuggling (in our terms) the explosive Lithium Polymer batteries to getting drunk in the plane, we had it all. To our surprise, the luggage check at New Delhi and Chennai was stringent than the US customs. Now zoom out from an ever more South Indian place like Chennai and zoom into an American city like Detroit. Well coincidence is that Chennai is called the Detroit of Asia due to the boom of Auto Industry. The States was much better than I imagined: wide welcoming streets, lush green grass on the sidewalk, the cold sun, uniform house designs and like cherry on top of all this, no traffic congestion. The warmth of people in US (almost everyone said hello :)) was much better than the warmth of Chennai (which should actually be described as unforgiving heat). The spell of Dominoes and McD every corner made me forget the delicious dosa and sambar for a week. 

"Where is Alan key number 4?", this was all the screaming I heard through the first two days of stay at Comfort Suites, Michigan. Who knew that assembly of the robot would take two full days even after countless facetimes with the mechanical team back in India! We were frustrated that two days went by and that we were just working on screwing and bolting and turning and juggling with the aluminium extrusion channels. It was a miracle that we put on those gears in place. 

Once the bot was assembled, the worst cases scenarios started sprouting one by one. There was no Differential GPS satellites in our arena and we had to reset the entire configuration. We had to reset a lot of parameters to make the robot work in a new environment with open arena grassland. We managed to pass the qualifier course on day 3. That was simple we thought, while the bigger problems were swallowing us whole. The transform between UTM[^1]  (Universal Transverse Mercator) and the bot specific map frame was now trembling like a blistered lightning in the sky. This problem kept us awake dawn and dusk, we couldn't tell the difference. The theme of night-out was just set for us in those dim-lit yellow striped tents in the campus (cover of the blog). We slaved away for three full days trying to figure out a solution. The cold nights were just too cruel. The hot solder rod now had dew drops on it. We used the heat gun to keep our hands from freezing and becoming numb. My overheating laptop running Ubuntu, finally had relief in those cold crazy nights. 

The solution finally dawned upon us on the fourth night when we everyone was sitting on the grass grounds, having lost all the hope. The team lead came up with a code that successfully transformed the GPS waypoints into the simple bot specific map co-ordinates and this localization was more robust than the default package which did the job! (navsat_transform_node).

You'd think we'd had it enough right? But no! The CV code for lane detection was.. well, computationally expensive. Because of that, our costmap update was at snail's pace. We had a 7th Gen Intel NUC[^2]  (Next Unit of Computing) burning its transistors for processing the camera feed. We had to tune a lot of parameters to decrease the computational load including compromising on the costmap dimensions, adopting the less expensive path planning algorithms and decreasing the speed of the robot. With all that jugaad work, we did enter into the Heats but that was the last day for AutoNav challenge, we either run it in this Heats or we lose it.

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

Alas we didn't get another chance to run, since it was the end of Heats. If only we had been given one more chance!  We ran the bot by turning the camera down and pushing it one meter initially after the Heats and it ran perfectly. However, it was too late by then; the competition had ended. But the relief that, we came such a long way amongst all the odds as a team and actually manage to solve one of the most challenging problems prevailed with us till we left the States. This is us with the bot, standing proud next to the tricolor.

![team](/images/blog4/2.jpg)
*The team with the robot in front of the tricolor*


[^1]: UTM - The Universal Transverse Mercator (UTM) conformal projection uses a 2-dimensional Cartesian coordinate system to give locations on the surface of the Earth. 
[^2]: NUC - Next Unit of Computing (NUC) is a small-form-factor personal computer designed by Intel.