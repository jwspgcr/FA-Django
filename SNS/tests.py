import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import CustomUser, Post, Repost


def create_user(name):
    return User.objects.create(username=name, password="aaa")


def create_customuser_from_user(user):
    return CustomUser.objects.create(user=user, bio="")


def create_customuser(name):
    return create_customuser_from_user(create_user(name))


def create_post(author, text, days=None):
    if days is None:
        return Post.objects.create(author=author, text=text)

    time = timezone.now() + datetime.timedelta(days=days)
    return Post.objects.create(author=author, text=text, pub_date=time)


def create_repost(repostedBy, post, days=None):
    if days is None:
        return Repost.objects.create(repostedBy=repostedBy, post=post)

    time = timezone.now() + datetime.timedelta(days=days)
    return Repost.objects.create(repostedBy=repostedBy, post=post,
                                 pub_date=time)


class HomePostTests(TestCase):
    # 自分のポストを表示する
    def test_show_my_post(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)

        create_post(cuserA, "userA's post")

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], ["<Post: userA>"])

    # フォローしている他ユーザーのポストを表示する
    def test_show_if_I_follow(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)
        cuserB = create_customuser("userB")

        cuserA.followers.add(cuserB)
        cuserA.save()

        create_post(cuserB, "userB's post")

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], ["<Post: userB>"])

    # フォローしていない他ユーザーのポストを表示しない
    def test_not_show_if_not_I_follow(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)
        cuserB = create_customuser("userB")

        create_post(cuserB, "userB's post")

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], [])

    # フォローしている他ユーザーがリポストしたポストを表示する
    def test_show_if_my_followers_repost(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")

        post = create_post(cuserC, "userC's post")

        cuserA.followers.add(cuserB)
        cuserA.save()

        cuserB.reposts.add(post)
        cuserB.save()

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], ["<Post: userC>"])

    # フォローしていない他ユーザーがリポストしたポストを表示しない
    def test_not_show_if_none_of_my_followers_repost(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")

        post = create_post(cuserC, "userC's post")

        cuserB.reposts.add(post)
        cuserB.save()

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], [])

    # 複数のポストを新しく投稿されたものから表示する
    def test_show_multiple_posts_in_latest_first_order(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)
        cuserB = create_customuser("userB")

        create_post(cuserA, "1", 1)
        create_post(cuserB, "2", 2)
        create_post(cuserB, "3", 3)
        create_post(cuserA, "4", 4)
        create_post(cuserB, "5", 5)

        cuserA.followers.add(cuserB)
        cuserA.save()

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"],
                                 ["<Post: userB>",
                                  "<Post: userA>",
                                  "<Post: userB>",
                                  "<Post: userB>",
                                  "<Post: userA>",
                                  ])

    def test_show_most_recently_reposted_post_first(self):
        userA = create_user("userA")
        cuserA = create_customuser_from_user(userA)
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")

        cuserA.followers.add(cuserB)
        cuserA.followers.add(cuserC)
        cuserA.save()

        postB=create_post(cuserB, "",days=1)
        postC=create_post(cuserC, "",days=2)
        create_repost(cuserB,postC,days=4)
        create_repost(cuserC,postB,days=5)
        create_post(cuserA,"",days=6)
        create_repost(cuserC,postC,days=7)

        self.client.force_login(userA)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"],
                                ["<Post: userC>",
                                "<Post: userA>",
                                "<Post: userB>",
                                ])
