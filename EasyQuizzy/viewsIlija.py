#Ilija Miletić 2021/0335
import html
import json
import random
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *
from .viewsPetar import grading_question
from .views_guest_and_reg import myRole, questionOfTheDay
from .stickers import leftAdmin, rightAdmin, leftRegistered, rightRegistered, leftModerator, rightModerator


def answer(request):
    """
    Funkcija koja se poziva kada se pri izradi testa da odgovor na pitanje
    :param request:
    :return:
    """

    if request.method == "POST":

        choice = request.POST.get("answer_choice")
        answer_text = request.POST.get("answer_text" + str(choice))
        question_text = request.POST.get("question_text")
        question = Pitanje.objects.get(tekst_pitanja=question_text)

        if answer_text == question.tacan_odgovor:
            request.session['number_won_points'] += 1

        answers = [request.POST.get("answer_text" + str(0)), request.POST.get("answer_text" + str(1)),
                   request.POST.get("answer_text" + str(2)), request.POST.get("answer_text" + str(3))]

        correct = 4
        for i in range(4):
            if answers[i] == question.tacan_odgovor:
                correct = i
                break

        timer = request.POST.get("timer")

        request.session['question_text'] = question_text
        request.session['answers'] = answers
        request.session['timer'] = timer
        request.session['choice'] = choice
        request.session['correct'] = correct

        return redirect('answer_GET')


def answer_GET(request):
    """
    Funkcija koja obezbeđuje da ne može da se vara na testu reload-ovanjem stranice
    :param request:
    :return:
    """

    return render(request, "EasyQuizzy/answered_singleplayer.html",
                  {'korIme': request.session['korIme'],
                   'number_current_question': request.session['number_current_question'],
                   'question_text_content': request.session['question_text'],
                   'answers': request.session['answers'],
                   'half_half_used': request.session['half_half_used'],
                   'replacement_question_used': request.session['replacement_question_used'],
                   'points': request.session['number_won_points'],
                   'timer': request.session['timer'],
                   'choice': request.session['choice'],
                   'correct': request.session['correct']})


def load_grading(request):
    """
    Funkcija kojom se prelzi na ocenjivanje pitanja
    :param request:
    :return:
    """

    if request.method == "POST":

        if (request.session['role_user'] != 'guest'):
            return render(request, "EasyQuizzy/question_grading.html",
                          {"question_text_content": request.session['question_text']})
        else:
            return redirect(grading_question)


def fifty_fifty(request):
    """
    Funkcija koja poziva pomoć "pola-pola"
    :param request:
    :return:
    """

    if request.method == "POST":

        request.session['half_half_used'] = True

        question_text = request.POST.get("question_text")
        correct_answer = Pitanje.objects.get(tekst_pitanja=question_text).tacan_odgovor

        answers = [request.POST.get("answer_text" + str(0)), request.POST.get("answer_text" + str(1)),
                   request.POST.get("answer_text" + str(2)), request.POST.get("answer_text" + str(3))]

        incorrect = []
        for i in range(4):
            if answers[i] != correct_answer:
                incorrect.append(i)

        disable1 = random.randint(0, 1)
        disable2 = (disable1 + 1 + random.randint(0, 1)) % 3
        disable1 = incorrect[disable1]
        disable2 = incorrect[disable2]

        correct_incorrect_data = list(zip(answers, [0, 0, 0, 0]))

        timer = request.POST.get("timer")

        request.session['question_text'] = question_text
        request.session['correct_incorrect_data'] = correct_incorrect_data
        request.session['timer'] = timer
        request.session['disable1'] = disable1
        request.session['disable2'] = disable2

        return redirect('fifty_fifty_GET')


def fifty_fifty_GET(request):
    """
    Funkcija koja obezbeđuje da ne može da se vara na testu reload-ovanjem stranice
    :param request:
    :return:
    """

    return render(request, "EasyQuizzy/test_singleplayer.html",
                  {'korIme': request.session['korIme'],
                   'number_current_question': request.session['number_current_question'],
                   'question_text_content': request.session['question_text'],
                   'correct_incorrect_data': request.session['correct_incorrect_data'],
                   'half_half_used': request.session['half_half_used'],
                   'replacement_question_used': request.session['replacement_question_used'],
                   'points': request.session['number_won_points'],
                   'timer': request.session['timer'],
                   'disabled': [request.session['disable1'], request.session['disable2']]})


def replace(request):
    """
    Funkcija kojom se poziva pomoć "zamena pitanja"
    :param request:
    :return:
    """

    request.session['replacement_question_used'] = True
    replacement_question = json.loads(request.session['replacement_question'])

    correct_incorrect_layout_answers = [replacement_question['tacan_odgovor'], replacement_question['netacan1'],
                                        replacement_question['netacan2'], replacement_question['netacan3']]
    random.shuffle(correct_incorrect_layout_answers)
    request.session['correct_incorrect_layout_answers'] = correct_incorrect_layout_answers

    correct_incorrect_layout_indicators = []
    for ans in correct_incorrect_layout_answers:
        if ans == replacement_question['tacan_odgovor']:
            correct_incorrect_layout_indicators.append(1)
        else:
            correct_incorrect_layout_indicators.append(0)

    correct_incorrect_data = list(zip(correct_incorrect_layout_answers, correct_incorrect_layout_indicators))

    return render(request, "EasyQuizzy/test_singleplayer.html",
                  {'korIme': request.session['korIme'],
                   'number_current_question': request.session['number_current_question'],
                   'question_text_content': replacement_question['tekst_pitanja'],
                   'correct_incorrect_data': correct_incorrect_data,
                   'half_half_used': request.session['half_half_used'],
                   'replacement_question_used': request.session['replacement_question_used'],
                   'points': request.session['number_won_points'],
                   'timer': 10,
                   'disabled': [4, 4]})


# def tick(request):
#     request.session['timer'] -= 1
#     return JsonResponse({'status': 'success'})

def no_answer(request):
    """
    Funkcija koja se poziva kada istekne vreme za odgovor
    :param request:
    :return:
    """

    if request.method == "POST":

        question_text = request.POST.get("question_text")
        question = Pitanje.objects.get(tekst_pitanja=question_text)

        answers = [request.POST.get("answer_text" + str(0)), request.POST.get("answer_text" + str(1)),
                   request.POST.get("answer_text" + str(2)), request.POST.get("answer_text" + str(3))]

        correct = 4
        for i in range(4):
            if answers[i] == question.tacan_odgovor:
                correct = i
                break

        request.session['question_text'] = question_text

        return render(request, "EasyQuizzy/answered_singleplayer.html",
                      {'korIme': request.session['korIme'],
                       'number_current_question': request.session['number_current_question'],
                       'question_text_content': question_text,
                       'answers': answers,
                       'half_half_used': request.session['half_half_used'],
                       'replacement_question_used': request.session['replacement_question_used'],
                       'points': request.session['number_won_points'],
                       'timer': 0,
                       'choice': 4,
                       'correct': correct})


@login_required(login_url='login')
def question_of_the_day(request):
    """
    Funkcija koja se poziva kada se prosledi odgovor na pitanje dana
    :param request:
    :return:
    """

    if request.method != "POST":
        return redirect('main')

    answer_text = request.POST.get("odgovor")
    question_text = request.POST.get("tekst_pitanja")
    question_text = html.unescape(question_text)
    question = Pitanje.objects.filter(tekst_pitanja=question_text).get()

    correct_answer = 0
    level_passed = 0
    new_level = 0

    if answer_text == question.tacan_odgovor:
        correct_answer = 1

        user = Korisnik.objects.get(idkor=request.session['IdKor_current'])

        user.broj_poena = user.broj_poena + 5
        old_level = user.nivo
        new_level = (user.broj_poena // 10) + 1

        if new_level > old_level:
            level_passed = 1
            user.nivo = new_level

        user.save()

    request.session['correct_answer'] = correct_answer
    request.session['level_passed'] = level_passed
    request.session['new_level'] = new_level

    return redirect('question_of_the_day_GET')


@login_required(login_url='login')
def question_of_the_day_GET(request):
    """
    Funkcija koja obezbeđuje da ne može da se vara na testu reload-ovanjem stranice
    :param request:
    :return:
    """

    context = {}

    korisnik = request.user
    role = myRole(korisnik.username)

    questions = Pitanje.objects.all().order_by('-prosecna_ocena')[:3]
    template = loader.get_template('EasyQuizzy/regMainPage.html')
    bestQuestions = list()
    quest_objects = [questions]

    i = 0
    for quest in quest_objects[i]:
        quest_list = list()
        quest_list.append(i + 1)
        quest_list.append(quest.tekst_pitanja)
        quest_list.append(quest.tacan_odgovor)
        quest_list.append(quest.prosecna_ocena)
        bestQuestions.append(quest_list)
        i += 1

    tekst_pitanja, tacan, netacan1, netacan2, netacan3 = questionOfTheDay()
    odgovori = [tacan, netacan1, netacan2, netacan3]
    random.shuffle(odgovori)

    if role == 0:
        context = {
            'korIme': request.user.username,
            'vreme': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tekst_pitanja': tekst_pitanja,
            'odgovor1': odgovori[0],
            'odgovor2': odgovori[1],
            'odgovor3': odgovori[2],
            'odgovor4': odgovori[3],
            'all_questions': bestQuestions,
            'left': leftRegistered,
            'right': rightRegistered,
            'correct_answer': request.session['correct_answer'],
            'level_passed': request.session['level_passed'],
            'new_level': request.session['new_level']
        }
    if role == 1:
        context = {
            'korIme': request.user.username,
            'vreme': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tekst_pitanja': tekst_pitanja,
            'odgovor1': odgovori[0],
            'odgovor2': odgovori[1],
            'odgovor3': odgovori[2],
            'odgovor4': odgovori[3],
            'all_questions': bestQuestions,
            'left': leftModerator,
            'right': rightModerator,
            'correct_answer': request.session['correct_answer'],
            'level_passed': request.session['level_passed'],
            'new_level': request.session['new_level']
        }
    if role == 2:
        context = {
            'korIme': request.user.username,
            'vreme': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tekst_pitanja': tekst_pitanja,
            'odgovor1': odgovori[0],
            'odgovor2': odgovori[1],
            'odgovor3': odgovori[2],
            'odgovor4': odgovori[3],
            'all_questions': bestQuestions,
            'left': leftAdmin,
            'right': rightAdmin,
            'correct_answer': request.session['correct_answer'],
            'level_passed': request.session['level_passed'],
            'new_level': request.session['new_level']
        }

    return HttpResponse(template.render(context, request))
