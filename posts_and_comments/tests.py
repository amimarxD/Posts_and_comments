from django.test import TestCase
from django.utils import timezone
from .models import Post
from django.urls import reverse
import datetime


# Create your tests here.

def create_post(title, description, days):
    """
        Create a post with the given `title` and `description` and published the 
         in the given number of `days` offset to now (negative for post published in the 
        past, positive for posts that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days = days)

    return Post.objects.create(title = title, description = description, created_at = time)

class PostIndexViewTests(TestCase):
    def test_no_posts(self):
        """
            If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("post:index"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No posts available")

        self.assertQuerysetEqual(response.context["latest_post_list"], [])

    def test_past_post(self):
        """
            Posts with a pub_date in the past are displayed on the index page.
        """

        post = create_post(title = "Past question", description = "Some past description about the past.", days = -30)

        response = self.client.get(reverse("post:index"))

        self.assertQuerysetEqual(response.context["latest_post_list"], [post])

    def test_future_post(self):
        """
            posts with a created_at in the future aren't displayed on the index page.
        """

        create_post(title = "Future post", description = "Some future description about the future.", days=30)

        response = self.client.get(reverse("post:index"))

        self.assertContains(response, "No posts are available")

        self.assertQuerysetEqual(response.context["latest_post_list"], [])

    def test_future_post_and_past_post(self):
        """
            Even if both past and future posts exist, only past posts are displayed.
        """

        post = create_post(title = "Past question", description = "Some past question.", days = -30)

        create_post(title = "Future post", description = "Some future question", days = 30)

        response = self.client.get(reverse("post:index"))

        self.assertQuerysetEqual(response.context["latest_post_list"], [post])

    def test_two_past_posts(self):
        """
            The posts index page may display multiple posts.
        """

        post1 = create_post(title = "Past question 1", description = "Some past question 1", days = -30)

        post2 = create_post(title = "Past question 2", description = "Some past question 2", days = -30)

        response = self.client.get(reverse("post:index"))

        self.assertQuerysetEqual(set(response.context["latest_post_list"]), set([post2, post1]))

    
