# Dynamic Tutoring Website - _Tutor Me_
Students are often looking for tutors for courses. This app will help facilitate this matching.

## Table of Content:
- [Website](#website)
- [Technologies](#technologies)
- [Setup](#setup)
- [Approach](#approach)
- [Status](#status)

## Website

https://project-a-12-cs3240.herokuapp.com/


![image](https://github.com/arjuntrivedi/Dynamic-Tutoring-Website/assets/72959325/2f1a8587-bb18-45b9-95a0-56e36770e8f7)
![image](https://github.com/arjuntrivedi/Dynamic-Tutoring-Website/assets/72959325/22fd3dd8-daa5-42ce-9e8b-8a2f9acd0119)
![image](https://github.com/arjuntrivedi/Dynamic-Tutoring-Website/assets/72959325/3581dfa3-6966-4878-bfd4-f7992aafcf61)
![image](https://github.com/arjuntrivedi/Dynamic-Tutoring-Website/assets/72959325/b09280c6-373e-49dd-ab75-fe1ac0a5a84f)
![image](https://github.com/arjuntrivedi/Dynamic-Tutoring-Website/assets/72959325/588a93c0-19fa-412a-9a64-170a4939339f)
![image](https://github.com/arjuntrivedi/Dynamic-Tutoring-Website/assets/72959325/1d922330-cd01-4ed4-9b77-c2538fe2de64)


## Technologies
I used `HTML/CSS`, `Bootstrap`, `JavaScript`, `Django`, `Heroku`, `GitHub Actions`, and `Google API`

## Setup
- Click the website URL
- Sign in with Google and select status as either a student or tutor
- If tutor is chosen, select hourly rate, classes to tutor, and available time frames
- If student is chosen, search courses to determine tutor availability
- Create multiple accounts and submit various requests to view the website's dynamic features


## Approach
  1. **Requirements:** I identified the required components that the users wanted. The technical components included using Google authentication API to create profiles and querying data from the UVA course list API. The system components included allowing students and tutors to look up desired courses, tutors to set up hourly wage and availability, and students to submit tutoring requests that the tutor could accept/reject. 
  2. **Design:** Before coding, I needed to determine _how_ the system would be created. I chose to create objects (Django models) for students, tutors, and courses, due to their significant relationships in the system. The system also followed the Model-View-Controller pattern through Django. Because this was a dynamic website, I visualized the user story of students and tutors and designed business logic methods (Django views.py file), specifically redirects for every action performed by the user. 
  3. **Implementation:** To create the project, I first connected the GitHub repository to the Heroku cloud platform, which hosted the website and Postgres database. When developing the system, the Django framework allowed for smooth separation of concerns between the front-end, business logic, and database work. I thoroughly worked on each of the three layers to create a polished, scalable product.
  4. **Testing** Django unit tests and GitHub Actions Continuous Integration were used to discover bugs in the website and possible deployment issues.

## Status
The website is complete and ready for use!
