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


## Technologies
I used `HTML/CSS`, `Bootstrap`, `JavaScript`, `Django`, `Heroku`, `GitHub Actions`, and `Google API`

## Setup
- Click the website URL
- Sign in with Google and select status as either a student or tutor
- If tutor is chosen, select hourly rate, classes to tutor, and available time frames
- If student is chosen, search courses to determine tutor availability
- Create multiple accounts and submit various requests to view the website's dynamic features


## Approach
  1. **Requirements:** I identified the required components that the users wanted. This included using Google authentication API to create profiles, querying data from the UVA course list API, allowing students and tutors to look up desired courses, allowing tutors to set up up hourly wage and availability anytime, and allowing students to submit tutoring requests that the tutor can accept/reject. 
  2. **Design:** Before coding, I needed to determine _how_ the system would be created. I chose to create objects (Django models) for students, tutors, and courses, due to their significant relationships in the system. The system also followed the Model-View-Controller pattern through Django. Because this was a dynamic website, I visualized the user story of students and tutors and designed business logic methods (Django views.py file), specifically redirects for every action performed by the user. 
  3. **Implementation:** To create the project, I first connected the GitHub repository to the Heroku cloud platform, which hosted the website and Postgres database. When developing the system, the Django framework allowed for smooth separation of concerns between the front-end, business logic, and database work. I thoroughly worked on each of the three layers to create a polished, scalable product.
  4. **Testing** Django unit tests and GitHub Actions Continuous Integration were used to discover bugs in the website and possible deployment issues.

## Status
The website is complete and ready for use!
