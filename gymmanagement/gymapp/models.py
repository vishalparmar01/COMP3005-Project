from django.db import models

# class Member(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     fitness_goal = models.CharField(max_length=100)

#     @classmethod
#     def register(cls, name, email, password, fitness_goal):
#         member = cls(name=name, email=email, password=password, fitness_goal=fitness_goal)
#         member.save()