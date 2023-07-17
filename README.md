# Dynamic Tutoring Website
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
I used `HTML/CSS`, `Django`, `Heroku`, `GitHub Actions`

## Setup
- Click the website URL
- Sign in with Google and select status as either a student or tutor
- If tutor is chosen, select hourly rate, classes to tutor, and available time frames
- If student is chosen, search courses to determine tutor availability
- Create multiple accounts and submit various requests to view the website's dynamic features


## Approach
  1. **Requirements:** I identified the required components that the users wanted. This included using Google authentication to create profiles, querying data from the UVA course list API, allowing students and tutors to look up desired courses, allowing tutors to set up up hourly wage and availability anytime, and allowing students to submit tutoring requests that the tutor can accept/reject. 
  2. **Design:** Before coding, I needed to determine _how_ the system would be created. I chose to create objects (Django models) for students, tutors, and courses, due to their significant relationships in the system. Because this was a functional website, I visualized the user story of students and tutors to design methods for the middle tier (Django views.py file), specifically redirects for every action performed by the user.
  3. **Implementation:** 

## Status
The website is complete and ready for use!
