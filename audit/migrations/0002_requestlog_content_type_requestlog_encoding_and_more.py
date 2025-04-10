# Generated by Django 4.2.10 on 2025-03-27 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("audit", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="requestlog",
            name="content_type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="encoding",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="headers",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="host",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="is_ajax",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="is_secure",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="referer",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="request_body",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="response_time",
            field=models.FloatField(
                help_text="Response time in seconds", null=True
            ),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="session_key",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="status_code",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="requestlog",
            name="user_agent",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddIndex(
            model_name="requestlog",
            index=models.Index(
                fields=["-timestamp"], name="audit_reque_timesta_478c53_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="requestlog",
            index=models.Index(
                fields=["user"], name="audit_reque_user_id_52d4cd_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="requestlog",
            index=models.Index(
                fields=["method"], name="audit_reque_method_1ac6f2_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="requestlog",
            index=models.Index(
                fields=["status_code"], name="audit_reque_status__340c13_idx"
            ),
        ),
    ]
