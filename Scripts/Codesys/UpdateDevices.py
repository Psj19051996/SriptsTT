#
# update all devices in project
#
def update_device(proj):
    print("*** update device")

    # search for devices to update
    objects = proj.get_children(recursive=True)
    for object in objects:
        if object.is_device:
            print("*** found device")
            DeviceId = object.get_device_identification()
            devices = device_repository.get_all_devices()
            for device in devices:
                if device.device_id.type == DeviceId.type and device.device_id.id == DeviceId.id:
                    deviceToUpdate = device
            if deviceToUpdate != None:
                print ("*** found device to update %s" % deviceToUpdate.device_id)
                object.update(device=deviceToUpdate.device_id)