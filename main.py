import json
from bravia.app_control import AppControl
from bravia.settings import settings


def main():
    b = AppControl(**settings)
    # request = b.set_power_status(status="off")

    # print(json.dumps(request, indent=2))
    # for x in request:
        # print(json.dumps(x.dict(), indent=2))

    print(json.dumps(b.get_system_information(), indent=2))

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
