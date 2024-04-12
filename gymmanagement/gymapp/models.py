from django.db import models

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    @classmethod
    def post_discussion(cls, title, content):
        discussion = cls(title=title, content=content)
        discussion.save()

class MealPlan(models.Model):
    plan_name = models.CharField(max_length=200)
    plan_details = models.TextField()

    @classmethod
    def share_meal_plan(cls, plan_name, plan_details):
        meal_plan = cls(plan_name=plan_name, plan_details=plan_details)
        meal_plan.save()

class Image(models.Model):
    image_file = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=200)

    @classmethod
    def post_image(cls, image_file, caption):
        image = cls(image_file=image_file, caption=caption)
        image.save()
