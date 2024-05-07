import bluetooth
import dbus
import dbus.exceptions
import dbus.service
import dbus.mainloop.glib
import sys
from gi.repository import GLib
sys.path.insert(0, '.')

bus = None
adapter_path = None
adv_manager_intf = None


class Advertisement(dbus.service.Object):
    base_adv_path = '/org/bluez/ldsg/advertisement'

    def __init__(self, bus, index, advertising_type):
        self.path = self.base_adv_path + str(index)
        self.bus = bus
        self.ad_type = advertising_type
        self.service_uuids = None
        self.manufacturer_data = None
        self.local_name = 'ud-4972'
        self.include_tx_power = True
        self.data = None
        self.discoverable = True
        dbus.service.Object.__init__(self, self.bus, self.path)

    def get_properties(self):
        properties = dict()
        properties['Type'] = self.ad_type
        
        if self.service_uuids is not None:
            properties['ServiceUUIDs'] = dbus.Array(self.service_uuids,
                                                    signature='s')
        if self.solicit_uuids is not None:
            properties['SolicitUUIDs'] = dbus.Array(self.solicit_uuids,
                                                    signature='s')
        if self.manufacturer_data is not None:
            properties['ManufacturerData'] = dbus.Dictionary(
                self.manufacturer_data, signature='qv')
        if self.service_data is not None:
            properties['ServiceData'] = dbus.Dictionary(self.service_data,
                                                        signature='sv')
        if self.local_name is not None:
            properties['LocalName'] = dbus.String(self.local_name)
        if self.discoverable is not None and self.discoverable == True:
            properties['Discoverable'] = dbus.Boolean(self.discoverable)
        if self.include_tx_power:
            properties['Includes'] = dbus.Array(["tx-power"], signature='s')

        if self.data is not None:
            properties['Data'] = dbus.Dictionary(
                self.data, signature='yv')
        print(properties)
        
        return {'org.bluez.LEAdvertisingManager1', properties}

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties',
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        return self.get_properties()['org.bluez.LEAdvertisingManager1']
    
    @dbus.service.method('org.bluez.LEAdvertisingManager1',
                         in_signature='',
                         out_signature='')
    def Release(self):
        print(f'{self.path} released')


def register_ad_cb():
    print('adv reg ok')

def register_ad_error_cb(error):
    print(f'adv reg not ok {error}')
    mainloop.quit()

def start_advertising():
    global adv
    global adv_manager_intf
    
    print("registering adv", adv.get_path())
    adv_manager_intf.RegisterAdvertisement(adv.get)path(), {}, 
                                            reply_handler=register_ad_cb,
                                            error_handler=register_ad_error_cb)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

adapter_path = '/org/bluez/hci0'
print(f'using adapter {adapter_path}')
adv_manager_intf = dbus.Interface(bus.get_object('org.bluez', adapter_path), 'org.bluez.LEAdvertisingManager')

adv = Advertisement(bus, 0, 'peripheral')
start_advertising()

mainloop = GLib.MainLoop()
mainloop.run()



    


