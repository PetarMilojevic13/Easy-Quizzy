#Ilija Miletic 2021/0335

import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from EasyQuizzy.models import *


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.registrovani = Korisnik.objects.create(korisnicko_ime='registrovani123', lozinka='Psii123+',
                                                ime="registrovani", prezime="registrovani",
                                                email="registrovani@gmail.com", pol="M", broj_poena="0", nivo="0",
                                                vazeci="1")
        self.moderator = Korisnik.objects.create(korisnicko_ime='moderator123', lozinka='Psii123+',
                                                ime="moderator", prezime="moderator",
                                                email="moderator@gmail.com", pol="M", broj_poena="0", nivo="0",
                                                vazeci="1")
        self.administrator = Korisnik.objects.create(korisnicko_ime='administrator123', lozinka='Psii123+',
                                                 ime="administrator", prezime="administrator",
                                                 email="admin@gmail.com", pol="M", broj_poena="0", nivo="0",
                                                 vazeci="1")

        RegistrovaniKorisnik.objects.create(idkor=self.registrovani)
        Moderator.objects.create(idkor=self.moderator)
        Administrator.objects.create(idkor=self.administrator)

        self.client = Client()
        self.login_url = reverse('login')

    def test_registered_user_login(self):
        response = self.client.post(self.login_url, {
            'username': 'registrovani123',
            'password': 'Psii123+'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['role'], 'registrovani')

    def test_moderator_user_login(self):
        response = self.client.post(self.login_url, {
            'username': 'moderator123',
            'password': 'Psii123+'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['role'], 'moderator')

    def test_admin_user_login(self):
        response = self.client.post(self.login_url, {
            'username': 'administrator123',
            'password': 'Psii123+'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['role'], 'admin')

    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'username': 'pogresno123',
            'password': 'pogresnalozinka123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Uneli ste pogrešno ime ili lozinku.')



class StatisticsViewTestCase(TestCase):
    def setUp(self):
        self.igrac1 = Korisnik.objects.create(korisnicko_ime='igrac123', lozinka='Psii123+',
                                             ime="igrac", prezime="igrac",
                                             email="igrac@gmail.com", pol="M", broj_poena="22", nivo="3",
                                             vazeci="1")
        self.igrac2 = Korisnik.objects.create(korisnicko_ime='igrac223', lozinka='Psii123+',
                                              ime="igrac", prezime="igrac",
                                              email="igrac@gmail.com", pol="M", broj_poena="35", nivo="4",
                                              vazeci="1")

        RegistrovaniKorisnik.objects.create(idkor=self.igrac1)
        RegistrovaniKorisnik.objects.create(idkor=self.igrac2)

        self.client = Client()
        self.login_url = reverse('login')

    def test_statistics_view(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        response = self.client.get(reverse('statistics'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('all_users', response.context)
        self.assertIn('korIme', response.context)
        self.assertIn('rank', response.context)
        self.assertIn('nivo', response.context)
        self.assertIn('broj_poena', response.context)

        all_users = response.context['all_users']
        self.assertEqual(len(all_users), 2)
        self.assertEqual(all_users[0][1], 'igrac223')
        self.assertEqual(all_users[1][1], 'igrac123')

        self.assertEqual(response.context['korIme'], 'igrac123')
        self.assertEqual(response.context['nivo'], 3)
        self.assertEqual(response.context['broj_poena'], 22)
        self.assertEqual(response.context['rank'], 2)



class QuestionSuggestionViewTestCase(TestCase):
    def setUp(self):
        self.igrac = Korisnik.objects.create(korisnicko_ime='igrac123', lozinka='Psii123+',
                                              ime="igrac", prezime="igrac",
                                              email="igrac@gmail.com", pol="M", broj_poena="22", nivo="3",
                                              vazeci="1")

        RegistrovaniKorisnik.objects.create(idkor=self.igrac)

        with open('EasyQuizzy/static/css/logo.jpeg', 'rb') as img:
            img_bytes = img.read()
            self.category = Kategorija.objects.create(naziv='Nova', slika=img_bytes)

        self.client = Client()
        self.login_url = reverse('login')

    def test_question_suggestion_get(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        response = self.client.get(reverse('questionSuggestion'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('korIme', response.context)
        self.assertEqual(response.context['korIme'], 'igrac123')

    def test_question_suggestion_post_new_question(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        response = self.client.post(reverse('questionSuggestion'), {'text': 'Novo pitanje'})
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Pitanje.objects.filter(tekst_pitanja='Novo pitanje').exists())

    def test_question_suggestion_post_existing_question(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        Pitanje.objects.create(idkat=self.category, tekst_pitanja='Staro pitanje', tezina_pitanja=1,
                               tacan_odgovor='Tacan', netacan1='netacan', netacan2='netacan', netacan3='netacan',
                               zbir_ocena='0', broj_ocena='0', prosecna_ocena='0', status='0')

        response = self.client.post(reverse('questionSuggestion'), {'text': 'Staro pitanje'})
        self.assertEqual(response.status_code, 302)



class AddingAndChangingQuestionsViewTestCase(TestCase):
    def setUp(self):
        self.igrac = Korisnik.objects.create(korisnicko_ime='igrac123', lozinka='Psii123+',
                                              ime="igrac", prezime="igrac",
                                              email="igrac@gmail.com", pol="M", broj_poena="22", nivo="3",
                                              vazeci="1")

        Moderator.objects.create(idkor=self.igrac)

        with open('EasyQuizzy/static/css/logo.jpeg', 'rb') as img:
            img_bytes = img.read()
        self.category = Kategorija.objects.create(naziv='Nova', slika=img_bytes)

        self.client = Client()
        self.login_url = reverse('login')

    def test_adding_questions_get(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        response = self.client.get(reverse('adding_questions'))
        self.assertEqual(response.status_code, 200)

        self.assertIn('categories', response.context)
        self.assertIn('permitted', response.context)
        self.assertIn('message', response.context)
        self.assertIn('messageChange', response.context)
        self.assertIn('messagePermitted', response.context)
        self.assertIn('left', response.context)
        self.assertIn('right', response.context)
        self.assertIn('category_names', response.context)

    def test_add_new_question(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        post_data = {
            'category': 'Nova',
            'question': 'Tekst pitanja',
            'weight': '1',
            'correct': 'Tacno',
            'incorrect1': 'Netacno',
            'incorrect2': 'Netacno',
            'incorrect3': 'Netacno',
            'temp': 'temp'
        }

        response = self.client.post(reverse('add_new_question'), post_data)
        self.assertEqual(response.status_code, 200)

        self.assertTrue(Pitanje.objects.filter(tekst_pitanja='Tekst pitanja').exists())
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], 'Pitanje je uspešno ubačeno u bazu!')

    def test_change_question(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        self.pitanje = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja='Staro pitanje', tezina_pitanja=1,
                               tacan_odgovor='Tacan', netacan1='netacan', netacan2='netacan', netacan3='netacan',
                               zbir_ocena='0', broj_ocena='0', prosecna_ocena='0', status='0')

        post_data = {
            'id': str(self.pitanje.idpit),
            'question': 'Novo pitanje',
            'weight': '2',
            'correct': 'Novo tacno',
            'incorrect1': 'Novo netacno',
            'incorrect2': 'Novo netacno',
            'incorrect3': 'Novo netacno',
            'temp': 'temp'
        }

        response = self.client.post(reverse('change_question'), post_data)
        self.assertEqual(response.status_code, 200)

        novo_pitanje = Pitanje.objects.get(idpit=self.pitanje.idpit)
        self.assertEqual(novo_pitanje.tekst_pitanja, 'Novo pitanje')
        self.assertEqual(novo_pitanje.tezina_pitanja, 2)
        self.assertEqual(novo_pitanje.tacan_odgovor, 'Novo tacno')
        self.assertEqual(novo_pitanje.netacan1, 'Novo netacno')
        self.assertEqual(novo_pitanje.netacan2, 'Novo netacno')
        self.assertEqual(novo_pitanje.netacan3, 'Novo netacno')

        self.assertIn('messageChange', response.context)
        self.assertEqual(response.context['messageChange'], 'Uspešno ste izvršili izmenu pitanja!')

    def test_change_question_to_existing(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        self.pitanje = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja='Staro pitanje', tezina_pitanja=1,
                               tacan_odgovor='Tacan', netacan1='netacan', netacan2='netacan', netacan3='netacan',
                               zbir_ocena='0', broj_ocena='0', prosecna_ocena='0', status='0')

        self.drugo_pitanje = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja='Drugo pitanje',
                                              tezina_pitanja=1,
                                              tacan_odgovor='Tacan', netacan1='netacan', netacan2='netacan',
                                              netacan3='netacan',
                                              zbir_ocena='0', broj_ocena='0', prosecna_ocena='0', status='0')

        post_data = {
            'id': str(self.pitanje.idpit),
            'question': 'Drugo pitanje',
            'weight': '2',
            'correct': 'Novo tacno',
            'incorrect1': 'Novo netacno',
            'incorrect2': 'Novo netacno',
            'incorrect3': 'Novo netacno',
            'temp': 'temp'
        }

        response = self.client.post(reverse('change_question'), post_data)
        self.assertEqual(response.status_code, 200)

        self.assertIn('messageChange', response.context)
        self.assertEqual(response.context['messageChange'], 'Pitanje sa datim tekstom već postoji!')

    def test_add_permitted_question(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        self.pitanje = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja='Odobreno pitanje',
                                              tezina_pitanja=1,
                                              tacan_odgovor='Tacan', netacan1='netacan', netacan2='netacan',
                                              netacan3='netacan',
                                              zbir_ocena='0', broj_ocena='0', prosecna_ocena='0', status='1')

        post_data = {
            'id': str(self.pitanje.idpit),
            'category': self.category.naziv,
            'question': self.pitanje.tekst_pitanja,
            'weight': '2',
            'correct': 'Nov tacan',
            'incorrect1': 'Nov netacan',
            'incorrect2': 'Nov netacan',
            'incorrect3': 'Nov netacan',
        }

        response = self.client.post(reverse('add_permitted_question'), post_data)
        self.assertEqual(response.status_code, 200)

        updated_question = Pitanje.objects.get(idpit=self.pitanje.idpit)
        self.assertEqual(updated_question.idkat, self.category)
        self.assertEqual(updated_question.tekst_pitanja, self.pitanje.tekst_pitanja)
        self.assertEqual(updated_question.tezina_pitanja, 2)
        self.assertEqual(updated_question.tacan_odgovor, 'Nov tacan')
        self.assertEqual(updated_question.netacan1, 'Nov netacan')
        self.assertEqual(updated_question.netacan2, 'Nov netacan')
        self.assertEqual(updated_question.netacan3, 'Nov netacan')
        self.assertEqual(updated_question.status, 0)

        self.assertIn('messagePermitted', response.context)
        self.assertEqual(response.context['messagePermitted'],
                         'Uspešno ste izvršili dodavanje pitanja iz skupa odobrenih!')



class AddingAndChangingCategoriesViewTestCase(TestCase):
    def setUp(self):
        self.igrac = Korisnik.objects.create(korisnicko_ime='igrac123', lozinka='Psii123+',
                                             ime="igrac", prezime="igrac",
                                             email="igrac@gmail.com", pol="M", broj_poena="22", nivo="3",
                                             vazeci="1")

        Moderator.objects.create(idkor=self.igrac)

        with open('EasyQuizzy/static/css/logo.jpeg', 'rb') as img:
            img_bytes = img.read()
        self.category1 = Kategorija.objects.create(naziv='Kategorija 1', slika=img_bytes)

        with open('EasyQuizzy/static/css/art.jpg', 'rb') as img:
            img_bytes = img.read()
        self.category2 = Kategorija.objects.create(naziv='Kategorija 2', slika=img_bytes)

        self.client = Client()
        self.login_url = reverse('login')

    def test_changing_categories_page(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        response = self.client.get(reverse('changing_categories_page'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'EasyQuizzy/adding_categories.html')

        self.assertIn('images', response.context)
        self.assertIn('messageChange', response.context)
        self.assertIn('left', response.context)
        self.assertIn('right', response.context)
        self.assertIn('messageQu', response.context)
        self.assertIn('messageCat', response.context)

        self.assertEqual(response.context['messageChange'], '')
        self.assertEqual(response.context['messageQu'], '')
        self.assertEqual(response.context['messageCat'], '')

    def test_change_category(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        post_data = {
            'firstName': 'Kategorija 1',
            'category': 'Novo ime'
        }

        response = self.client.post(reverse('change_existing_category'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Promena je uspešno napravljena')

        self.assertTrue(Kategorija.objects.filter(naziv='Novo ime').exists())
        self.assertFalse(Kategorija.objects.filter(naziv='Kategorija 1').exists())

    def test_add_new_category(self):
        self.client.post(self.login_url, {
            'username': 'igrac123',
            'password': 'Psii123+'
        })

        self.questions = {
            "pitanja": [
                ["Pitanje 1", "1", "Tacan", "Netacan", "Netacan", "Netacan"],
                ["Pitanje 2", "1", "Tacan", "Netacan", "Netacan", "Netacan"],
                ["Pitanje 3", "1", "Tacan", "Netacan", "Netacan", "Netacan"],
                ["Pitanje 4", "1", "Tacan", "Netacan", "Netacan", "Netacan"],
                ["Pitanje 5", "1", "Tacan", "Netacan", "Netacan", "Netacan"],
            ]
        }

        self.client.cookies['pitanja'] = json.dumps(self.questions)
        image_data = SimpleUploadedFile("newCatFile.png", b"dummy image content", content_type="image/png")

        post_data = {
            'newCatFile': image_data,
            'newCatName': 'Novo ime',
        }

        response = self.client.post(reverse('add_new_category'), post_data, format='multipart')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Kategorija je uspešno dodata')

        new_category = Kategorija.objects.filter(naziv='Novo ime').first()
        self.assertIsNotNone(new_category)
        self.assertEqual(new_category.naziv, 'Novo ime')

        for question in self.questions['pitanja']:
            self.assertTrue(Pitanje.objects.filter(tekst_pitanja=question[0], idkat=new_category).exists())
