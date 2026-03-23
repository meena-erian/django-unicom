import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smokeproject.settings")

import django

django.setup()

from unicom.models import Channel


channel, _ = Channel.objects.get_or_create(
    name="Smoke WebChat",
    platform="WebChat",
    defaults={"config": {}},
)

channel.config = channel.config or {}
channel.validate()

print(f"Seeded channel {channel.id} active={channel.active}")
