# Magdalena Obradović 2021/0304
# Elena Savić 2021/0332

from django.test import TestCase,Client
from django.urls import reverse
from EasyQuizzy.models import Kategorija, Korisnik, Pitanje
import base64
import math
from django.db import connection
from EasyQuizzy.viewsIlija import answer, answer_GET, fifty_fifty

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
import json
    
    
class TestViews(TestCase):

    def setUp(self):
        client=Client()
        self.factory = RequestFactory()
        self.client=client
        self.username='igrac123'
        self.password='Psii123+'
        # self.user=get_user_model().objects.create_user(username=self.username,password=self.password)
        self.user = Korisnik.objects.create(korisnicko_ime = "admin123", lozinka = "Psii123+", ime = "admin", prezime = "admin", email = "admin@gmail.com", pol = "Z", broj_poena = "0", nivo = "0", vazeci = "1")
        Korisnik.objects.create(korisnicko_ime = "igrac123", lozinka = "Psii123+", ime = "igrac", prezime = "igrac", email = "igrac@gmail.com", pol = "Z", broj_poena = "0", nivo = "0", vazeci = "1")
        
        categories = ['Kategorija1', 'Kategorija2', 'Kategorija3']
        img_path = ['EasyQuizzy/static/css/collage3.jpg', 'EasyQuizzy/static/css/sport.jpg', 'EasyQuizzy/static/css/music.jpg']

        i = 0
        for cat in categories:
            with open(img_path[i], 'rb') as img:
                img_bytes = img.read()
            Kategorija.objects.create(naziv = cat, slika= img_bytes)

        Pitanje.objects.create(idkat = Kategorija.objects.first(), tekst_pitanja = "tekst1", tezina_pitanja = 1, tacan_odgovor = "a", netacan1 = "b", netacan2 = "c", netacan3 = "d", zbir_ocena = 0, broj_ocena = 0, prosecna_ocena = 0, status = 0)
        Pitanje.objects.create(idkat = Kategorija.objects.first(), tekst_pitanja = "teks2", tezina_pitanja = 1, tacan_odgovor = "a", netacan1 = "b", netacan2 = "c", netacan3 = "d", zbir_ocena = 0, broj_ocena = 0, prosecna_ocena = 0, status = 0)
        Pitanje.objects.create(idkat = Kategorija.objects.first(), tekst_pitanja = "tekst3", tezina_pitanja = 1, tacan_odgovor = "a", netacan1 = "b", netacan2 = "c", netacan3 = "d", zbir_ocena = 0, broj_ocena = 0, prosecna_ocena = 0, status = 0)
        Pitanje.objects.create(idkat = Kategorija.objects.first(), tekst_pitanja = "tekst4", tezina_pitanja = 1, tacan_odgovor = "a", netacan1 = "b", netacan2 = "c", netacan3 = "d", zbir_ocena = 0, broj_ocena = 0, prosecna_ocena = 0, status = 0)
        Pitanje.objects.create(idkat = Kategorija.objects.first(), tekst_pitanja = "tekst5", tezina_pitanja = 1, tacan_odgovor = "a", netacan1 = "b", netacan2 = "c", netacan3 = "d", zbir_ocena = 0, broj_ocena = 0, prosecna_ocena = 0, status = 0)
        Pitanje.objects.create(idkat = Kategorija.objects.first(), tekst_pitanja = "tekst6", tezina_pitanja = 1, tacan_odgovor = "a", netacan1 = "b", netacan2 = "c", netacan3 = "d", zbir_ocena = 0, broj_ocena = 0, prosecna_ocena = 0, status = 0)
        print(Pitanje.objects.all())

    def test_play(self):

        response = self.client.get(reverse('doing_test_button'))
        print(response)

        self.assertEqual(200,response.status_code)
        self.assertTemplateUsed(response,'EasyQuizzy/picking_choice_singleplayer_or_multiplayer.html')

    
    def test_picking_singleplayer(self):
        response = self.client.post(reverse('choice_single_multi'), {'test': 'small_single'})
        
        categories  = Kategorija.objects.all()
        images=[]  
        for cat in categories:
            images.append(base64.b64encode(cat.slika).decode())

        length_range = math.ceil((len(categories)-4)/5)
        list_images=[]
        for cat in categories:
            list_images.append((cat.idkat//5)-1)

        data = list(zip(categories,images,list_images))

        # definišemo ključeve koje očekujemo u odgovoru
        keys = ["data", "range"]
        for key in keys:
            self.assertIn(key, response.context)
        # proveravamo da li su vrednosti koje nam views vraća iste kao očekivane
        self.assertEqual(response.context['data'], data)
        self.assertEqual(response.context['range'], range(length_range))
        
        self.assertEqual(200,response.status_code)
        self.assertTemplateUsed(response,'EasyQuizzy/picking_category_number_of_questions_singleplayer.html')

    def test_picking_categories_guest(self):
        response = self.client.get(reverse('choice_single_multi_guest'), {'test': 'small_single'})
        
        categories  = Kategorija.objects.all()
        print(categories)
        images=[]  
        for cat in categories:
            images.append(base64.b64encode(cat.slika).decode())

        length_range = math.ceil((len(categories)-4)/5)
        list_images=[]
        for cat in categories:
            list_images.append((cat.idkat//5)-1)

        data = list(zip(categories,images,list_images))

        # definišemo ključeve koje očekujemo u odgovoru
        keys = ["data", "range"]
        for key in keys:
            self.assertIn(key, response.context)
        # proveravamo da li su vrednosti koje nam views vraća iste kao očekivane
        self.assertEqual(response.context['data'], data)
        self.assertEqual(response.context['range'], range(length_range))
        
        self.assertEqual(200,response.status_code)
        self.assertTemplateUsed(response,'EasyQuizzy/picking_category_number_of_questions_singleplayer.html')



    def test_answer(self):
        request = self.factory.post(reverse('answer'), {'answer_choice' : 0, "answer_text0" : 'a', "question_text": "tekst1", "answer_text1" : 'b', "answer_text2" : 'c', "answer_text3" : 'd', "timer" : 5})
        middleware = SessionMiddleware(get_response=lambda r: None)
        middleware.process_request(request)
        request.session.save()
        request.session['korIme'] = 'igrac123'
        request.session['role_user'] = 'registered'
        request.session['number_current_question'] = 1
        request.session['number_won_points'] = 0
        request.session['half_half_used'] = False
        request.session['replacement_question_used'] = False

        
        response = answer(request)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(request.session['number_won_points'], 1)

    def test_answer_get(self):
        print(Korisnik.objects.filter(idkor = 2).first())
        session = self.client.session
        session['korIme'] = 'igrac123'
        session['role_user'] = 'registered'
        session['number_current_question'] = 1
        session['half_half_used'] = False
        session['replacement_question_used'] = False
        session['question_text'] = "tekst1"
        session['timer'] = 5
        session['answers'] = ["a", "b", "c", "d"]
        session['number_won_points'] = 1
        session['correct'] = "a"
        session['choice'] = 0
        session.save()

        response = self.client.get(reverse('answer_GET'))
    
        keys = ['korIme', 'number_current_question', 'question_text_content', 'half_half_used', 'replacement_question_used', 'timer', 'points', 'choice', 'correct', 'answers']
        for key in keys:
            self.assertIn(key, response.context)
        # proveravamo da li su vrednosti koje nam views vraća iste kao očekivane
        self.assertEqual(response.context['korIme'], "igrac123")
        self.assertEqual(response.context['number_current_question'], 1)
        self.assertEqual(response.context['question_text_content'], "tekst1")
        self.assertEqual(response.context['half_half_used'], False)
        self.assertEqual(response.context['replacement_question_used'], False)
        self.assertEqual(response.context['points'], 1)
        self.assertEqual(response.context['timer'], 5)
        self.assertEqual(response.context['choice'], 0)
        self.assertEqual(response.context['correct'], "a")

    def test_load_grading(self):
        session = self.client.session
        session['question_text'] = "tekst1"
        session['role_user'] = 'registered'
        session.save()
        response = self.client.post(reverse('load_grading'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'EasyQuizzy/question_grading.html')

    def test_fifty_fifty(self):
        request = self.factory.post(reverse('fifty_fifty'), {'question_text' : "tekst1"})
        middleware = SessionMiddleware(get_response=lambda r: None)
        middleware.process_request(request)
        request.session.save()
        request.session['half_half_used'] = False

        response = fifty_fifty(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(request.session['half_half_used'], True)

    def test_no_answer(self):
        session = self.client.session
        session['korIme'] = "igrac123"
        session['number_current_question'] = 2
        session['half_half_used'] = False
        session['replacement_question_used'] = False
        session['number_won_points'] = 0
        session.save()

        response = self.client.post(reverse('no_answer'), {'question_text': "tekst1"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'EasyQuizzy/answered_singleplayer.html')

        keys = ['korIme', 'number_current_question', 'question_text_content', 'answers', 'half_half_used', "replacement_question_used", "points", "timer", "choice", "correct"]
        for key in keys:
            self.assertIn(key, response.context)
        
    def test_choice_categories(self):
        self.client.login(username= "igrac123",password="Psii123+")
        session = self.client.session
        session['role_user'] = "registered"
        session['type_game'] = "single"
        session.save()

        response = self.client.post(reverse('choice_category_question_number'), {'broj_pitanja' : 5, "dugmad" : "Kategorija1"})
        session = self.client.session

        self.assertEqual(response.status_code, 302)
        
        keys = ['number_current_question', 'current_question', 'half_half_used', 'replacement_question_used']
        for key in keys:
            self.assertIn(key, session)
        
        self.assertEqual(session['number_current_question'], 1)
        self.assertEqual(json.loads(session['current_question'])['tezina_pitanja'], 1)
        self.assertEqual(json.loads(session['current_question'])['tacan_odgovor'], "a")
        self.assertEqual(json.loads(session['current_question'])['netacan1'], "b")
        self.assertEqual(session['half_half_used'], False)
        self.assertEqual(session['replacement_question_used'], False)
        
        
        
    