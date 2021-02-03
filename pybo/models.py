from django.db import models
from django.contrib.auth.models import User
# Create your models here.
"""
모델이 생성,변경된 경우 migrate 명령을 통해 테이블을 생성해주어야 함.
migrate를 통해 테이블을 생성하기 위해서는 테이블 작업 파일이 필요
이를 위해 makemigrations를 해주어야 함.
"""


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    # null=True : modify_date 칼럼에 null을 허용한다는 의미, 
    # blank=True 는 form.is_valid()를 통한 입력 폼 데이터 검사 시 값이 없어도 된다는 의미
    # 즉 null=True, blank=True 는 어떤 조건으로든 값을 비워둘 수 있음을 의미한다

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #ForeignKey : 다른 모델과의 연결, on_delete = : 질문이 삭제되면 연결된 답변도 함께 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
