# Petar Milojević 2021/0336
from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from EasyQuizzy.models import Kategorija, Korisnik, Pitanje, RegistrovaniKorisnik, Moderator
import base64
import math
from django.db import connection
from EasyQuizzy.viewsIlija import answer, answer_GET, fifty_fifty

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from EasyQuizzy.viewsIlija import question_of_the_day, question_of_the_day_GET
from django.contrib.auth.models import User

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')


    def test_registerSuccesful(self):
        response = self.client.post(self.url, {
            'username': 'test',
            'name': 'Test',
            'surname': 'User',
            'password': 'Psii123+',
            'passwordVal': 'Psii123+',
            'email': 'testuser@etf.rs',
            'gender': 'Muško',

        })
        self.assertRedirects(response, self.url)
        self.assertEqual(Korisnik.objects.count(), 1)
        self.assertEqual(RegistrovaniKorisnik.objects.count(), 1)
        user = Korisnik.objects.get(korisnicko_ime='test')
        self.assertEqual(user.ime, 'Test')
        self.assertEqual(user.prezime, 'User')

    def test_missing_surname(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'name': 'Test',
            'surname': '',
            'password': 'Psii123+',
            'passwordVal': 'Psii123+',
            'email': 'testuser@etf.rs',
            'gender': 'Muško',
        })
        self.assertContains(response, 'Prezime nije popunjeno!')
        self.assertEqual(Korisnik.objects.count(), 0)

    def test_passwords_do_not_match(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'name': 'Test',
            'surname': 'User',
            'password': 'Psii123+',
            'passwordVal': 'Psii321+',
            'email': 'testuser@etf.rs',
            'gender': 'Muško',
        })
        self.assertContains(response, 'Lozinke se ne poklapaju!')
        self.assertEqual(Korisnik.objects.count(), 0)





class ShowCategoriesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('show_categories')  # Pretpostavljam da je ime URL-a 'show_categories'

    @patch('EasyQuizzy.views_administrator.get_category_images')
    @patch('EasyQuizzy.views_administrator.get_stickers')
    def test_show_categories(self, mock_get_stickers, mock_get_category_images):
        # Simulacija povratnih vrednosti funkcija
        mock_get_category_images.return_value = [
            {'name': 'Category 1', 'image': 'image1.jpg'},
            {'name': 'Category 2', 'image': 'image2.jpg'}
        ]
        mock_get_stickers.return_value = ('left_sticker', 'right_sticker')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'EasyQuizzy/categories.html')

        # Provera konteksta
        context = response.context
        self.assertIn('images', context)
        self.assertIn('left', context)
        self.assertIn('right', context)

        # Provera vrednosti konteksta
        self.assertEqual(context['images'], [
            {'name': 'Category 1', 'image': 'image1.jpg'},
            {'name': 'Category 2', 'image': 'image2.jpg'}
        ])
        self.assertEqual(context['left'], 'left_sticker')
        self.assertEqual(context['right'], 'right_sticker')


class QuestionOfTheDayTestCase(TestCase):
    def setUp(self):
        # Kreiranje testnog korisnika
        self.user = User.objects.create_user(username='testuser', password='Psii123+')

        # Kreiranje Korisnik instance povezana sa User modelom
        self.korisnik = Korisnik.objects.create(
            korisnicko_ime='testuser',
            lozinka='Psii123+',
            email='test@etf.rs',
            broj_poena=0,
            nivo=1,
            vazeci=1
        )

        categories = ['Kategorija1', 'Kategorija2', 'Kategorija3']
        img_path = ['EasyQuizzy/static/css/collage3.jpg', 'EasyQuizzy/static/css/sport.jpg',
                    'EasyQuizzy/static/css/music.jpg']

        i = 0
        for cat in categories:
            with open(img_path[i], 'rb') as img:
                img_bytes = img.read()
            Kategorija.objects.create(naziv=cat, slika=img_bytes)

        self.question = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja="probica", tezina_pitanja=1,
                               tacan_odgovor="a", netacan1="b", netacan2="c", netacan3="d", zbir_ocena=0, broj_ocena=0,
                               prosecna_ocena=0, status=0)

        # Postavljanje URL-a za view metodu
        self.url = reverse('question_of_the_day')

        # Inicijalizacija klijenta
        self.client = Client()

    def test_question_of_the_day_authenticated_correct(self):
        # Prijavljivanje korisnika
        self.client.login(username='testuser', password='Psii123+')

        # Postavljanje sesije
        session = self.client.session
        session['IdKor_current'] = self.korisnik.idkor
        session.save()

        # Simulacija POST zahteva sa odgovorom na pitanje
        response = self.client.post(self.url, {
            'odgovor': 'a',
            'tekst_pitanja': 'probica'
        })

        # Provera da li su sesijske promenljive postavljene
        session = self.client.session
        self.assertEqual(session['correct_answer'], 1)
        self.assertEqual(session['level_passed'], 0)
        self.assertEqual(session['new_level'], 1)

        # Provera da li su poeni i nivo korisnika ispravno ažurirani
        self.korisnik.refresh_from_db()
        self.assertEqual(self.korisnik.broj_poena, 5)
        self.assertEqual(self.korisnik.nivo, 1)


    def test_question_of_the_day_authenticated_incorrect(self):
        # Prijavljivanje korisnika
        self.client.login(username='testuser', password='Psii123+')

        # Postavljanje sesije
        session = self.client.session
        session['IdKor_current'] = self.korisnik.idkor
        session.save()

        # Simulacija POST zahteva sa odgovorom na pitanje
        response = self.client.post(self.url, {
            'odgovor': 'b',
            'tekst_pitanja': 'probica'
        })

        # Provera da li su sesijske promenljive postavljene
        session = self.client.session
        self.assertEqual(session['correct_answer'], 0)
        self.assertEqual(session['level_passed'], 0)
        self.assertEqual(session['new_level'], 0)

        # Provera da li su poeni i nivo korisnika ispravno ažurirani
        self.korisnik.refresh_from_db()
        self.assertEqual(self.korisnik.broj_poena, 0)
        self.assertEqual(self.korisnik.nivo, 1)


class AddToPermittedTestCase(TestCase):
    def setUp(self):
        # Kreiranje testnog korisnika
        self.user = User.objects.create_user(username='admin', password='Psii123+')

        self.korisnik = Korisnik.objects.create(
            korisnicko_ime='test',
            lozinka='Psii123+',
            email='test@etf.rs',
            broj_poena=0,
            nivo=1,
            vazeci=1
        )

        categories = ['Kategorija1', 'Kategorija2', 'Kategorija3']
        img_path = ['EasyQuizzy/static/css/collage3.jpg', 'EasyQuizzy/static/css/sport.jpg',
                    'EasyQuizzy/static/css/music.jpg']

        i = 0
        for cat in categories:
            with open(img_path[i], 'rb') as img:
                img_bytes = img.read()
            Kategorija.objects.create(naziv=cat, slika=img_bytes)

        self.question1 = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja="probica", tezina_pitanja=1,
                               tacan_odgovor="a", netacan1="b", netacan2="c", netacan3="d", zbir_ocena=0, broj_ocena=0,
                               prosecna_ocena=0, status=2)

        self.question2 = Pitanje.objects.create(idkat=Kategorija.objects.first(), tekst_pitanja="probica2",
                                                tezina_pitanja=1,
                                                tacan_odgovor="a", netacan1="b", netacan2="c", netacan3="d",
                                                zbir_ocena=0, broj_ocena=0,
                                                prosecna_ocena=0, status=2)

        # Postavljanje URL-a za view metodu
        self.url = reverse('add_to_permitted')

        # Inicijalizacija klijenta
        self.client = Client()

    def test_add_to_permitted_authenticated(self):
        # Prijavljivanje korisnika
        self.client.login(username='admin', password='Psii123+')

        # Simulacija POST zahteva sa listom pitanja za odobrenje
        response = self.client.post(self.url, {
            'checkbox': [self.question1.tekst_pitanja, self.question2.tekst_pitanja],
            'permit': '1'
        })

        # Provera da li su pitanja pravilno ažurirana
        self.question1.refresh_from_db()
        self.question2.refresh_from_db()
        self.assertEqual(self.question1.status, 1)
        self.assertEqual(self.question2.status, 1)

        # Provera odgovora
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'EasyQuizzy/question_permission.html')

    def test_add_to_permitted_delete(self):
        # Prijavljivanje korisnika
        self.client.login(username='admin', password='Psii123+')

        # Simulacija POST zahteva sa listom pitanja za odobrenje
        response = self.client.post(self.url, {
            'checkbox': [self.question1.tekst_pitanja, self.question2.tekst_pitanja],
            'delete': '1'
        })

        # Provera da li su pitanja pravilno ažurirana
        with self.assertRaises(Pitanje.DoesNotExist):
            Pitanje.objects.get(tekst_pitanja="probica")
        with self.assertRaises(Pitanje.DoesNotExist):
            Pitanje.objects.get(tekst_pitanja="probica2")

        # Provera odgovora
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'EasyQuizzy/question_permission.html')


class DeleteUserTestCase(TestCase):
    def setUp(self):
        # Kreiranje testnog korisnika
        self.user = User.objects.create_user(username='proba', password='Psii123+')

        # Kreiranje Korisnik instance povezana sa User modelom
        self.korisnik = Korisnik.objects.create(
            korisnicko_ime='proba',
            lozinka='Psii123+',
            email='proba@etf.rs',
            broj_poena=0,
            nivo=1,
            vazeci=1,
        )

        # Postavljanje URL-a za view metodu
        self.url = reverse('delete_user')

        # Inicijalizacija klijenta
        self.client = Client()

    def test_delete_existing_user(self):
        # Simulacija AJAX POST zahteva za brisanje postojećeg korisnika
        response = self.client.post(self.url, data=f"username={self.korisnik.korisnicko_ime}",
                                    content_type="application/x-www-form-urlencoded")

        # Provera odgovora
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['successful'])
        self.assertEqual(response_data['message'], "Uspešno ste izvršili brisanje korisnika")

        # Provera da li je korisnik ispravno ažuriran
        self.korisnik.refresh_from_db()
        self.assertEqual(self.korisnik.vazeci, 0)

    def test_delete_non_existing_user(self):
        # Simulacija AJAX POST zahteva za brisanje nepostojećeg korisnika
        response = self.client.post(self.url, data="username=nepostojeci",
                                    content_type="application/x-www-form-urlencoded")

        # Provera odgovora
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertFalse(response_data['successful'])
        self.assertEqual(response_data['message'], "Ne postoji korisnik koga želite da obrišete")


class AddModeratorTestCase(TestCase):
    def setUp(self):
        # Kreiranje testnih korisnika
        self.user = User.objects.create_user(username='proba', password='Psii123+')
        self.user_moderator = User.objects.create_user(username='moderator', password='Psii123+')

        # Kreiranje Korisnik instanci povezanih sa User modelom
        self.korisnik = Korisnik.objects.create(
            korisnicko_ime='proba',
            lozinka='Psii123+',
            email='test@etf.rs',
            broj_poena=0,
            nivo=1,
            vazeci=1,
        )
        print(self.korisnik.idkor)
        self.korisnik_moderator = Korisnik.objects.create(
            korisnicko_ime='moderator',
            lozinka='Psii123+',
            email='moderator@etf.rs',
            broj_poena=0,
            nivo=1,
            vazeci=1,
        )
        print(self.korisnik_moderator.idkor)
        RegistrovaniKorisnik.objects.create(idkor=self.korisnik)
        Moderator.objects.create(idkor=self.korisnik_moderator)
        # Postavljanje URL-a za view metodu
        self.url = reverse('add_moderator')

        # Inicijalizacija klijenta
        self.client = Client()

    def test_add_moderator_existing_user(self):
        # Simulacija AJAX POST zahteva za dodavanje moderatora postojećem korisniku
        response = self.client.post(self.url, data="username=proba",
                                    content_type="application/x-www-form-urlencoded")

        # Provera da li je moderator pravilno dodat u bazu
        moderator_count = Moderator.objects.filter(idkor=self.korisnik).count()
        self.assertEqual(moderator_count, 0)

    def test_add_moderator_existing_moderator(self):
        # Simulacija AJAX POST zahteva za dodavanje moderatora korisniku koji već ima ulogu moderatora
        response = self.client.post(self.url, data="username=moderator",
                                    content_type="application/x-www-form-urlencoded")

        # Provera da li je baza ostala nepromenjena
        moderator_count = Moderator.objects.filter(idkor=self.korisnik_moderator).count()
        self.assertEqual(moderator_count, 1)

    def test_add_moderator_non_existing_user(self):
        # Simulacija AJAX POST zahteva za dodavanje moderatora nepostojećem korisniku
        response = self.client.post(self.url, data="username=nepostojeci",
                                    content_type="application/x-www-form-urlencoded")

        # Provera da li je baza ostala nepromenjena
        moderator_count = Moderator.objects.filter(idkor__korisnicko_ime="nonexistentuser").count()
        self.assertEqual(moderator_count, 0)





