from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from AccountApp.models import Doctor, Patient, Specialty
from AppointmentApp.models import Appointment


class ModelsTest(TestCase):

    def setUp(self):
        self.specialty = Specialty.objects.create(name="Cardiologie")
        self.doctor = Doctor.objects.create_user(
            username="dr1", password="Test1234",
            first_name="Ali", last_name="Ben",
            license_number="123456", phone="12345678",
        )
        self.doctor.specialties.add(self.specialty)
        self.patient = Patient.objects.create_user(
            username="pat1", password="Test1234!",
            first_name="Sana", last_name="Trabelsi",
            national_id="12345678", phone="87654321",
            birth_date=date(2000, 1, 1),
        )

    def make_appointment(self, when):
        return Appointment(
            doctor=self.doctor, patient=self.patient,
            reason="Controle", appointment_date=when,
        )

    def test_cle_primaire_heritee(self):
        self.assertEqual(self.doctor.pk, self.doctor.user_ptr_id)

    def test_phone_invalide(self):
        self.doctor.phone = "12"
        with self.assertRaises(ValidationError):
            self.doctor.full_clean()

    def test_naissance_dans_le_futur_refusee(self):
        self.patient.birth_date = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.patient.full_clean()

    def test_rdv_futur_valide_et_valeurs_par_defaut(self):
        a = self.make_appointment(timezone.now() + timedelta(days=1))
        a.full_clean()
        a.save()
        self.assertEqual(a.status, "PENDING")
        self.assertEqual(a.duration_minutes, 30)

    def test_rdv_passe_refuse_a_la_creation(self):
        a = self.make_appointment(timezone.now() - timedelta(days=1))
        with self.assertRaises(ValidationError):
            a.full_clean()

    def test_meme_medecin_meme_date_refuse(self):
        when = timezone.now() + timedelta(days=2)
        self.make_appointment(when).save()
        with self.assertRaises(ValidationError):
            self.make_appointment(when).full_clean()

    def test_rdv_passe_reste_modifiable(self):
        a = self.make_appointment(timezone.now() - timedelta(days=3))
        a.save()
        a = Appointment.objects.get(pk=a.pk)
        a.status = Appointment.Status.CONFIRMED
        a.full_clean()