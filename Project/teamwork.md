# Marking criteria for teamwork.md

* Consistent work towards the goal of a working backend.
* Task board is always up to date and reflects ongoing work
* Demonstration of appropriate use of agile practices to work effectively as a team.

# How often you met, and why you met that often

* We hosted meetings on Tuesday Nights, Thursday Nights and Saturday Mornings.
* We met this often to ensure that we were on track with what we needed to get done.

# What methods you used to ensure that meetings were successful

* All meetings we had(physical or online) followed the same structure.
* Stand Up at the beginning to cover what we have done.
* Go over certain complications or things that needed to be done(eg. user acceptance criteria).
* Followed by plans of actions for the next few days. (Thus completing the structure of a stand up)

# What steps you took when things did not go to plan during iteration to

* Conflicts between members were handled by comparing each own's solutions and determining as a team which one's fulfilled User Acceptance Criteria and provided a valid solution.
* Keeping meetings to 1 - 1.5 hours enabled us to have a collaborative workspace where ideas could be bounced back to provide a solution that fulfilled User Acceptance Criteria in a more effective way
* We took steps to ensure things did not go to plan eg. providing a buffer window at the end of the project to sift through logic and tests.
* Utilising a gaant chart to keep us motivated on the goal

**However things did go wrong and steps we took included:**
* reviewing all the logic of the given problem **(as a team or pair)**
* finding better solutions via lecture notes, stack overflow and piazza(in order of helpfulness) **(as a team or pair)**
* implementing said solutions and testing it to ensure that it satisfied individually defined verification criteria.
* and repeating said steps if the problem still persisted

# Details on how you had multiple people working on the same code

We each worked on our own separate branches and only merged with master after approval from another team member. For overlapping work, we discussed this thoroughly before starting the project so that our files didn't clash and we had minimal merge conflicts to fix. During the project, we communicated clearly and very often using a Facebook Messenger group chat. We would also often work in a video call.

# Overview after iteration-3

After iteration 2, the foundation of our backend was strong. The only things left to do was to integrate it with the front end, which required a few tweaks to the backend and to add the new functionalities according to the specs. As we used test driven development, we knew our backend functioned correctly and only had to modify it according to the frontend's needs. Because of this we already knew which segments of code we (individual members) were integrating and we worked on it on our individual branches. We consistently kept in touch with each other as we worked on our code, especially when we faced any difficulties debugging it.

We used the agile method of pair programming when we had any major halts in our debugging stage, which we found to be very effective way and it often worked well for us. We went through a series of commit logs to see where the code might have been updated incorrectly, which made us realize the importance of concise commit messages.

We also met up in person to code and work on some problems occasionally. This way we could work on the same code in a more efficient way rather than messaging back and forth.

We also communicated with each other mostly through messenger, often sending screenshots and asking each other for help or video calling. This helped us resolve our issues quite well and quite quickly.

Working on the same code in iteration 3 was pretty common due to the fact that when someone got stuck on fixing an error, they’d ask for assistance and another team member would try to debug it too. For this reason we had a strict policy to work on our own branches, and when we had to merge to master, we’d use the following strategy:
    -> Push to own branch
    -> checkout to master
    -> pull from origin master
    -> push master
    -> checkout to own branch
    -> pull origin master
    -> fix any conflicts in own branch
    -> push to own branch
    -> push to master
This let us avoid any major problems with merging in our code. And then the group member who fixed the issue will tell the others working on it what they did and if all parties are satisfied, only then they would push their code. 