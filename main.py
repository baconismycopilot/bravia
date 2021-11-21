import json

import bravia
from bravia.settings import settings, Settings


def main():
    app_config = Settings(**settings)
    b = bravia.Bravia(**app_config.dict())

    sys_info = b.get_system_information()
    print(sys_info.json(indent=2))
    service_list: list = [svc.get("service") for svc in b.api_info()]
    print(json.dumps(service_list, indent=2))
    print(b.get_interface_information().json(indent=2))

    '''
    app_list: List[AppModel] = b.app_list()
    for app in app_list:
        print(app.json(indent=2))
        if app.title == "TV":
            resp = b.set_active_app(app.uri)
            if len(resp.get("result")) > 0:
                return {"error": f"{app.title} could not be activated"}

        return {"msg": f"{app.title} activated"}
    '''


if __name__ == '__main__':
    main()
