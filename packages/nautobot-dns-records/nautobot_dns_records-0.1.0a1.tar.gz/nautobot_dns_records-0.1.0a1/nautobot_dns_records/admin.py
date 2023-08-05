from nautobot.core.admin import NautobotModelAdmin

from nautobot_dns_records.models import AddressRecord, TxtRecord, PtrRecord, LocRecord, SshfpRecord, CNameRecord
from django.contrib import admin


@admin.register(AddressRecord)
class AddressAdmin(NautobotModelAdmin):
    pass


@admin.register(TxtRecord)
class TxtAdmin(NautobotModelAdmin):
    pass


@admin.register(PtrRecord)
class PtrAdmin(NautobotModelAdmin):
    pass


@admin.register(LocRecord)
class LocAdmin(NautobotModelAdmin):
    pass


@admin.register(SshfpRecord)
class SshfpAdmin(NautobotModelAdmin):
    pass


@admin.register(CNameRecord)
class CnameAdmin(NautobotModelAdmin):
    pass
