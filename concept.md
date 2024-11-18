# ShareHW.net
## general

ShareHW.net is a web application designed to simplify homework sharing for college and high school students. It offers a collaborative platform where "captains or captain approved students" can upload homework assignments, ensuring easy access for all students in the class. The app is ideal for those who may have missed class or forgotten their homework, fostering peer-to-peer support and reducing academic stress. With a clean, intuitive design and features tailored to students' needs, ShareHW.net provides a centralized space for managing assignments, promoting organization, and enhancing communication among classmates.

## purpose:

- Easy access to homework assignments
- Peer-to-peer support
- Reduce academic stress
- fast with caching

## mention:
- when i sayes "class" it means "a indevisual class with different section and sections" such as XI-Science-A is a class 
- when i sayes "student" it means "a student of any class and section"
- when i sayes "captain" it means "a student of any class and section who is approved by admin as a captain confirming it"
 
 ## information:
 - name: ShareHW.net
 - version: 1.0.0

 ### author:
- author/developer/admin - name: Mohin Uddin Shipon
- student of Dhamrai Govt. College
- class: XI
- section: Science-B
- roll number: 241182
- github link: https://github.com/MohinUddin
- email: mohinuddinshipon10@example.com

### college:
- name: Dhamrai Govt. College
- address: Dhamrai, Dhaka, Bangladesh


## user-authentication
- role based authentication: captain, student, admin-student
- if someone signup as student then a request will be sent to captain(of current user's class) for approval. after approval student will be able to upload homeworks. without approval student will not be able to upload homeworks but can view them.
- if someone signup as captain then a request will be sent to admin for approval. after approval captain will be same as student without approval.
### Signup
- seasson timeout: 30 days
- after signup send a email to uses email with a link to confirm his/her account. cliking on the link will confirm account. (show link of the gmail when he submit signup form)

#### requirments:
- full name
- college roll number(6 digits)
- class dropdown (XI or XII)
- section dropdown (Science, Arts or Commerce with A and B subsections)
- role (strudent selected by default or captain or admin-student. extra reqiurment form will shown if captain or admin-student selected)
- new password (minimum 8 characters)

### extra requirments for admin-student, captain :
- email
- image of student id card

#### data save in database:
- full name
- college roll number (6 digits)
- class
- section
- status (approved or rejected or pending. pending by default)
- role
- email
- image of student id card
- new password (minimum 8 characters)
- submission date
- time

### Login
- seasson timeout: 30 days
- forget password functonality: send password reset link to user's email

#### requirments:
- roll number
- password

### admin panel: 
- this pages url should not be anywhere in the website (admin will access it writing url in browser manually)
- url is: https://sharehw.net/admin
- any one can access this page but it will be blank page with only a password input field to confirm admin
- password will be: Sshiponkarimuddin
- after confirmation admin will be able to do the following
    - 
    - add new captains (only admin can add/remove as well as students )

### permission:
#### admin:
- can add captains
- can remove captains
- can add students
- can remove students
- can do everything

#### captains:
- can view all homeworks
- can upload homeworks
- can approve student's account to upload homework
- can access captain-dashboard for only his class. where all pending students will be shown and he can approve them, or can reject them.also he can see all students list of his class and their profile 
- only captain can add notes

#### students(captain approved):
- can upload homeworks
- can view all homeworks


### students (pending or rejected stutas):
- can view all homeworks

## Homewirk:

#### Homework upload form:
- subject dropdown (common subjects: Bangla, English, ICT. Science subjects: Physics, Chemistry, Biology, Mathematics. Arts subjects: Economics, Geography, History, Political Science. commerce subjects: Accounting, Economics, Management, Statistics)

- Teacher name
- description
- due date (up comming date are not allowed, only past 8 days are allowed)
- attuchments (max file size: 8MB per file)
- submit
(student name, roll number, class, section, submission date, time will be added automatically.)

#### Homework save in database:
- subject
- teacher name
- description
- due date
- attuchments (must. max file size: 8MB per file)
- student name
- student roll number
- student class
- student section
- submission date, time
- likes (0 by default)
- dislikes (0 by default)
- comments (0 by default)

## comments:
- student can add comments

### homeworks find:
- all the hmoneworks of last three days will be shown as a small card including subject, teacher name, likes, dislikes and comments count as icons, student name(who uploaded). clicking on the card will show the full details of the homework.

- stuents can find by date. (upcoming date are not allowed,past all days are allowed. take necessary information to find homeworks such as class and section from current user data to show only his class homeworks)

- student can also find homeworks of different class and section by selecting it from "different class" dropdown.


## notes:
- only captain can upload notes.
### notes upload form:
- subject dropdown (of current user class, section)
- teacher name (optional)
- title
- description(optional)
- attuchments (must. max file size: 8MB per file)
- submit

### notes save in database:
- subject
- teacher name
- title
- description(optional)
- attuchments(must. max file size: 8MB per file)
- student name
- student roll number
- student class
- student section
- submission date, time
- likes (0 by default)
- dislikes (0 by default)
- comments (0 by default)

### notes find:
- all student can see notes of their class and section also anather class notes selecting from "different class" dropdown.
- all student can also find notes by subject.

## UI/UX:
- clean and simple design
- color only black and white
- minimalistic
- using bootstrap
- using icons
- responsive design
- facebook like design and layout
- easy to use
- primaryly for mobile
- sidebar navigation in large screen 
- light and dark mode
- animated elements
- header with icon in right corner
- logo in left corner of header. text "Dhamrai Govt. College" with logo for larg screen
- footer as minimistic as possible
- a dot in the captain-dashboard navigation showing number of pending students for only captains

## technology:
- html
- css
- bootstrap
- javascript
- python
- Flask
- github
