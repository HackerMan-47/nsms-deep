import pyshark

def start_capture():
    from django.apps import apps  # تحميل التطبيقات قبل استيراد models
    if not apps.ready:
        return  # تأكد أن التطبيقات جاهزة

    from .models import Alert, Packet  # استيراد models داخل الدالة فقط

    capture = pyshark.LiveCapture(interface='en0')  # استخدم الواجهة الصحيحة

    for packet in capture.sniff_continuously():
        source_ip = packet.ip.src if 'IP' in packet else 'N/A'
        destination_ip = packet.ip.dst if 'IP' in packet else 'N/A'
        protocol = packet.transport_layer if hasattr(packet, 'transport_layer') else 'N/A'
        length = packet.length if hasattr(packet, 'length') else 0

        # حفظ الحزمة في قاعدة البيانات
        Packet.objects.create(
            source_ip=source_ip,
            destination_ip=destination_ip,
            protocol=protocol,
            length=length
        )

        # اكتشاف حركة SSH المشبوهة
        if protocol == 'TCP' and hasattr(packet, 'tcp') and int(packet.tcp.dstport) == 22:
            Alert.objects.create(
                source_ip=source_ip,
                destination_ip=destination_ip,
                threat_type="SSH Traffic",
                severity="High"
            )
