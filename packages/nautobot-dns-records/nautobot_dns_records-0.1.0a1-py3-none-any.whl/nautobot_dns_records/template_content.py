from django.urls import reverse
from nautobot.extras.plugins import PluginTemplateExtension


class DeviceExtraTabs(PluginTemplateExtension):

    model = "dcim.device"

    def detail_tabs(self):
        return [
            {
                "title": "DNS Records",
                "url": reverse("plugins:nautobot_dns_records:device_records", kwargs={"pk": self.context["object"].pk}),
            },
        ]


template_extensions = [
    DeviceExtraTabs,
]
