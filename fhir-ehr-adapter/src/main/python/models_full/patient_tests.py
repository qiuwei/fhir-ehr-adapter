#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Generated from FHIR 1.8.0.10521 on 2018-01-16.
#  2018, SMART Health IT.


import os
import io
import unittest
import json
from . import patient
from .fhirdate import FHIRDate


class PatientTests(unittest.TestCase):
    def instantiate_from(self, filename):
        datadir = os.environ.get('FHIR_UNITTEST_DATADIR') or ''
        with io.open(os.path.join(datadir, filename), 'r', encoding='utf-8') as handle:
            js = json.load(handle)
            self.assertEqual("Patient", js["resourceType"])
        return patient.Patient(js)
    
    def testPatient1(self):
        inst = self.instantiate_from("patient-example-xds.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient1(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient1(inst2)
    
    def implPatient1(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.address[0].city, "Metropolis")
        self.assertEqual(inst.address[0].country, "USA")
        self.assertEqual(inst.address[0].line[0], "100 Main St")
        self.assertEqual(inst.address[0].postalCode, "44130")
        self.assertEqual(inst.address[0].state, "Il")
        self.assertEqual(inst.birthDate.date, FHIRDate("1956-05-27").date)
        self.assertEqual(inst.birthDate.as_json(), "1956-05-27")
        self.assertEqual(inst.gender, "male")
        self.assertEqual(inst.id, "xds")
        self.assertEqual(inst.identifier[0].system, "urn:oid:1.2.3.4.5")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "MR")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://hl7.org/fhir/v2/0203")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "89765a87b")
        self.assertEqual(inst.name[0].family, "Doe")
        self.assertEqual(inst.name[0].given[0], "John")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Patient John Doe, M, 27-May 1956. ID: 89765a87b</p></div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient2(self):
        inst = self.instantiate_from("patient-example-f001-pieter.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient2(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient2(inst2)
    
    def implPatient2(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.address[0].city, "Amsterdam")
        self.assertEqual(inst.address[0].country, "NLD")
        self.assertEqual(inst.address[0].line[0], "Van Egmondkade 23")
        self.assertEqual(inst.address[0].postalCode, "1024 RJ")
        self.assertEqual(inst.address[0].use, "home")
        self.assertEqual(inst.birthDate.date, FHIRDate("1944-11-17").date)
        self.assertEqual(inst.birthDate.as_json(), "1944-11-17")
        self.assertEqual(inst.communication[0].language.coding[0].code, "nl")
        self.assertEqual(inst.communication[0].language.coding[0].display, "Dutch")
        self.assertEqual(inst.communication[0].language.coding[0].system, "urn:ietf:bcp:47")
        self.assertEqual(inst.communication[0].language.text, "Nederlands")
        self.assertTrue(inst.communication[0].preferred)
        self.assertEqual(inst.contact[0].name.family, "Abels")
        self.assertEqual(inst.contact[0].name.given[0], "Sarah")
        self.assertEqual(inst.contact[0].name.use, "usual")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].code, "partner")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].system, "http://hl7.org/fhir/patient-contact-relationship")
        self.assertEqual(inst.contact[0].telecom[0].system, "phone")
        self.assertEqual(inst.contact[0].telecom[0].use, "mobile")
        self.assertEqual(inst.contact[0].telecom[0].value, "0690383372")
        self.assertFalse(inst.deceasedBoolean)
        self.assertEqual(inst.gender, "male")
        self.assertEqual(inst.id, "f001")
        self.assertEqual(inst.identifier[0].system, "urn:oid:2.16.840.1.113883.2.4.6.3")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "738472983")
        self.assertEqual(inst.identifier[1].system, "urn:oid:2.16.840.1.113883.2.4.6.3")
        self.assertEqual(inst.identifier[1].use, "usual")
        self.assertEqual(inst.maritalStatus.coding[0].code, "M")
        self.assertEqual(inst.maritalStatus.coding[0].display, "Married")
        self.assertEqual(inst.maritalStatus.coding[0].system, "http://hl7.org/fhir/v3/MaritalStatus")
        self.assertEqual(inst.maritalStatus.text, "Getrouwd")
        self.assertTrue(inst.multipleBirthBoolean)
        self.assertEqual(inst.name[0].family, "van de Heuvel")
        self.assertEqual(inst.name[0].given[0], "Pieter")
        self.assertEqual(inst.name[0].suffix[0], "MSc")
        self.assertEqual(inst.name[0].use, "usual")
        self.assertEqual(inst.telecom[0].system, "phone")
        self.assertEqual(inst.telecom[0].use, "mobile")
        self.assertEqual(inst.telecom[0].value, "0648352638")
        self.assertEqual(inst.telecom[1].system, "email")
        self.assertEqual(inst.telecom[1].use, "home")
        self.assertEqual(inst.telecom[1].value, "p.heuvel@gmail.com")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient3(self):
        inst = self.instantiate_from("patient-example-d.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient3(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient3(inst2)
    
    def implPatient3(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.birthDate.date, FHIRDate("1982-08-02").date)
        self.assertEqual(inst.birthDate.as_json(), "1982-08-02")
        self.assertTrue(inst.deceasedBoolean)
        self.assertEqual(inst.gender, "female")
        self.assertEqual(inst.id, "pat4")
        self.assertEqual(inst.identifier[0].system, "urn:oid:0.1.2.3.4.5.6.7")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "MR")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://hl7.org/fhir/v2/0203")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "123458")
        self.assertEqual(inst.name[0].family, "Notsowell")
        self.assertEqual(inst.name[0].given[0], "Sandy")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Patient Sandy Notsowell @ Acme Healthcare, Inc. MR = 123458, DECEASED</p></div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient4(self):
        inst = self.instantiate_from("patient-genetics-example1.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient4(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient4(inst2)
    
    def implPatient4(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.address[0].line[0], "2222 Home Street")
        self.assertEqual(inst.address[0].use, "home")
        self.assertEqual(inst.birthDate.date, FHIRDate("1973-05-31").date)
        self.assertEqual(inst.birthDate.as_json(), "1973-05-31")
        self.assertEqual(inst.gender, "female")
        self.assertEqual(inst.id, "genetics-example1")
        self.assertEqual(inst.identifier[0].system, "http://hl7.org/fhir/sid/us-ssn")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "SS")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://hl7.org/fhir/v2/0203")
        self.assertEqual(inst.identifier[0].value, "444222222")
        self.assertEqual(inst.meta.lastUpdated.date, FHIRDate("2012-05-29T23:45:32Z").date)
        self.assertEqual(inst.meta.lastUpdated.as_json(), "2012-05-29T23:45:32Z")
        self.assertEqual(inst.name[0].family, "Everywoman")
        self.assertEqual(inst.name[0].given[0], "Eve")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.telecom[0].system, "phone")
        self.assertEqual(inst.telecom[0].use, "work")
        self.assertEqual(inst.telecom[0].value, "555-555-2003")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Everywoman, Eve. SSN:444222222</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient5(self):
        inst = self.instantiate_from("patient-example-b.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient5(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient5(inst2)
    
    def implPatient5(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.gender, "other")
        self.assertEqual(inst.id, "pat2")
        self.assertEqual(inst.identifier[0].system, "urn:oid:0.1.2.3.4.5.6.7")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "MR")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://hl7.org/fhir/v2/0203")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "123456")
        self.assertEqual(inst.link[0].type, "seealso")
        self.assertEqual(inst.name[0].family, "Donald")
        self.assertEqual(inst.name[0].given[0], "Duck")
        self.assertEqual(inst.name[0].given[1], "D")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.photo[0].contentType, "image/gif")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Patient Donald D DUCK @ Acme Healthcare, Inc. MR = 123456</p></div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient6(self):
        inst = self.instantiate_from("patient-example-c.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient6(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient6(inst2)
    
    def implPatient6(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.birthDate.date, FHIRDate("1982-01-23").date)
        self.assertEqual(inst.birthDate.as_json(), "1982-01-23")
        self.assertEqual(inst.deceasedDateTime.date, FHIRDate("2015-02-14T13:42:00+10:00").date)
        self.assertEqual(inst.deceasedDateTime.as_json(), "2015-02-14T13:42:00+10:00")
        self.assertEqual(inst.gender, "male")
        self.assertEqual(inst.id, "pat3")
        self.assertEqual(inst.identifier[0].system, "urn:oid:0.1.2.3.4.5.6.7")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "MR")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://hl7.org/fhir/v2/0203")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "123457")
        self.assertEqual(inst.name[0].family, "Notsowell")
        self.assertEqual(inst.name[0].given[0], "Simon")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p>Patient Simon Notsowell @ Acme Healthcare, Inc. MR = 123457, DECEASED</p></div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient7(self):
        inst = self.instantiate_from("patient-example-ihe-pcd.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient7(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient7(inst2)
    
    def implPatient7(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.id, "ihe-pcd")
        self.assertEqual(inst.identifier[0].type.text, "Internal Identifier")
        self.assertEqual(inst.identifier[0].value, "AB60001")
        self.assertEqual(inst.name[0].family, "BROOKS")
        self.assertEqual(inst.name[0].given[0], "ALBERT")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\">Albert Brooks, Id: AB60001</div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient8(self):
        inst = self.instantiate_from("patient-example.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient8(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient8(inst2)
    
    def implPatient8(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.address[0].city, "PleasantVille")
        self.assertEqual(inst.address[0].district, "Rainbow")
        self.assertEqual(inst.address[0].line[0], "534 Erewhon St")
        self.assertEqual(inst.address[0].period.start.date, FHIRDate("1974-12-25").date)
        self.assertEqual(inst.address[0].period.start.as_json(), "1974-12-25")
        self.assertEqual(inst.address[0].postalCode, "3999")
        self.assertEqual(inst.address[0].state, "Vic")
        self.assertEqual(inst.address[0].type, "both")
        self.assertEqual(inst.address[0].use, "home")
        self.assertEqual(inst.birthDate.date, FHIRDate("1974-12-25").date)
        self.assertEqual(inst.birthDate.as_json(), "1974-12-25")
        self.assertEqual(inst.contact[0].address.city, "PleasantVille")
        self.assertEqual(inst.contact[0].address.district, "Rainbow")
        self.assertEqual(inst.contact[0].address.line[0], "534 Erewhon St")
        self.assertEqual(inst.contact[0].address.period.start.date, FHIRDate("1974-12-25").date)
        self.assertEqual(inst.contact[0].address.period.start.as_json(), "1974-12-25")
        self.assertEqual(inst.contact[0].address.postalCode, "3999")
        self.assertEqual(inst.contact[0].address.state, "Vic")
        self.assertEqual(inst.contact[0].address.type, "both")
        self.assertEqual(inst.contact[0].address.use, "home")
        self.assertEqual(inst.contact[0].gender, "female")
        self.assertEqual(inst.contact[0].period.start.date, FHIRDate("2012").date)
        self.assertEqual(inst.contact[0].period.start.as_json(), "2012")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].code, "partner")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].system, "http://hl7.org/fhir/patient-contact-relationship")
        self.assertEqual(inst.contact[0].telecom[0].system, "phone")
        self.assertEqual(inst.contact[0].telecom[0].value, "+33 (237) 998327")
        self.assertFalse(inst.deceasedBoolean)
        self.assertEqual(inst.gender, "male")
        self.assertEqual(inst.id, "example")
        self.assertEqual(inst.identifier[0].period.start.date, FHIRDate("2001-05-06").date)
        self.assertEqual(inst.identifier[0].period.start.as_json(), "2001-05-06")
        self.assertEqual(inst.identifier[0].system, "urn:oid:1.2.36.146.595.217.0.1")
        self.assertEqual(inst.identifier[0].type.coding[0].code, "MR")
        self.assertEqual(inst.identifier[0].type.coding[0].system, "http://hl7.org/fhir/v2/0203")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "12345")
        self.assertEqual(inst.name[0].family, "Chalmers")
        self.assertEqual(inst.name[0].given[0], "Peter")
        self.assertEqual(inst.name[0].given[1], "James")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.name[1].given[0], "Jim")
        self.assertEqual(inst.name[1].use, "usual")
        self.assertEqual(inst.telecom[0].use, "home")
        self.assertEqual(inst.telecom[1].system, "phone")
        self.assertEqual(inst.telecom[1].use, "work")
        self.assertEqual(inst.telecom[1].value, "(03) 5555 6473")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient9(self):
        inst = self.instantiate_from("patient-example-proband.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient9(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient9(inst2)
    
    def implPatient9(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.birthDate.date, FHIRDate("1966-04-04").date)
        self.assertEqual(inst.birthDate.as_json(), "1966-04-04")
        self.assertFalse(inst.deceasedBoolean)
        self.assertEqual(inst.extension[0].extension[0].url, "ombCategory")
        self.assertEqual(inst.extension[0].extension[0].valueCoding.code, "2106-3")
        self.assertEqual(inst.extension[0].extension[0].valueCoding.display, "White")
        self.assertEqual(inst.extension[0].extension[0].valueCoding.system, "http://hl7.org/fhir/v3/Race")
        self.assertEqual(inst.extension[0].url, "http://hl7.org/fhir/StructureDefinition/us-core-race")
        self.assertEqual(inst.gender, "female")
        self.assertEqual(inst.id, "proband")
        self.assertEqual(inst.identifier[0].system, "urn:oid:2.16.840.1.113883.6.117")
        self.assertEqual(inst.identifier[0].type.text, "Computer-Stored Abulatory Records (COSTAR)")
        self.assertEqual(inst.identifier[0].use, "usual")
        self.assertEqual(inst.identifier[0].value, "999999999")
        self.assertEqual(inst.text.div, "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Annie Proband</b>: Female, born 1966-04-04</p></div>")
        self.assertEqual(inst.text.status, "generated")
    
    def testPatient10(self):
        inst = self.instantiate_from("patient-example-f201-roel.json")
        self.assertIsNotNone(inst, "Must have instantiated a Patient instance")
        self.implPatient10(inst)
        
        js = inst.as_json()
        self.assertEqual("Patient", js["resourceType"])
        inst2 = patient.Patient(js)
        self.implPatient10(inst2)
    
    def implPatient10(self, inst):
        self.assertTrue(inst.active)
        self.assertEqual(inst.address[0].city, "Amsterdam")
        self.assertEqual(inst.address[0].country, "NLD")
        self.assertEqual(inst.address[0].line[0], "Bos en Lommerplein 280")
        self.assertEqual(inst.address[0].postalCode, "1055RW")
        self.assertEqual(inst.address[0].use, "home")
        self.assertEqual(inst.birthDate.date, FHIRDate("1960-03-13").date)
        self.assertEqual(inst.birthDate.as_json(), "1960-03-13")
        self.assertEqual(inst.communication[0].language.coding[0].code, "nl-NL")
        self.assertEqual(inst.communication[0].language.coding[0].display, "Dutch")
        self.assertEqual(inst.communication[0].language.coding[0].system, "urn:ietf:bcp:47")
        self.assertTrue(inst.communication[0].preferred)
        self.assertEqual(inst.contact[0].name.text, "Ariadne Bor-Jansma")
        self.assertEqual(inst.contact[0].name.use, "usual")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].code, "127850001")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].display, "Wife")
        self.assertEqual(inst.contact[0].relationship[0].coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.contact[0].relationship[0].coding[1].code, "partner")
        self.assertEqual(inst.contact[0].relationship[0].coding[1].system, "http://hl7.org/fhir/patient-contact-relationship")
        self.assertEqual(inst.contact[0].telecom[0].system, "phone")
        self.assertEqual(inst.contact[0].telecom[0].use, "home")
        self.assertEqual(inst.contact[0].telecom[0].value, "+31201234567")
        self.assertFalse(inst.deceasedBoolean)
        self.assertEqual(inst.gender, "male")
        self.assertEqual(inst.id, "f201")
        self.assertEqual(inst.identifier[0].system, "urn:oid:2.16.840.1.113883.2.4.6.3")
        self.assertEqual(inst.identifier[0].type.text, "BSN")
        self.assertEqual(inst.identifier[0].use, "official")
        self.assertEqual(inst.identifier[0].value, "123456789")
        self.assertEqual(inst.identifier[1].system, "urn:oid:2.16.840.1.113883.2.4.6.3")
        self.assertEqual(inst.identifier[1].type.text, "BSN")
        self.assertEqual(inst.identifier[1].use, "official")
        self.assertEqual(inst.identifier[1].value, "123456789")
        self.assertEqual(inst.maritalStatus.coding[0].code, "36629006")
        self.assertEqual(inst.maritalStatus.coding[0].display, "Legally married")
        self.assertEqual(inst.maritalStatus.coding[0].system, "http://snomed.info/sct")
        self.assertEqual(inst.maritalStatus.coding[1].code, "M")
        self.assertEqual(inst.maritalStatus.coding[1].system, "http://hl7.org/fhir/v3/MaritalStatus")
        self.assertFalse(inst.multipleBirthBoolean)
        self.assertEqual(inst.name[0].family, "Bor")
        self.assertEqual(inst.name[0].given[0], "Roelof Olaf")
        self.assertEqual(inst.name[0].prefix[0], "Drs.")
        self.assertEqual(inst.name[0].suffix[0], "PDEng.")
        self.assertEqual(inst.name[0].text, "Roel")
        self.assertEqual(inst.name[0].use, "official")
        self.assertEqual(inst.photo[0].contentType, "image/jpeg")
        self.assertEqual(inst.photo[0].url, "Binary/f006")
        self.assertEqual(inst.telecom[0].system, "phone")
        self.assertEqual(inst.telecom[0].use, "mobile")
        self.assertEqual(inst.telecom[0].value, "+31612345678")
        self.assertEqual(inst.telecom[1].system, "phone")
        self.assertEqual(inst.telecom[1].use, "home")
        self.assertEqual(inst.telecom[1].value, "+31201234567")
        self.assertEqual(inst.text.status, "generated")
