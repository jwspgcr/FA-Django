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
    def setUp(self):
        self.userA=User.objects.create(username="userA",password="aaa")
        self.cuserA=CustomUser.objects.create(user=self.userA,bio="")

        self.client.force_login(self.userA)

    # 200 OKを返す
    def test_return_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code,200)

    def test_show_my_post(self):
        create_post(self.cuserA, "userA's post")

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], ["<Post: userA>"])

    # フォローしている他ユーザーのポストを表示する
    def test_show_if_I_follow(self):
        cuserB = create_customuser("userB")

        self.cuserA.followers.add(cuserB)
        self.cuserA.save()

        create_post(cuserB, "userB's post")

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], ["<Post: userB>"])

    # フォローしていない他ユーザーのポストを表示しない
    def test_not_show_if_not_I_follow(self):
        cuserB = create_customuser("userB")

        create_post(cuserB, "userB's post")

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], [])

    # フォローしている他ユーザーがリポストしたポストを表示する
    def test_show_if_my_followers_repost(self):
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")

        post = create_post(cuserC, "userC's post")

        self.cuserA.followers.add(cuserB)
        self.cuserA.save()

        cuserB.reposts.add(post)
        cuserB.save()

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], ["<Post: userC>"])

    # フォローしていない他ユーザーがリポストしたポストを表示しない
    def test_not_show_if_none_of_my_followers_repost(self):
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")

        post = create_post(cuserC, "userC's post")

        cuserB.reposts.add(post)
        cuserB.save()

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"], [])

    # 複数のポストを新しく投稿されたものから表示する
    def test_show_multiple_posts_in_latest_first_order(self):
        cuserB = create_customuser("userB")

        create_post(self.cuserA, "1", 1)
        create_post(cuserB, "2", 2)
        create_post(cuserB, "3", 3)
        create_post(self.cuserA, "4", 4)
        create_post(cuserB, "5", 5)

        self.cuserA.followers.add(cuserB)
        self.cuserA.save()

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"],
                                 ["<Post: userB>",
                                  "<Post: userA>",
                                  "<Post: userB>",
                                  "<Post: userB>",
                                  "<Post: userA>",
                                  ])
    # リポストされたポストはリポストの日付を並べ替えに使う
    def test_order_posts_with_post_pubdate_and_repost_pubdate(self):
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")

        post=create_post(cuserC, "",days=1)
        create_post(self.cuserA,"",days=2)

        self.cuserA.followers.add(cuserB)
        self.cuserA.save()

        create_repost(cuserB,post,days=3)

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"],
                                ["<Post: userC>",
                                "<Post: userA>",
                                ])
    # 複数回リポストされたポストは最新のリポストの日付を並べ替えに使う
    # フォローしていない他ユーザーのリポスト日付は並べ替えに使わない
    def test_show_most_recently_reposted_post_first(self):
        cuserB = create_customuser("userB")
        cuserC = create_customuser("userC")
        cuserD = create_customuser("userD")

        self.cuserA.followers.add(cuserB)
        self.cuserA.followers.add(cuserC)
        self.cuserA.save()

        postB=create_post(cuserB, "",days=1)
        postC=create_post(cuserC, "",days=2)
        create_repost(cuserB,postC,days=4)
        create_repost(cuserC,postB,days=5)
        create_post(self.cuserA,"",days=6)
        create_repost(cuserC,postC,days=7)
        create_repost(cuserD,postB,days=8) # repost made by whom you don't follow

        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context["posts"],
                                ["<Post: userC>",
                                "<Post: userA>",
                                "<Post: userB>",
                                ])
