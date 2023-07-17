from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class DummyTestCase(TestCase):
    def test_dummy(self):
        x = 1
        self.assertEqual(x, 1)
    
class ViewTestCase(TestCase):
    def test_login_view(self):
        response = self.client.get("/login")
        self.assertTemplateUsed(response, "base/general_login.html")
        self.assertTemplateUsed(response, "base/general_navbar.html")
        #self.assertContains(
            #response, "Login With Google")
    
    def test_student_view(self):
        response = self.client.get("/student-home")
        self.assertTemplateUsed(response, "base/unauthorized.html")
        self.assertTemplateUsed(response, "base/general_navbar.html")
        self.assertContains(
            response, "You are not authorized as a student")
    
    def test_tutor_view(self):
        response = self.client.get("/tutor-home")
        self.assertTemplateUsed(response, "base/unauthorized.html")
        self.assertTemplateUsed(response, "base/general_navbar.html")
        self.assertContains(
            response, "You are not authorized as a tutor")
    
