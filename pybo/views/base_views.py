from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from pybo.models import Question, Answer


#기본 관리

# index함수 추가



def index(request):
    # pybo 목록 출력
    
    # 입력 인자
    page = request.GET.get('page', '1')     # 페이지
    kw = request.GET.get('kw', '')          # 검색어
    so = request.GET.get('so', 'recent')    # 정렬기준
    
    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')       # 작성한 날짜 역순으로 출력
    # annotate 함수 : 임시로 필드를 추가해 줌.
    # order_by 에 두 개 이상의 인자가 전달되는 경우 첫 번째 항목부터 우선순위를 매긴다

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |                              # 제목 검색
            Q(content__icontains=kw) |                              # 내용 검색
            Q(author__username__icontains=kw) |                     # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)               # 답변 글쓴이 검색
        ).distinct()                                                # 조회 결과의 중복을 없애줌줌
       #icontains -> 대소문자 구분 없이 찾아줌. contains는 구분함.

    #페이징 처리
    paginator = Paginator(question_list, 10)        #페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)
#render 함수 : context에 있는 Question모델 데이터 question_list를 pybo/question_list.html파일에 적용하여 HTML코드로 변환한다
#pybo/question_list.html과 같은 파일을 템플릿이라 부른다. 템플릿은 장고이 태그를 추가로 사용할 수 있는 html파일이라 생각하면 된다
#HttpResponse : 페이지 요청에 대한 응답을 할 때 사용하는 장고클래스
#여기서 request는 장고에 의해 자동으로 전달되는 Http 요청 객체

def detail(request, question_id):
    # pybo 내용 출력
    # 입력 인자
    question = get_object_or_404(Question, pk=question_id)

    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recommend')  # 정렬기준, default 는 추천순, 추천순/최신순 가능

    # 정렬
    if so == 'recommend':
        answer_list = Answer.objects.annotate(
            num_voter=Count('voter')).filter(question=question).order_by('-num_voter', '-create_date')
    else:
        answer_list = Answer.objects.filter(question=question).order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(answer_list, 3)  # 페이지당 3개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj, 'page': page, 'so': so}
    return render(request, 'pybo/question_detail.html', context)
