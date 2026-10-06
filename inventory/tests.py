"""Regression checks for the original EcoFlux views."""
import io
import tempfile
from pathlib import Path

from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, SimpleTestCase, RequestFactory, override_settings
from django.urls import reverse, reverse_lazy

from .models import Document, Equipment, FieldNote, Photo, Site
from navigation import get_return_url


class NavigationFallbackTests(SimpleTestCase):
    def test_empty_history_accepts_a_route_name_or_resolved_url(self):
        request = RequestFactory().get("/sites/edit/1/")
        request.session = {}
        expected = reverse("view_sites")
        for fallback in ("view_sites", expected, reverse_lazy("view_sites")):
            with self.subTest(fallback=str(fallback)):
                self.assertEqual(get_return_url(request, fallback), expected)


class SiteEditPreservationTests(TestCase):
    def test_edit_preserves_fieldnotes_photos_documents_and_file_bytes(self):
        with tempfile.TemporaryDirectory() as temp, override_settings(MEDIA_ROOT=temp):
            site = Site.objects.create(
                name="Original site", code="UQAM_3", amp="CA-CQ3",
                location="Quebec", description="Original description",
                date_activated="2025-04-10",
            )
            note = FieldNote.objects.create(site=site, note="Original field note")
            equipment = Equipment.objects.create(
                instrument="Analyzer", serial_number="test-serial",
                date_purchased="2025-01-01", site=site,
            )
            image = io.BytesIO()
            Image.new("RGB", (2, 2), "green").save(image, "JPEG")
            photo = Photo.objects.create(
                fieldnote=note,
                photo=SimpleUploadedFile("photo.jpg", image.getvalue(), "image/jpeg"),
            )
            documents = []
            for parent in (site, note):
                documents.append(Document.objects.create(
                    content_type=ContentType.objects.get_for_model(parent),
                    object_id=parent.pk, date_received="2026-01-01",
                    summary="Protocol",
                    file=SimpleUploadedFile("protocol.pdf", b"%PDF-test-fixture"),
                    thumbnail=SimpleUploadedFile("preview.jpg", image.getvalue()),
                ))
            saved_files = [photo.photo, photo.thumbnail]
            for document in documents:
                saved_files.extend([document.file, document.thumbnail])
            before = {field.name: Path(field.path).read_bytes() for field in saved_files}

            user = get_user_model().objects.create_user(username="site-editor")
            self.client.force_login(user)
            response = self.client.post(reverse("site_edit", args=[site.pk]), {
                "name": "Corrected site", "code": site.code, "amp": site.amp,
                "location": site.location, "description": site.description,
                "date_activated": "2025-04-10", "date_retired": "",
                "gps_coordinates": "",
            })

            self.assertEqual(response.status_code, 302)
            site.refresh_from_db()
            self.assertEqual(site.name, "Corrected site")
            self.assertTrue(FieldNote.objects.filter(pk=note.pk, site=site).exists())
            self.assertTrue(Photo.objects.filter(pk=photo.pk, fieldnote=note).exists())
            self.assertEqual(Document.objects.filter(pk__in=[d.pk for d in documents]).count(), 2)
            self.assertTrue(Equipment.objects.filter(pk=equipment.pk, site=site).exists())
            for field in saved_files:
                self.assertTrue(field.storage.exists(field.name), field.name)
                self.assertEqual(Path(field.path).read_bytes(), before[field.name])
