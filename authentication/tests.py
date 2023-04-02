from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class AuthViewsTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser'
        self.email = 'testuser@email.com'
        self.password = 'pa$sw0rd'

    
    def test_login_page(self):
        """
            Test if the login page is showing up for none loged users and that the page shows the right information.
        """
        response = self.client.get(reverse("auth:login"))

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "Login page")

    def test_sign_up_page(self):
        """
            Test if the sign-up page is showing up for none loged users and that the page shows the right information.
        """
        response = self.client.get(reverse("auth:sign-up"))

        self.assertEquals(response.status_code, 200)

        self.assertContains(response, "Registration page")

    def test_home_redirect_to_login(self):
        """
            If a user is not authenticated, the home page should redirect towards the login page.
        """
        response = self.client.get(reverse("auth:home"))

        self.assertRedirects(response, reverse("auth:login")+"?next="+reverse("auth:home"))

    def test_sign_up_view_valid(self):
        """
            If the registration information are correct the user should get loged in and redirected to the home page.
        """
        response = self.client.post(reverse("auth:sign-up"), {"username": self.username, "email": self.email, "password1": self.password, "password2": self.password})

        self.assertRedirects(response, reverse("auth:home"))






class AuthTemplateTests(TestCase):
    def test_index_page(self):
        """
            Test if the content of the index page is complete.
        """
        response = self.client.get(reverse("auth:login"))